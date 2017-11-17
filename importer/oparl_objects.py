import hashlib
import mimetypes
import os
from collections import defaultdict
from typing import Optional, Type

# noinspection PyPackageRequirements
import gi
import requests
from django.utils.translation import ugettext as _
# noinspection PyPackageRequirements
from slugify.slugify import slugify

from importer.oparl_helper import OParlHelper
from mainapp.models import Body, LegislativeTerm, Paper, Department, Committee, ParliamentaryGroup, Meeting, Location, \
    File, Person, AgendaItem, CommitteeMembership, DepartmentMembership, ParliamentaryGroupMembership
from mainapp.models.consultation import Consultation
from mainapp.models.default_fields import DefaultFields
from mainapp.models.paper_type import PaperType

gi.require_version('OParl', '0.2')
from gi.repository import OParl


class OParlObjects(OParlHelper):
    """ Methods for saving the oparl objects as database entries. """

    def __init__(self, options):
        super().__init__(options)

        # mappings that could not be resolved because the target object
        # hasn't been imported yet
        self.meeting_person_queue = defaultdict(list)
        self.agenda_item_paper_queue = {}
        self.membership_queue = []
        self.consultation_meeting_queue = []
        self.consultation_paper_queue = []

    def body(self, libobject: OParl.Body):
        body = self.check_existing(libobject, Body)
        if not body:
            return
        print("Processing {}".format(libobject.get_id()))

        body.save()

        terms = []
        for term in libobject.get_legislative_term():
            saved_term = self.term(term)
            if saved_term:
                terms.append(saved_term)

        body.legislative_terms = terms

        location = self.location(libobject.get_location())
        if location and location.geometry:
            if location.geometry["type"] == "Point":
                body.center = location
            elif location.geometry["type"] == "Polygon":
                body.outline = location
            else:
                message = "Location object is of type {}, which is neither 'Point' nor 'Polygon'." \
                          "Skipping this location.".format(location.geometry["type"])
                self.errorlist.append(message)

        body.save()

        return body

    def term(self, libobject: OParl.LegislativeTerm):
        if not libobject.get_start_date() or not libobject.get_end_date():
            print("Term has no start or end date - skipping")
            return

        term = self.check_existing(libobject, LegislativeTerm)
        if not term:
            return

        self.logger.info("Processing {}".format(libobject.get_name()))

        term.start = self.glib_datetime_to_python_date(libobject.get_start_date())
        term.end = self.glib_datetime_to_python_date(libobject.get_end_date())

        term.save()

        return term

    def paper(self, libobject: OParl.Paper):
        paper = self.check_existing(libobject, Paper)
        if not paper:
            return
        self.logger.info("Processing Paper {}".format(libobject.get_id()))

        if libobject.get_paper_type():
            paper_type, _ = PaperType.objects.get_or_create(defaults={"paper_type": libobject.get_paper_type()})
        else:
            paper_type = None

        paper.legal_date = self.glib_datetime_to_python_date(libobject.get_date())
        paper.reference_number = libobject.get_reference()
        paper.paper_type = paper_type
        paper.save()

        files = [self.file(file) for file in libobject.get_auxiliary_file()]
        paper.files = [file for file in files if file is not None]
        paper.main_file = self.file(libobject.get_main_file())

        for i in libobject.get_consultation():
            self.consultation(i)

        for org in libobject.get_under_direction_of_url():
            organization = self.get_organization_by_oparl_id(org)
            if isinstance(organization, Committee):
                paper.submitter_committees.add(organization)
            elif isinstance(organization, Department):
                paper.submitter_departments.add(organization)
            elif isinstance(organization, ParliamentaryGroup):
                paper.submitter_parliamentary_groups.add(organization)
            else:
                message = "Failed to find organization for {}".format(org)
                self.errorlist.append(message)

        paper.save()

        return paper

    def organization_to_class(self, libobject: OParl.Organization) -> Optional[Type[DefaultFields]]:
        classification = libobject.get_classification()
        if classification in self.organization_classification[Department]:
            return Department
        elif classification in self.organization_classification[Committee]:
            return Committee
        elif classification in self.organization_classification[ParliamentaryGroup]:
            return ParliamentaryGroup
        else:
            message = "Unknown Classification: {} ({})".format(classification, libobject.get_id())
            self.errorlist.append(message)
            return None

    def organization(self, libobject: OParl.Organization):
        self.logger.info("Processing Organization {}".format(libobject.get_id()))
        if not libobject:
            return
        org_type = self.organization_to_class(libobject)
        if not org_type:
            return

        organization = self.check_existing(libobject, org_type)
        if not organization:
            return

        organization.body = Body.by_oparl_id(libobject.get_body().get_id())
        if org_type == Department:
            assert not libobject.get_start_date() and not libobject.get_end_date()
        elif org_type == Committee:
            organization.start = self.glib_datetime_or_date_to_python(libobject.get_start_date())
            organization.end = self.glib_datetime_or_date_to_python(libobject.get_end_date())
        elif org_type == ParliamentaryGroup:
            organization.start = self.glib_datetime_or_date_to_python(libobject.get_start_date())
            organization.end = self.glib_datetime_or_date_to_python(libobject.get_end_date())
        else:
            assert False

        for membership in libobject.get_membership():
            self.membership(org_type, organization, membership)

        organization.save()

        return organization

    def meeting(self, libobject: OParl.Meeting):
        meeting = self.check_existing(libobject, Meeting)
        if not meeting:
            return
        self.logger.info("Processing Meeting {}".format(libobject.get_id()))

        meeting.start = self.glib_datetime_to_python(libobject.get_start())
        meeting.end = self.glib_datetime_to_python(libobject.get_end())
        meeting.location = self.location(libobject.get_location())
        meeting.invitation = self.file(libobject.get_invitation())
        meeting.verbatim_protocol = self.file(libobject.get_verbatim_protocol())
        meeting.results_protocol = self.file(libobject.get_results_protocol())
        meeting.cancelled = libobject.get_cancelled() or False

        meeting.save()

        auxiliary_files = []
        for oparlfile in libobject.get_auxiliary_file():
            djangofile = self.file(oparlfile)
            if djangofile:
                auxiliary_files.append(djangofile)
        meeting.auxiliary_files = auxiliary_files

        persons = []
        for oparlperson in libobject.get_participant():
            djangoperson = Person.by_oparl_id(oparlperson.get_id())
            if djangoperson:
                persons.append(djangoperson)
            else:
                self.meeting_person_queue[libobject.get_id()].append(oparlperson.get_id())
        meeting.persons = persons

        for index, oparlitem in enumerate(libobject.get_agenda_item()):
            self.agendaitem(oparlitem, index, meeting)

        meeting.save()

        return meeting

    def location(self, libobject: OParl.Location):
        self.logger.info("Processing Location {}".format(libobject.get_id()))
        location = self.check_existing(libobject, Location, name_fixup=_("Unknown"))
        if not location:
            return None

        location.oparl_id = libobject.get_id()
        location.description = libobject.get_description()
        location.is_official = self.official_geojson
        location.geometry = self.extract_geometry(libobject.get_geojson())
        location.save()

        return location

    def agendaitem(self, libobject: OParl.AgendaItem, index, meeting):
        item = self.check_existing(libobject, AgendaItem, add_defaults=False)
        if not item:
            return

        item.key = libobject.get_number()
        if not item.key:
            item.key = "-"

        item.oparl_id = libobject.get_id()
        item.key = libobject.get_number()
        item.title = libobject.get_name()
        item.position = index
        item.public = libobject.get_public()
        item.result = libobject.get_result()
        item.resolution_text = libobject.get_resolution_text()
        item.start = libobject.get_start()
        item.end = libobject.get_end()

        item.save()

        item.resolution_file = self.file(libobject.get_resolution_file())
        item.meeting = meeting
        if len(libobject.get_auxiliary_file()) > 0:
            item.auxiliary_files = [self.file(i) for i in libobject.get_auxiliary_file()]
        item.consultation = self.consultation(libobject.get_consultation())

        item.save()

        return item

    def consultation(self, libobject: OParl.Consultation):
        consultation = self.check_existing(libobject, Consultation, add_defaults=False)
        if not consultation:
            return

        consultation.oparl_id = libobject.get_id()
        consultation.authoritative = libobject.get_authoritative()
        consultation.role = libobject.get_role()

        if libobject.get_meeting():
            meeting = Meeting.objects.filter(oparl_id=libobject.get_meeting().get_id()).first()
            if not meeting:
                self.consultation_meeting_queue.append((consultation, libobject.get_meeting().get_id()))
            else:
                consultation.meeting = meeting
        if libobject.get_paper():
            paper = Meeting.objects.filter(oparl_id=libobject.get_paper().get_id()).first()
            if not paper:
                self.consultation_paper_queue.append((consultation, libobject.get_paper().get_id()))
            else:
                consultation.paper = paper

        consultation.save()

        # TODO consultation.organization = libobject.get_organization()

        # consultation.save()
        return consultation

    def download_file(self, file: File, libobject: OParl.File):
        url = libobject.get_download_url() or libobject.get_access_url()
        last_modified = self.glib_datetime_to_python(libobject.get_modified())

        if file.filesize > 0 and file.modified and last_modified < file.modified:
            self.logger.info("Skipping cached Download: {}".format(url))
            return

        print("Downloading {}".format(url))

        urlhash = hashlib.sha1(libobject.get_id().encode("utf-8")).hexdigest()
        path = os.path.join(self.storagefolder, urlhash)

        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
        open(path, 'wb').write(r.content)

        file.filesize = os.stat(path).st_size
        file.storage_filename = urlhash

    def file(self, libobject: OParl.File):
        file = self.check_existing(libobject, File, add_defaults=False)
        if not file:
            return
        self.logger.info("Processing File {}".format(libobject.get_id()))

        if libobject.get_file_name():
            displayed_filename = libobject.get_file_name()
        elif libobject.get_name():
            extension = mimetypes.guess_extension("application/pdf") or ""
            length = self.filename_length_cutoff - len(extension)
            displayed_filename = slugify(libobject.get_name())[:length] + extension
        else:
            displayed_filename = slugify(libobject.get_access_url())[-self.filename_length_cutoff:]

        file.oparl_id = libobject.get_id()
        file.name = libobject.get_name()[:200]  # FIXME
        file.displayed_filename = displayed_filename
        file.parsed_text = libobject.get_text()
        file.mime_type = libobject.get_mime_type() or "application/octet-stream"
        file.legal_date = self.glib_datetime_to_python_date(libobject.get_date())

        if self.download_files:
            self.download_file(file, libobject)
        else:
            file.storage_filename = ""
            file.filesize = -1

        if file.storage_filename and not file.parsed_text:
            self.extract_text_from_file(file)

        file.save()
        file.rebuild_locations()

        return file

    def person(self, libobject: OParl.Person):
        self.logger.info("Processing Person {}".format(libobject.get_id()))
        person = self.check_existing(libobject, Person)
        if not person:
            return

        person.name = libobject.get_name()
        person.given_name = libobject.get_given_name()
        person.family_name = libobject.get_family_name()
        person.location = self.location(libobject.get_location())
        person.save()

    def membership(self, classification, organization, libobject: OParl.Membership):
        person = Person.objects_with_deleted.filter(oparl_id=libobject.get_person().get_id()).first()
        if not person:
            self.membership_queue.append((classification, organization, libobject))
            return None

        role = libobject.get_role()
        if not role:
            role = _("Unknown")

        defaults = {
            "person": person,
            "start": self.glib_datetime_to_python_date(libobject.get_start_date()),
            "end": self.glib_datetime_to_python_date(libobject.get_end_date()),
            "role": role,
        }

        if classification in self.organization_classification[Department]:
            defaults["department"] = organization
            membership = DepartmentMembership.objects_with_deleted.get_or_create(oparl_id=libobject.get_id(),
                                                                                 defaults=defaults)
        elif classification in self.organization_classification[Committee]:
            defaults["committee"] = organization
            membership = CommitteeMembership.objects_with_deleted.get_or_create(oparl_id=libobject.get_id(),
                                                                                defaults=defaults)
        elif classification in self.organization_classification[ParliamentaryGroup]:
            defaults["parliamentary_group"] = organization
            membership = ParliamentaryGroupMembership.objects_with_deleted.get_or_create(oparl_id=libobject.get_id(),
                                                                                         defaults=defaults)
        else:
            message = "Unknown Classification: {} ({})".format(classification, libobject.get_id())
            self.errorlist.append(message)
            return

        return membership

    def add_missing_associations(self):
        print("Adding missing meeting <-> persons associations")
        for meeting_id, person_ids in self.meeting_person_queue.items():
            meeting = Meeting.by_oparl_id(meeting_id)
            meeting.persons = [Person.by_oparl_id(person_id) for person_id in person_ids]
            meeting.save()

        print("Adding missing agenda item <-> paper associations")
        for item_id, paper_id in self.agenda_item_paper_queue.items():
            item = AgendaItem.objects_with_deleted.get(oparl_id=item_id)
            item.paper = Paper.objects_with_deleted.filter(oparl_id=paper_id).first()
            if not item.paper:
                message = "Missing Paper: {}, ({})".format(paper_id, item_id)
                self.errorlist.append(message)
            item.save()

        print("Adding missing memberships")
        for classification, organization, libobject in self.membership_queue:
            self.membership(classification, organization, libobject)

        print("Adding missing papper to consultations")
        for consultation, paper in self.consultation_paper_queue:
            consultation.paper = Paper.by_oparl_id(paper)
            consultation.save()

        print("Adding missing meetings to consultations")
        for consultation, meeting in self.consultation_meeting_queue:
            consultation.meeting = Meeting.by_oparl_id(meeting)
            consultation.save()
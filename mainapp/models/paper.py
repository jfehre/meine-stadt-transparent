from django.db import models

from .committee import Committee
from .default_fields import DefaultFields
from .department import Department
from .file import File
from .parliamentary_group import ParliamentaryGroup
from .person import Person


class Paper(DefaultFields):
    reference_number = models.CharField(max_length=50)
    name = models.CharField(max_length=300)
    short_name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    submitter_parliamentary_groups = models.ManyToManyField(ParliamentaryGroup, blank=True)
    submitter_committees = models.ManyToManyField(Committee, blank=True)
    submitter_departments = models.ManyToManyField(Department, blank=True)
    # Only relevant if a person acts independently from one of the submitting organizations
    submitter_persons = models.ManyToManyField(Person, blank=True)
    # There isn't any logic built on change requests, so higher order change requests are allowed
    change_request_of = models.ForeignKey("self", null=True, blank=True)
    # This is relevant e.g. for deadlines
    legal_date = models.DateField(null=True, blank=True)
    main_file = models.ForeignKey(File, null=True, blank=True, related_name="paper_main_file")
    files = models.ManyToManyField(File, blank=True)
    paper_type = models.CharField(max_length=200, null=True, blank=True)

    def reference_number_autocomplete(self):
        """ A workaround to prevent empty values in the autocomplete-field in elasticsearch, which throws an error """
        return self.reference_number if len(self.reference_number) > 0 else ' '

    def __str__(self):
        return self.short_name

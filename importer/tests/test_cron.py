from unittest import mock

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from importer.models import ExternalList
from importer.tests.utils import (
    MockLoader,
    old_date,
    make_system,
    make_body,
    make_list,
    make_file,
    make_paper,
)


class TestCron(TestCase):
    """ [WIP] Tests that an file change sends out exactely one mail to only the subscribed user. """

    fixtures = ["cron.json"]

    system = make_system()
    body = make_body()

    def external_list_fixture(self):
        """
        Loads a fixture with two papers and two users, with one user beeing subscribed
        to one paper, and the external lists loaded.

        Should probably be moved into a json file
        """
        ExternalList(url=self.system["body"], last_update=old_date).save()
        ExternalList(url=self.body["person"], last_update=old_date).save()
        ExternalList(url=self.body["meeting"], last_update=old_date).save()
        ExternalList(url=self.body["organization"], last_update=old_date).save()
        ExternalList(url=self.body["paper"], last_update=old_date).save()

    def get_mock_loader(self):
        return MockLoader(
            self.system,
            {
                self.system["id"]: self.system,
                self.system["body"]: make_list([self.body]),
                self.body["id"]: self.body,
                self.body["meeting"]: make_list([]),
                self.body["organization"]: make_list([]),
                self.body["person"]: make_list([]),
                self.body["paper"]: make_list([]),
            },
        )

    def test_cron(self):
        """ WIP """
        self.external_list_fixture()
        loader = self.get_mock_loader()

        # Run cron. Check that nothing happend
        with mock.patch("mainapp.functions.notify_users.send_mail") as mocked_send_mail:
            with mock.patch(
                "importer.functions.get_loader_from_body", new=lambda body_id: loader
            ):
                call_command("cron")
            print(mocked_send_mail.call_count == 0)

    def cron_unfinished(self, loader):
        # In[]

        # Mock an extern list with changes to both paper

        new_date = timezone.now().astimezone().replace(microsecond=0)

        file1 = make_file(1)
        file2 = make_file(2)
        file2["modified"] = new_date
        file1["modified"] = new_date
        paper1 = make_paper([file1], paper_id=1)
        paper1["modified"] = new_date
        paper2 = make_paper([file2], paper_id=2)
        paper2["modified"] = new_date

        loader.api_data[self.body["paper"]] = make_list([paper1, paper2])

        # In[]

        # Run cron. Check that exactely the one user got one notification for the one paper

        with mock.patch("mainapp.functions.notify_users.send_mail") as mocked_send_mail:
            with mock.patch(
                "importer.functions.get_loader_from_body", new=lambda body_id: loader
            ):
                call_command("cron")
            print(mocked_send_mail.call_count == 1)

        # In[]

        # Run cron. Check that nothing happend

        with mock.patch("mainapp.functions.notify_users.send_mail") as mocked_send_mail:
            with mock.patch(
                "importer.functions.get_loader_from_body", new=lambda body_id: loader
            ):
                call_command("cron")
            print(mocked_send_mail.call_count == 0)

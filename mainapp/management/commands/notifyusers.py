from datetime import datetime

from dateutil.parser import parse
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from mainapp.functions.notify_users import NotifyUsers


class Command(BaseCommand):
    help = "Notifies users about new search results"

    def add_arguments(self, parser):
        parser.add_argument("--override-since", type=parse)
        parser.add_argument(
            "--simulate", action="store_true", help="Don't actually send any emails"
        )

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)

        notifier = NotifyUsers(datetime.fromisoformat(options["override_since"]), options["simulate"])
        notifier.notify_all()

import logging

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry

from mainapp.functions.minio import setup_minio

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Set all database up (mariadb, elasticsearch and minio)"

    def handle(self, *args, **options):
        self.stdout.write("Running migrations")
        call_command("migrate")
        if settings.ELASTICSEARCH_ENABLED:
            self.stdout.write("Creating elasticsearch indices")
            # The logic comes from django_elasticsearch_dsl.managment.commands.search_index:_create
            for index in registry.get_indices(registry.get_models()):
                # noinspection PyProtectedMember
                self.stdout.write(
                    f"Creating elasticsearch index '{index._name}' if not exists"
                )
                # https://elasticsearch-py.readthedocs.io/en/master/api.html:
                # "ignore 400 cause by IndexAlreadyExistsException when creating an index"
                # See also https://github.com/elastic/elasticsearch/issues/19862
                index.create(ignore=400)
        else:
            self.stdout.write("Elasticsearch is disabled; Not creating any indices")
        # This is more brittle, so we run it last
        self.stdout.write("Creating minio buckets")
        setup_minio()
        logger.info("Setup successful")

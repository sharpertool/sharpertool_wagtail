import re
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from wagtail.core.models import Site as WagtailSite


class Command(BaseCommand):
    help = 'Convert sites to *.local and update their port'

    def add_arguments(self, parser):
        parser.add_argument('domain')
        parser.add_argument('--port', type=int, default=443)

    def handle(self, *args, **options):
        newport = options.get('port')
        domain = options.get('domain')

        site = Site.objects.all()[0]
        site.domain = domain
        site.name = 'Sharpertool'
        site.save()

        wagsites = WagtailSite.objects.all()

        for site in wagsites:
            newhost = domain
            if newhost != site.hostname or site.port != newport:
                print(f"Updating {site.hostname} to {newhost} and Port from {site.port} to {newport}")
                site.hostname = newhost
                site.port = newport
                site.save()




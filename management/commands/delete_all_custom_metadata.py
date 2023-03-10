from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from geonode.base.models import ResourceBase
from geonode.base.models import ExtraMetadata

class Command(BaseCommand):
    help = _('Delete all ManyToMany relations from geonode.models.ResourceBase')

    def handle(self, *args, **options):
        confirm = input("Are you sure you want to delete all ManyToMany relations from geonode.models.ResourceBase? (y/n): ")
        if confirm.lower() == "y":
            resources = ResourceBase.objects.all()
            for resource in resources:
                resource.metadata.clear()
            self.stdout.write(self.style.SUCCESS('Successfully deleted all ManyToMany relations'))
        else:
            self.stdout.write(self.style.WARNING('Delete ManyToMany relations cancelled'))
from django.core.management.base import BaseCommand
from geonode.base.models import ResourceBase

class Command(BaseCommand):
    help = 'Delete the metadata associated with a ResourceBase instance'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='The id of the ResourceBase instance')

    def handle(self, *args, **options):
        resource_id = options['id']
        try:
            resource = ResourceBase.objects.get(pk=resource_id)
        except ResourceBase.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Resource with id {resource_id} does not exist'))
            return
        confirm = input("Are you sure you want to delete all metadata of this resource (y/n): ")
        if confirm == 'y':
            resource.metadata.clear()
            self.stdout.write(self.style.SUCCESS(f'All metadata deleted from resource {resource_id}'))
        else:
            self.stdout.write(self.style.WARNING(f'No metadata deleted from resource {resource_id}'))

from django.core.management.base import BaseCommand
from geonode.base.models import ResourceBase

class Command(BaseCommand):
    help = 'Print the metadata associated with a ResourceBase instance'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help='The id of the ResourceBase instance')

    def handle(self, *args, **options):
        resource_id = options['id']
        try:
            resource = ResourceBase.objects.get(pk=resource_id)
        except ResourceBase.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Resource with id {resource_id} does not exist'))
            return

        metadata = resource.metadata.all()
        if metadata:
            for m in metadata:
                self.stdout.write(self.style.SUCCESS(f'{m.metadata}'))
        else:
            self.stdout.write(self.style.ERROR('No metadata associated with this resource'))

from django.core.management.base import BaseCommand, CommandError
from img_app.models import Tag, Image


class Command(BaseCommand):
    help = "cleans database"

    def handle(self, *args, **options):
        Tag.objects.all().delete()
        Image.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f'dtabase clean'))

from django.core.management.base import BaseCommand, CommandError
from img_app.models import Tag, Image
from faker import Faker
from django.utils import timezone
import os
import random

fake = Faker()

class Command(BaseCommand):
    help = 'adds <num> images from <img_dir> to database'

    def add_arguments(self, parser):
        parser.add_argument('folder_path', type=str, help='Path to the folder containing images')
        parser.add_argument('count', type=int, help='Number of pictures to add')

    def handle(self, *args, **options):
        folder_path = options['folder_path']
        count = options['count']

        tag_names = ['tag1', 'tag2', 'tag3']  # Modify with your tag names

        image_files = os.listdir(folder_path)
        for _ in range(count):
            image_file_name = random.choice(image_files)
            image_file_path = os.path.join(folder_path, image_file_name)

            image = Image.objects.create(
                image=image_file_path,
                name=fake.word(),
                published=timezone.now(),
                description=fake.text(),
            )

            tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]
            random_tags = random.sample(tags, k=random.randint(1, len(tags) // 2))
            image.tags.add(*random_tags)

            self.stdout.write(self.style.SUCCESS(f'Successfully added image: {image.name}'))

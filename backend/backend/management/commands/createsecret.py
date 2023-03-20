from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a new secret key for the .env file.'

    def handle(self, *args, **options):
        from django.core.management.utils import get_random_secret_key
        new_secret_key = get_random_secret_key()
        self.stdout.write(self.style.SUCCESS(
            f'Copy this key into your .env file: {new_secret_key}'))

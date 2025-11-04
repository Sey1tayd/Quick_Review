from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables'

    def handle(self, *args, **options):
        username = config('SUPERUSER_USERNAME', default=None)
        email = config('SUPERUSER_EMAIL', default='admin@example.com')
        password = config('SUPERUSER_PASSWORD', default=None)

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'SUPERUSER_USERNAME and SUPERUSER_PASSWORD environment variables not set. Skipping superuser creation.'
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists. Skipping.')
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created superuser "{username}"')
        )

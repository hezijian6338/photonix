import os
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from photonix.photos.models import Library, LibraryPath, LibraryUser
from photonix.photos.utils.db import record_photo
from photonix.photos.utils.fs import determine_destination, download_file


User = get_user_model()


class Command(BaseCommand):
    help = 'Create a library for a user'

    def create_library(self, username, library_name):
        # Get user
        user = User.objects.get(username=username)

        # Create Library
        library, _ = Library.objects.get_or_create(
            name=library_name,
        )
        library_path, _ = LibraryPath.objects.get_or_create(
            library=library,
            type='St',
            backend_type='Lo',
            path='/data/photos/',
            url='/photos/',
        )
        library_user, _ = LibraryUser.objects.get_or_create(
            library=library,
            user=user
        )

        print(f'Library "{library_name}" created successfully for user "{username}"')

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('username', nargs='+', type=str)
        parser.add_argument('library_name', nargs='+', type=str)

    def handle(self, *args, **options):
        self.create_library(options['username'][0], options['library_name'][0])

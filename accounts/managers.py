from django.contrib.auth.models import UserManager
from django.db import models


class AccountManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email and password:  # TODO: fix from dirty hack into check social strategy
            raise ValueError('User must have a valid email address')
        email = self.normalize_email(email).lower()
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not email:
            # in social with email only email=username
            if '@' in username:
                email, username = username, email.split('@')[0]
            else:
                email = '%s@email.com' % username
        email_valid = False if '@email' in email else True
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('email_valid', email_valid)
        extra_fields.setdefault('send_email_notifications', email_valid)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        username = email.split('@')[0]
        return self._create_user(username, email, password, **extra_fields)

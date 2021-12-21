# Core Django imports
import uuid as uuid_lib

from django.db import models
from django.core import validators
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    UserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


class User(AbstractUser):
    uuid = models.UUIDField(
        primary_key=True, default=uuid_lib.uuid4, editable=False)
    username = models.CharField(
        _('username'), max_length=255, unique=True,
        validators=[
            validators.RegexValidator(
                '^[\\w.@+-]+$', 'Enter a valid username.',
                'invalid')
        ],
        error_messages={
            'unique': 'A user with that username already exists.'
        },
    )
    email = models.EmailField(
        _('email address'), unique=True)
    first_name = models.CharField(
        _('first name'), max_length=30, blank=True)
    last_name = models.CharField(
        _('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now)
    is_staff = models.BooleanField(
        _('staff status'), default=False)
    is_active = models.BooleanField(
        _('active'), default=True)

    def __str__(self):
        return '{} {}'.format(self.get_full_name(), self.email)

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

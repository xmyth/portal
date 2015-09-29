from django.db import models
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.models import (
    BaseUserManager,  AbstractUser
)
from django.utils import six, timezone


class EmployeeManager(BaseUserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)

class Department(models.Model):
    name = models.CharField(_("Name"), max_length=128, unique=True)
    desc = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    employee_num  = models.CharField(_("Employee No"), max_length=32, unique=True)
    departments   = models.ManyToManyField(Department)
    telephone_num = models.CharField(_("Telephone Number"), max_length=32)
    leave_data    = models.DateField(_("Leave Data"), blank=True, null=True)
    desc          = models.TextField(_("Description"), blank=True)
    
    objects = EmployeeManager()

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')    

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']

    # def get_full_name(self):
    #     # The user is identified by their email address
    #     return self.email

    # def get_short_name(self):
    #     # The user is identified by their email address
    #     return self.email

    # def __str__(self):              # __unicode__ on Python 2
    #     return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin
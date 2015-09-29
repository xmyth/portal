from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _ 
from hr.models import Employee, Department


class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('username','departments',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(EmployeeCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EmployeeChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmployeeChangeForm, self).__init__(*args, **kwargs)

class EmployeeAdmin(UserAdmin):
    # The forms to add and change user instances
    form = EmployeeChangeForm
    add_form = EmployeeCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password', 'departments', "employee_num")}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'telephone_num')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'leave_data')}),
    )

    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple()},
    }
# Now register the new UserAdmin...
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.

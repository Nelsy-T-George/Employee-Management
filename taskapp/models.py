from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
EMPLOYEE_ROLE = (
    ('Software Developer', 'Software Developer'),
    ('Project Manager', 'Project Manager'),
    ('Team Lead ', 'Team Lead'),
    ('System Engineer', 'System Engineer'),
    ('Marketing Head', 'Marketing Head'),
)
PRIORITY = (
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High')
)

class Role(models.Model):
    name = models.CharField(max_length=100, choices=EMPLOYEE_ROLE, default='Software Developer',unique=True)

    class Meta:
        db_table = "role"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Role, blank=True, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return "{0}".format(self.get_full_name())

@receiver(post_save, sender=Employee)
def emp_created(sender, instance, created, **kwargs):
    if created:
        instance.employee_id = "EMP-{}".format(str(instance.id).zfill(3))
        instance.save()


class Comments(models.Model):
    comment_text = models.TextField()
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'comments'

class Task(models.Model):

    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=100, choices=PRIORITY, default='Low')
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(null=True)
    time = models.TimeField(null=True, blank=True)
    employee = models.ForeignKey(Employee, blank=True, null=True, on_delete=models.SET_NULL)
    is_status = models.BooleanField(default=False)
    created_by = models.CharField(max_length=255,null=True, blank=True)
    updated_by = models.CharField(max_length=255,null=True, blank=True)
    comment = models.ManyToManyField(Comments, blank=True)

    def __str__(self):
        """
        function returns unicode representaion of a task
        """
        return self.title
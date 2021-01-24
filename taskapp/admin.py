from django.contrib import admin

# Register your models here.
from .models import Employee,Role

EMPLOYEE_ROLE = (
    ('Software Developer', 'Software Developer'),
    ('Project Manager', 'Project Manager'),
    ('Team Lead ', 'Team Lead'),
    ('System Engineer', 'System Engineer'),
    ('Marketing Head', 'Marketing Head'),
)

class EmployeeAdmin(admin.ModelAdmin):
    exclude = ['employee_id']


admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Role)

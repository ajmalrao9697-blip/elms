from django.contrib import admin
from .models import Employee, Attendance, Salary

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'designation', 'date_joined', 'is_active')
    list_filter = ('designation', 'is_active', 'date_joined')
    search_fields = ('employee_id', 'name', 'cnic')
    list_editable = ('is_active',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'total_days', 'leaves', 'present_days')
    list_filter = ('month', 'year', 'employee__designation')
    search_fields = ('employee__name', 'employee__employee_id')
    autocomplete_fields = ('employee',)

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'total_salary', 'received_salary', 'status', 'payment_date')
    list_filter = ('status', 'month', 'year', 'payment_date')
    search_fields = ('employee__name', 'employee__employee_id')
    autocomplete_fields = ('employee',)
    readonly_fields = ('created_at', 'updated_at')
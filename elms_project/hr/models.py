from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200, blank=True, null=True)
    mother_name = models.CharField(max_length=200, blank=True, null=True)
    cnic = models.CharField(max_length=30, blank=True, null=True, unique=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_joined = models.DateField(default=timezone.now, blank=True, null=True)  # Make nullable first
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employee_id} - {self.name}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    month = models.CharField(max_length=20)
    year = models.PositiveSmallIntegerField(
        default=timezone.now().year,
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )
    total_days = models.PositiveSmallIntegerField(default=0)
    leaves = models.PositiveSmallIntegerField(default=0)
    present_days = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Make nullable first
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Make nullable first

    class Meta:
        unique_together = (('employee', 'month', 'year'),)
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.employee.employee_id} - {self.month}/{self.year}"

class Salary(models.Model):
    STATUS_CHOICES = (('Paid','Paid'),('Unpaid','Unpaid'))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    month = models.CharField(max_length=20)
    year = models.PositiveSmallIntegerField(
        default=timezone.now().year,
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    received_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid')
    payment_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Make nullable first
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)  # Make nullable first

    class Meta:
        unique_together = (('employee', 'month', 'year'),)
        ordering = ['-year', '-month']

    def save(self, *args, **kwargs):
        if self.received_salary >= self.total_salary:
            self.status = 'Paid'
            if not self.payment_date:
                self.payment_date = timezone.now().date()
        else:
            self.status = 'Unpaid'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.employee_id} - Salary {self.month}/{self.year}"
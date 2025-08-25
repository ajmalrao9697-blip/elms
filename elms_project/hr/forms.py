from django import forms
from .models import Employee, Attendance, Salary
from django.utils import timezone

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'month': forms.Select(choices=[
                ('January', 'January'), ('February', 'February'), 
                ('March', 'March'), ('April', 'April'), 
                ('May', 'May'), ('June', 'June'), 
                ('July', 'July'), ('August', 'August'), 
                ('September', 'September'), ('October', 'October'), 
                ('November', 'November'), ('December', 'December')
            ]),
            'year': forms.NumberInput(attrs={
                'min': 2000, 
                'max': 2100,
                'value': timezone.now().year
            }),
        }

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = '__all__'
        widgets = {
            'month': forms.Select(choices=[
                ('January', 'January'), ('February', 'February'), 
                ('March', 'March'), ('April', 'April'), 
                ('May', 'May'), ('June', 'June'), 
                ('July', 'July'), ('August', 'August'), 
                ('September', 'September'), ('October', 'October'), 
                ('November', 'November'), ('December', 'December')
            ]),
            'year': forms.NumberInput(attrs={
                'min': 2000, 
                'max': 2100,
                'value': timezone.now().year
            }),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'total_salary': forms.NumberInput(attrs={'step': '0.01'}),
            'received_salary': forms.NumberInput(attrs={'step': '0.01'}),
        }
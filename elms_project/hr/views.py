from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime
from .models import Employee, Attendance, Salary
from .forms import EmployeeForm, AttendanceForm, SalaryForm
import csv

# ------------------- DASHBOARD -------------------
@login_required
def dashboard(request):
    emp_count = Employee.objects.filter(is_active=True).count()
    current_month = timezone.now().strftime('%B')
    current_year = timezone.now().year

    attendance_stats = Attendance.objects.filter(month=current_month, year=current_year)\
                        .aggregate(total_present=Sum('present_days'), total_leaves=Sum('leaves'))
    salary_stats = Salary.objects.filter(month=current_month, year=current_year)\
                        .aggregate(total_payable=Sum('total_salary'), total_paid=Sum('received_salary'))

    context = {
        'emp_count': emp_count,
        'attendance_stats': attendance_stats,
        'salary_stats': salary_stats,
        'current_month': current_month,
        'current_year': current_year
    }
    return render(request, 'hr/dashboard.html', context)

# ------------------- EMPLOYEES -------------------
@login_required
def employee_list(request):
    query = request.GET.get('q', '')
    employees = Employee.objects.filter(
        Q(employee_id__icontains=query) |
        Q(name__icontains=query) |
        Q(cnic__icontains=query) |
        Q(designation__icontains=query)
    ).order_by('employee_id') if query else Employee.objects.all().order_by('employee_id')

    template = 'hr/partials/_employee_table.html' if request.headers.get('HX-Request') == 'true' else 'hr/employee_list.html'
    return render(request, template, {'employees': employees})

@login_required
def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        e = form.save()
        if request.headers.get('HX-Request') == 'true':
            html = render_to_string('hr/partials/_employee_row.html', {'e': e})
            return HttpResponse(html)
        messages.success(request, f'Employee {e.name} created successfully!')
        return redirect('hr:employee_list')
    template = 'hr/partials/_employee_form.html' if request.headers.get('HX-Request') == 'true' else 'hr/employee_form.html'
    return render(request, template, {'form': form})

@login_required
def employee_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=emp)
    if request.method == 'POST' and form.is_valid():
        e = form.save()
        if request.headers.get('HX-Request') == 'true':
            html = render_to_string('hr/partials/_employee_row.html', {'e': e})
            return HttpResponse(html)
        messages.success(request, f'Employee {e.name} updated successfully!')
        return redirect('hr:employee_list')
    return render(request, 'hr/partials/_employee_form.html', {'form': form, 'emp': emp})

@login_required
def employee_detail(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    context = {
        'emp': emp,
        'recent_attendance': emp.attendances.all().order_by('-year', '-month')[:5],
        'recent_salaries': emp.salaries.all().order_by('-year', '-month')[:5]
    }
    return render(request, 'hr/employee_detail.html', context)

@login_required
def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        emp_name = emp.name
        emp.delete()
        if request.headers.get('HX-Request') == 'true':
            return HttpResponse(status=204)
        messages.success(request, f'Employee {emp_name} deleted successfully!')
        return redirect('hr:employee_list')
    return render(request, 'hr/partials/_confirm_delete.html', {'obj': emp, 'obj_type': 'employee'})

# ------------------- ATTENDANCE -------------------
@login_required
def attendance_list(request):
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')
    attends = Attendance.objects.select_related('employee').all().order_by('-year', '-month')
    if month: attends = attends.filter(month__iexact=month)
    if year: attends = attends.filter(year=year)
    return render(request, 'hr/attendance_list.html', {'attends': attends})

@login_required
def attendance_create(request):
    form = AttendanceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        a = form.save()
        if request.headers.get('HX-Request') == 'true':
            html = render_to_string('hr/partials/_attendance_row.html', {'a': a})
            return HttpResponse(html)
        messages.success(request, f'Attendance record for {a.employee.name} created successfully!')
        return redirect('hr:attendance_list')
    return render(request, 'hr/partials/_attendance_form.html', {'form': form})

@login_required
def attendance_edit(request, pk):
    a = get_object_or_404(Attendance, pk=pk)
    form = AttendanceForm(request.POST or None, instance=a)
    if request.method == 'POST' and form.is_valid():
        a = form.save()
        if request.headers.get('HX-Request') == 'true':
            html = render_to_string('hr/partials/_attendance_row.html', {'a': a})
            return HttpResponse(html)
        messages.success(request, f'Attendance record for {a.employee.name} updated successfully!')
        return redirect('hr:attendance_list')
    return render(request, 'hr/partials/_attendance_form.html', {'form': form, 'a': a})

@login_required
def attendance_delete(request, pk):
    a = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        a.delete()
        if request.headers.get('HX-Request') == 'true':
            return HttpResponse(status=204)
        messages.success(request, 'Attendance record deleted successfully!')
        return redirect('hr:attendance_list')
    return render(request, 'hr/partials/_confirm_delete.html', {'obj': a, 'obj_type': 'attendance record'})

# ------------------- SALARY -------------------
@login_required
def salary_list(request):
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')
    status = request.GET.get('status', '')
    salaries = Salary.objects.select_related('employee').all().order_by('-year', '-month')
    if month: salaries = salaries.filter(month__iexact=month)
    if year: salaries = salaries.filter(year=year)
    if status: salaries = salaries.filter(status=status)
    return render(request, 'hr/salary_list.html', {'salaries': salaries})

@login_required
def salary_create(request):
    form = SalaryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        s = form.save()
        if request.headers.get('HX-Request') == 'true':
            html = render_to_string('hr/partials/_salary_row.html', {'s': s})
            return HttpResponse(html)
        messages.success(request, f'Salary record for {s.employee.name} created successfully!')
        return redirect('hr:salary_list')
    return render(request, 'hr/partials/_salary_form.html', {'form': form})

@login_required
def salary_edit(request, pk):
    s = get_object_or_404(Salary, pk=pk)
    form = SalaryForm(request.POST or None, instance=s)
    if request.method == 'POST' and form.is_valid():
        s = form.save()
        if request.headers.get('HX-Request') == 'true':
            html = render_to_string('hr/partials/_salary_row.html', {'s': s})
            return HttpResponse(html)
        messages.success(request, f'Salary record for {s.employee.name} updated successfully!')
        return redirect('hr:salary_list')
    return render(request, 'hr/partials/_salary_form.html', {'form': form, 's': s})

@login_required
def salary_delete(request, pk):
    s = get_object_or_404(Salary, pk=pk)
    if request.method == 'POST':
        s.delete()
        if request.headers.get('HX-Request') == 'true':
            return HttpResponse(status=204)
        messages.success(request, 'Salary record deleted successfully!')
        return redirect('hr:salary_list')
    return render(request, 'hr/partials/_confirm_delete.html', {'obj': s, 'obj_type': 'salary record'})

# ------------------- LETTERS -------------------
@login_required
def generate_letter(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        letter_type = request.POST.get('letter_type', 'offer_letter')

        employee = get_object_or_404(Employee, employee_id=employee_id)
        template_map = {
            'offer_letter': 'hr/letters/offer_letter.html',
            'experience_letter': 'hr/letters/experience_letter.html',
            'resignation_letter': 'hr/letters/resignation_letter.html',
            'termination_letter': 'hr/letters/termination_letter.html',
            'warning_letter': 'hr/letters/warning_letter.html',
        }
        template_name = template_map.get(letter_type)
        if not template_name:
            return HttpResponse("Invalid letter type.", status=400)

        return render(request, template_name, {'employee': employee, 'date': datetime.today()})

    return render(request, 'hr/partials/_letter_form.html')

# ------------------- EXPORTS -------------------
@login_required
def export_employees_csv(request):
    qs = Employee.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=employees.csv'
    writer = csv.writer(response)
    writer.writerow(['Employee ID','Name','Father Name','Mother Name','CNIC','Designation','Contact','Address', 'Date Joined', 'Status'])
    for e in qs:
        writer.writerow([
            e.employee_id, e.name, e.father_name or '', e.mother_name or '', 
            e.cnic or '', e.designation or '', e.contact_number or '', 
            e.address or '', e.date_joined, 'Active' if e.is_active else 'Inactive'
        ])
    return response

@login_required
def export_attendance_csv(request):
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')
    qs = Attendance.objects.select_related('employee').all()
    if month: qs = qs.filter(month__iexact=month)
    if year: qs = qs.filter(year=year)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=attendance_{month}_{year}.csv'
    writer = csv.writer(response)
    writer.writerow(['Employee ID','Name','CNIC','Month','Year','Total Days','Leaves','Present Days'])
    for a in qs:
        writer.writerow([
            a.employee.employee_id, a.employee.name, a.employee.cnic or '', 
            a.month, a.year, a.total_days, a.leaves, a.present_days
        ])
    return response

@login_required
def export_salary_csv(request):
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')
    status = request.GET.get('status', '')
    qs = Salary.objects.select_related('employee').all()
    if month: qs = qs.filter(month__iexact=month)
    if year: qs = qs.filter(year=year)
    if status: qs = qs.filter(status=status)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=salary_{month}_{year}.csv'
    writer = csv.writer(response)
    writer.writerow(['Employee ID','Name','CNIC','Month','Year','Total Salary','Received Salary','Status','Payment Date'])
    for s in qs:
        writer.writerow([
            s.employee.employee_id, s.employee.name, s.employee.cnic or '', 
            s.month, s.year, s.total_salary, s.received_salary, 
            s.status, s.payment_date or ''
        ])
    return response

# ------------------- UTILITIES -------------------
@login_required
def get_employee_details(request, employee_id):
    try:
        employee = Employee.objects.get(employee_id=employee_id)
        return JsonResponse({
            'name': employee.name,
            'designation': employee.designation,
            'cnic': employee.cnic
        })
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

@login_required
def requests_list(request):
    return HttpResponse("<h5>No pending requests found.</h5>")
@login_required
def star_animation(request):
    return render(request, 'hr/stars.html')
def dashboard(request):
    context = {
        'employees_count': 42,
        'attendance_count': 127,
        'salary_count': 86,
        'pending_requests': 12,
    }
    return render(request, 'hr/dashboard.html', context)
def employee_list(request):
    employees = Employee.objects.all()  # or any other queryset
    return render(request, 'hr/employee_list.html', {'employees': employees})


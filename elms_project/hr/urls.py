from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'hr'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # 🔹 Login & Logout URLs
    path('login/', auth_views.LoginView.as_view(template_name='hr/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='hr:login'), name='logout'),

    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('employees/<int:pk>/detail/', views.employee_detail, name='employee_detail'),
    
    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/<int:pk>/edit/', views.attendance_edit, name='attendance_edit'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),
    
    # Salary URLs
    path('salary/', views.salary_list, name='salary_list'),
    path('salary/create/', views.salary_create, name='salary_create'),
    path('salary/<int:pk>/edit/', views.salary_edit, name='salary_edit'),
    path('salary/<int:pk>/delete/', views.salary_delete, name='salary_delete'),
    
    # Letters URLs
    path('generate-letter/', views.generate_letter, name='generate_letter'),
    path('letters/', views.generate_letter, name='letters'),  

    # Export URLs
    path('export/employees/', views.export_employees_csv, name='export_employees_csv'),
    path('export/attendance/', views.export_attendance_csv, name='export_attendance_csv'),
    path('export/salary/', views.export_salary_csv, name='export_salary_csv'),

    # Employee details
    path('employee-details/<str:employee_id>/', views.get_employee_details, name='get_employee_details'),

    # Requests list
    path('requests/', views.requests_list, name='requests_list'),
    path('stars/', views.star_animation, name='star_animation'),  
]

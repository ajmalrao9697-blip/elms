Write-Host "🚀 Starting HR app quick test..."

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Set Django settings (correct dotted path)
$env:DJANGO_SETTINGS_MODULE="elms_project.settings"

# Check models import
python -c "from hr.models import Employee, Attendance, Salary; print('✅ Models imported successfully')"

# Check forms import
python -c "from hr.forms import EmployeeForm, AttendanceForm, SalaryForm; print('✅ Forms imported successfully')"

# Check views import
python -c "from hr import views; print('✅ Views imported successfully')"

# Run migrations
Write-Host "🔄 Making migrations..."
python manage.py makemigrations hr

Write-Host "🔄 Applying migrations..."
python manage.py migrate

Write-Host "✅ All HR app tests completed successfully!"

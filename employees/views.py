from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def is_staff_user(user):
    return user.groups.filter(name='Staff').exists()

# @login_required
# def employee_list(request):
#     employees = Employee.objects.all()

#     return render(
#         request,
#         'employees/employee_list.html',
#         {'employees': employees}
#     )

@login_required
def employee_list(request):

    if request.user.groups.filter(name='Staff').exists():

        employees = Employee.objects.all()
        is_staff_role = True

    elif request.user.groups.filter(name='Employee').exists():

        employees = Employee.objects.filter(
            user=request.user
        )
        is_staff_role = False

    else:

        employees = Employee.objects.none()
        is_staff_role = False

    return render(
        request,
        'employees/employee_list.html',
        {
            'employees': employees,
            'is_staff_role': is_staff_role
        }
    )

# def employee_list(request):

#     employee = Employee.objects.get(user=request.user)

#     return render(
#         request,
#         'employees/employee_list.html',
#         {'employee': employee}
#     )

@login_required
def employee_create(request):

    if not is_staff_user(request.user):
        return redirect('employee_list')

    if request.method == 'POST':
        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('employee_list')

    else:
        form = EmployeeForm()

    return render(
        request,
        'employees/employee_form.html',
        {'form': form}
    )

@login_required
def employee_update(request, id):

    if not is_staff_user(request.user):
        return redirect('employee_list')
    
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()
            return redirect('employee_list')

    else:
        form = EmployeeForm(instance=employee)

    return render(
        request,
        'employees/employee_form.html',
        {
            'form': form,
            'employee': employee
        }
    )

@login_required
def employee_delete(request, id):

    if not is_staff_user(request.user):
            return redirect('employee_list')
    
    employee = get_object_or_404(Employee, id=id)
    
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')

    return render(
        request,
        'employees/employee_confirm_delete.html',
        {'employee': employee}
    )

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(
        request,
        'employees/register.html',
        {'form': form}
    )
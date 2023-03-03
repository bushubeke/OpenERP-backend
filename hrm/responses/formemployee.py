from . import *


@hr_app.route('/employee',methods=["GET","POST"])
def form_employee():
    return render_template('hrm/employee.html', emp_form=EmployeeForm(),
    doc_form=FileForms(), addr_form=AddressForm(),bank_form=BankDetailsForm())
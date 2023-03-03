from . import *

@hr_app.route('/empops',methods=["POST","PATCH","DELETE"])
@roles_accepted('superuser','Hr Admin')
def employee():
    emp_form=EmployeeForm()
    if request.method == "POST":
        try:
            data=dict(emp_form.data)    
            data.pop('csrf_token')
            data['user_id']=data['user_id'].id
            if  data['manager_id']:
                data['manager_id']=data['manager_id'].id
            else:
                data.pop('manager_id')
            db.session.add(Employee(**data))
            db.session.commit()
            flash("creation sucess")
            return redirect(url_for('hrapp.form_employee'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            flash("Something went wrong when updating the Database")
            return render_template('hrm/employee.html', emp_form=EmployeeForm(**data),\
            doc_form=FileForms(), addr_form=AddressForm(),bank_form=BankDetailsForm())
        finally:
            db.session.close()
    else:
        flash('Form validation has failed')
        return render_template('hrm/employee.html', emp_form=EmployeeForm(**data),\
            doc_form=FileForms(), addr_form=AddressForm(),bank_form=BankDetailsForm())

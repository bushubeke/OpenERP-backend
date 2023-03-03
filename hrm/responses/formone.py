from . import *

@hr_app.route('/form',methods=["GET","POST"])
@roles_accepted('superuser')
def formone():
    register_form=EmployeeFormLayout()
    return render_template('hrm/layout.html', form=register_form)

from . import *


@hr_app.route('/sample',methods=["GET","POST"])
def form_three():
    register_form=EmployeeSampleForm()
    return render_template('hrm/updateemployee.html', form=register_form)
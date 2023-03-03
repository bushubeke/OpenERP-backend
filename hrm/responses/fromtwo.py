from . import *

@hr_app.route('/formwtf',methods=["GET","POST"])
def formtwo():
    register_form=EmployeeTestForm()
    if register_form.validate_on_submit():
        return render_template('hrm/formwtf.html', form=register_form)
    return render_template('hrm/formwtf.html', form=register_form)
from . import *

@hr_app.route('/automated',methods=["GET","POST"])
def automation_page():
     setAll=SetLeaveForm()
     setSpecfic=SetSpecficLeaveForm()
     return render_template('hrm/automated.html',setAll=setAll,setSpecfic=setSpecfic)


@hr_app.route('/passwordreset/<uid>',methods=["POST"])
@roles_accepted('superuser','Hr Admin')
def password_reset_type(uid):
    pass


@hr_app.route('/activate/<uid>',methods=["GET","POST"])
@roles_accepted('superuser','Hr Admin')
def activate_employee(uid):
    try:
        user=db.session.execute(update(User).where(User.uid == uid).values(disabled=False))
        db.session.commit()
        flash('sucessfully activated')
        return  redirect(url_for('hrapp.view_single_employee',uid=uid))
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e),exc_info=True)
        flash('Something went wrong or the user does not exist')
        return redirect(url_for('hrapp.view_single_employee',uid=uid))
    finally:
        db.session.close()

@hr_app.route('/deactivate/<uid>',methods=["GET","POST"])
@roles_accepted('superuser','Hr Admin')
def deactivate_employee(uid):
    try:
        user=db.session.execute(update(User).where(User.uid == uid).values(disabled=True))
        db.session.commit()
        flash('sucessfully deactivated')
        return redirect(url_for('hrapp.view_single_employee',uid=uid))
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e),exc_info=True)
        flash('Something went wrong or the user does not exist')
        return redirect(url_for('hrapp.view_single_employee',uid=uid))
    finally:
        db.session.close()

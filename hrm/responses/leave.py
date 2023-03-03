from . import *


@hr_app.route('/leave',methods=["GET","POST","PATCH","DELETE"])
@roles_accepted('superuser','Hr Admin')
def form_add_view_leave_type():
    leave_typeform=LeaveConfigForm()  
    leavetypes=db.session.execute(select(LeaveConfig))
    leavetypes=leavetypes.unique().scalars().all()
    leavetypes=[LeaveConfigModel.from_orm(x).dict() for x in leavetypes]
    leavetypes_form=[EditLeaveConfigForm(**x) for x in leavetypes]
    deletetypes_form=[DeleteLeaveConfigForm(**x) for x in leavetypes]
    leave_typs_zip=zip(leavetypes,leavetypes_form,deletetypes_form) 
    if request.method == "GET":
        return render_template('hrm/leave.html', form=leave_typeform,leave_types=leave_typs_zip)
    elif request.method == 'POST':
        try:
            data=dict(leave_typeform.data)
            if leave_typeform.validate() or data['days']==0:
                data.pop('csrf_token')
                lt=LeaveConfig(**data)
                try:
                    db.session.add(lt)
                    db.session.commit()
                    flash('Created Object successfully')
                    return redirect(url_for('hrapp.form_add_view_leave_type'))
                except Exception as e:
                    flash('Creating object Failed')
                    current_app.logger.error(str(e),exc_info=True)
                    render_template('hrm/leave.html', form=leave_typeform,leave_types=leave_typs_zip)
            else:
                flash("Validation of form failed or Something went wrong")
                return render_template('hrm/leave.html', form=leave_typeform,leave_types=leave_typs_zip)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            render_template('hrm/leave.html', form=leave_typeform,leave_types=leave_typs_zip)
        finally:
            db.session.close()
    elif request.method == "PATCH":    
        try:
            dataup=loads(request.data)
            dataup.pop('csrf_token')
            try: 
                db.session.execute(update(LeaveConfig).where(LeaveConfig.id == dataup['id']).values(**dataup))
                db.session.commit()
                return { "Message" : "Update Sucessful"},status.HTTP_202_ACCEPTED
            except Exception as e:
                flash('Updating object Failed')
                current_app.logger.error(str(e),exc_info=True)
                render_template('hrm/leave.html', form=leave_typeform,leave_types=leave_typs_zip)
        
        except Exception as e:
            db.session.rollback()
            flash('Something has happened')
            current_app.logger.error(str(e),exc_info=True)
            return { "Message" : str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            db.session.close()
    elif request.method == "DELETE":
        try:
            datadel=loads(request.data)
            if DeleteLeaveConfigForm(**datadel).validate():
                try:
                    dt=db.session.execute(delete(LeaveConfig).where(LeaveConfig.id == int(datadel['id'])))
                    dt2=db.session.execute(delete(EmployeeLeave).where(EmployeeLeave.leave_config_id == int(datadel['id'])))
                    db.session.commit()
                    return {"Message" : "Entry deleted successfully"},status.HTTP_202_ACCEPTED
                except Exception as e:
                    flash('Removing object Failed')
                    current_app.logger.error(str(e),exc_info=True)
                    render_template('hrm/leave.html', form=leave_typeform,leave_types=leave_typs_zip)
            else:
                flash("Validation of form failed or something went wrong")
                render_template('hrm/leave.html', form=leave_typeform,leave_types=leave_typs_zip)
        except Exception as e:
            current_app.logger.error(str(e),exc_info=True)
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            return { "Message" : str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            
            db.session.close()
    else:
        return { "Message" : "Not Allowed Type of Request"},status.HTTP_405_METHOD_NOT_ALLOWED


@hr_app.route('/setleave',methods=["POST"])
@roles_accepted('superuser','Hr Admin')
def set_leave():
    if request.method == "POST":
        try:
            data=dict(SetLeaveForm().data)
            employees=db.session.execute(select(Employee.id)).scalars().unique().all()
            dbdata=[EmployeeLeave(employee_id =x,leave_year=int(data['year']),leave_config_id=data['leave_type'].id,days=data['leave_type'].days ) for x in employees \
                if db.session.execute(select(EmployeeLeave.id).where(EmployeeLeave.leave_year==int(data['year'])).where(EmployeeLeave.leave_config_id==data['leave_type'].id).\
                where(EmployeeLeave.employee_id == x)).scalar() is None]
            db.session.add_all(dbdata)
            db.session.commit()
            flash('Sucessfully set leaves')
            return redirect(url_for('hrapp.automation_page'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            flash("Something Unexpected happened, please contact adminstrator if the problem persists")
            return redirect(url_for('hrapp.automation_page'))
    else:
        return { "Message" : "Not Allowed Type of Request"},status.HTTP_405_METHOD_NOT_ALLOWED 


@hr_app.route('/setspecficleave',methods=["POST"])
@roles_accepted('superuser','Hr Admin')
def set_specfic_leave():
    if request.method == "POST":
        try:
            data=dict(SetSpecficLeaveForm().data)
            dbdata=[]
            if db.session.execute(select(EmployeeLeave.id).where(EmployeeLeave.leave_year==int(data['year'])).where(EmployeeLeave.leave_config_id==data['leave_type'].id).\
                where(EmployeeLeave.employee_id == data['employee'].id)).scalar() is None:
                dbdata=[EmployeeLeave(employee_id =data['employee'].id,leave_year=int(data['year']),leave_config_id=data['leave_type'].id,days=data['leave_type'].days )] 
            db.session.add_all(dbdata)
            db.session.commit()
            flash('Sucessfully set leaves')
            return redirect(url_for('hrapp.automation_page'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            flash("Something Unexpected happened, please contact adminstrator if the problem persists")
            return redirect(url_for('hrapp.automation_page'))
    else:
        return { "Message" : "Not Allowed Type of Request"},status.HTTP_405_METHOD_NOT_ALLOWED        
       
@hr_app.route('/deactivateleave',methods=["POST"])
@roles_accepted('superuser','Hr Admin')
def deactivate_leave():
    if request.method == "POST":
        try:
            data=dict(SetLeaveForm().data)
            db.session.execute(update(EmployeeLeave).where(EmployeeLeave.leave_year == int(data['year'])).where(EmployeeLeave.leave_config_id == data['leave_type'].id).values(status=False))
            db.session.commit()
            flash('Sucessfully Updated leaves')
            return redirect(url_for('hrapp.automation_page'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            flash("Something Unexpected happened, please contact adminstrator if the problem persists")
            return redirect(url_for('hrapp.automation_page'))
     

@hr_app.route('/leave/<uid>',methods=["GET","POST","PATCH"])
@login_required
def request_leave_type(uid): 
    user=db.session.execute(select(User).where(User.uid == uid)).scalars().unique().first()
    user_id=user.id
    employee=db.session.execute(select(Employee).where(Employee.user_id == int(user_id)).options(joinedload(Employee.adresses))).scalars().unique().first()
    employee_id=employee.id
    lrequst_form=make_request_form(employee_id)
    if request.method == "GET":
        req_balance=db.session.execute(select(EmployeeLeave).where(EmployeeLeave.employee_id == employee_id).where(EmployeeLeave.status == True)\
            .options(joinedload(EmployeeLeave.leave_name)).options(joinedload(EmployeeLeave.requests))).scalars().unique().all()
        req_balance=[EmployeeLeaveBlanceModel.from_orm(x).dict() for x in req_balance]
        leave_requests=[x for y in req_balance for x in y['requests'] ]
        print(req_balance)
        print([x['requested_days'] for x in leave_requests if x['status'] != "Canceled" ])
        print(sum([x['requested_days'] for x in leave_requests if x['status'] != "Canceled"]))
        print(leave_requests)        
        return render_template('hrm/requestleave.html',uid=uid,user_id=user_id, balance=req_balance,request_form=lrequst_form,\
        name=user.name[0].name, cancel_form=CancelLeaveRequestForm())
    elif request.method == "POST":
        data=dict(lrequst_form.data)
        try:
            if data['year'].balance >=  data['days']:
                dbdata=data
                dbdata.pop('csrf_token')
                dbdata['leave_id']=dbdata['year'].id
                dbdata['requested_days']=dbdata['days']
                dbdata.pop('year')
                dbdata.pop('days')
                db.session.add(LeaveRequest(**dbdata))
                db.session.commit()
                flash('Request sent sucessfully')
                return redirect(url_for('hrapp.request_leave_type',uid=uid))
            else:
                flash('You do not have Sufficent balance')
                return redirect(url_for('hrapp.request_leave_type',uid=uid))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            flash("Something Unexpected happened, please contact adminstrator if the problem persists")
            return redirect(url_for('hrapp.request_leave_type',uid=uid))
        finally:
            db.session.close()
    else:
        return { "Message" : "Not Allowed Type of Request"},status.HTTP_405_METHOD_NOT_ALLOWED 


@hr_app.route('/leaveapprove/<uid>/<lrid>',methods=["POST"])
@login_required
def approve_leave_request(uid,lrid):
    pass

@hr_app.route('/leavedecline/<uid>/<lrid>',methods=["POST",])
@login_required
def decline_leave_request(uid,lrid):
    pass

@hr_app.route('/leavecancel/<uid>/<lrid>',methods=["POST"])
@roles_self()
def cancel_leave_request(uid,lrid):
    from hrm.models import LeaveStatus
    try:
        leave_request=db.session.execute(select(LeaveRequest).where(LeaveRequest.id == lrid)).scalars().unique().first()
        cancel,partial=LeaveStatus('Canceled'),0
        if (datetime.utcnow()- leave_request.start_date).days >=0:
            cancel=LeaveStatus('Partial')
            partial=float((datetime.utcnow()- leave_request.start_date).days)
        db.session.execute(update(LeaveRequest).where(LeaveRequest.id == lrid).values(status=cancel.value,partial=partial)) 
        db.session.commit()
        flash("working fine")
        return redirect(url_for('hrapp.request_leave_type',uid=uid))  
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e),exc_info=True)
        flash("Something Unexpected happened, please contact adminstrator if the problem persists")
        return redirect(url_for('hrapp.request_leave_type',uid=uid))
    finally:
        db.session.close()
  
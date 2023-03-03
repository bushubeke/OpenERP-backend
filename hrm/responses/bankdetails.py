from . import *

@hr_app.route('/bankdetail/<uid>',methods=["GET","POST","DELETE"])
@roles_xor('superuser','Hr Admin')
def bank_details(uid):
    bank_form=BankDetailsForm()
    if request.method == "GET":
        user=db.session.execute(select(User).where(User.uid == uid)).scalars().unique().first()
        user_id=user.id
        employee=db.session.execute(select(Employee).where(Employee.user_id == int(user_id)).options(joinedload(Employee.bank))).scalars().unique().first()
        banks=[BankDetModel.from_orm(x).dict() for x in employee.bank]
        return render_template('hrm/managebanks.html', bank_form=bank_form,uid=uid,user_id=user_id,banks=banks,\
        name=user.name[0].name, delete_form=DeleteBankDetailsForm())
    elif request.method == "POST":
        try:
            if bank_form.validate_on_submit(): 
                data=dict(BankDetailsForm().data)
                data.pop('csrf_token')
                user=db.session.execute(select(User).where(User.uid == uid)).scalars().unique().first()
                user_id=user.id
                employee=db.session.execute(select(Employee).where(Employee.user_id == int(user_id)).options(joinedload(Employee.bank))).scalars().unique().first()
                banks=[BankDetModel.from_orm(x).dict() for x in employee.bank]
                data['employee_id']=employee.id
                data['bank_id']=data['bank_id'].id
                db.session.add(BankDetails(**data))
                db.session.commit()
                flash("creation sucess")
                return redirect(url_for('hrapp.bank_details',uid=uid))
            else:
                flash("Input Validation failed,please provided correct values and try again")
                return redirect(url_for('hrapp.bank_details',uid=uid))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            flash("Something went wrong when updating the Database")
            return redirect(url_for('hrapp.bank_details',uid=uid))
        finally:
            db.session.close()
    elif request.method == "DELETE":
        try:
            data=loads(request.data)
            dt=db.session.execute(delete(BankDetails).where(BankDetails.id==int(data['id'])))
            db.session.commit()
            return { "Message" : "Deleting Object Sucessful"},status.HTTP_202_ACCEPTED
        except Exception as e:
            current_app.logger.error(str(e),exc_info=True)
            db.session.rollback()
            return { "Message" : "Something Unexpected happened"},status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            db.session.close()
    else:
        
        return { "Message" : "Method is not allowed"},status.HTTP_405_METHOD_NOT_ALLOWED
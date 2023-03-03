from . import *

@hr_app.route('/bank',methods=["GET","POST","PATCH","DELETE"])
@roles_accepted('superuser','Hr Admin')
def form_add_view_banks():
    bank_form=BankForm()  
    banks=db.session.execute(select(Banks)) 
    banks=banks.unique().scalars().all()
    banks=[BanksModel.from_orm(x).dict() for x in banks]
    editbanks=[EditBankForm(**x) for x in banks]
    deletebanks=[DeleteBankForm(**x) for x in banks]
    banks_zip=zip(banks,editbanks,deletebanks)
    if request.method == "GET":
        return render_template('hrm/banks.html', form=bank_form,file_types=banks_zip)
    elif request.method == 'POST':
        try:
            if bank_form.validate_on_submit():
                data=dict(bank_form.data)
                data.pop('csrf_token')
                try:
                    bt=Banks(**data)
                    db.session.add(bt)
                    db.session.commit()
                    flash("Created object sucessfully")
                    return redirect(url_for('hrapp.form_add_view_banks'))
                except Exception as e:
                    flash('Creating object Failed')
                    current_app.logger.error(str(e),exc_info=True)
                    return render_template('hrm/banks.html', form=bank_form,file_types=banks_zip)
            else:
                flash("Validation of form failed or something went wrong")
                return render_template('hrm/banks.html', form=bank_form,file_types=banks_zip)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            flash('Something has happened')
            render_template('hrm/banks.html', form=bank_form,file_types=banks_zip)
        finally:
            db.session.close()
    elif request.method == "PATCH":
        try:
            dataup=loads(request.data)
            if EditBankForm(**dataup).validate():
                dataup.pop('csrf_token')
                try:
                    db.session.execute(update(Banks).where(Banks.id == dataup['id']).values(**dataup))
                    db.session.commit()
                    return { "Message" : "Update Sucessful"},status.HTTP_202_ACCEPTED
                except Exception as e:
                    flash('Updating object Failed')
                    current_app.logger.error(str(e),exc_info=True)
                    return render_template('hrm/banks.html', form=bank_form,file_types=banks_zip)
            else:
                flash("Validation of form failed or something went wrong")
                return render_template('hrm/file_types.html', form=bank_form,file_types=banks_zip)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            return { "Message" : str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            db.session.close()
    elif request.method == "DELETE":
        try:
            datadel=loads(request.data)
            if DeleteBankForm(**datadel).validate():
                try:
                    ftb=db.session.execute(delete(BankDetails).where(BankDetails.bank_id == int(datadel['id'])))
                    ft=db.session.execute(delete(Banks).where(Banks.id == int(datadel['id'])))
                    db.session.commit()
                    return {"Message" : "Entry deleted successfully"},status.HTTP_202_ACCEPTED
                except Exception as e:
                    flash('Removing object Failed')
                    current_app.logger.error(str(e),exc_info=True)
                    return render_template('hrm/banks.html', form=bank_form,file_types=banks_zip)
            else:
                flash("Validation of form failed or something went wrong")
                return render_template('hrm/file_types.html', form=bank_form,file_types=banks_zip)
        except Exception as e:
            current_app.logger.error(str(e),exc_info=True)
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            return { "Message" : str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            
            db.session.close()
    else:
        return { "Message" : "Not Allowed Type of Request"},status.HTTP_405_METHOD_NOT_ALLOWED


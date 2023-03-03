from . import *

@hr_app.route('/filetype',methods=["GET","POST","PATCH","DELETE"])
@roles_accepted('superuser','Hr Admin')
def form_add_view_file_type():
    file_typeform=FileTypeForm()  
    filetypes=db.session.execute(select(HrFileType)) 
    filetypes=filetypes.unique().scalars().all()
    filetypes=[HrFileTypeModelView.from_orm(x).dict() for x in filetypes]
    filetypes_form=[EditFileTypeForm(**x) for x in filetypes]
    deletetypes_form=[DeleteFileTypeForm(**x) for x in filetypes]
    file_typs_zip=zip(filetypes,filetypes_form,deletetypes_form)
    if request.method == "GET":
        return render_template('hrm/file_types.html', form=file_typeform,file_types=file_typs_zip)
    elif request.method == 'POST':
        try:
            if file_typeform.validate_on_submit():
                data=dict(file_typeform.data)
                data.pop('csrf_token')
                ft=HrFileType(**data)
                try:    
                    db.session.add(ft)
                    db.session.commit()
                    flash('Created Object successfully')
                    return redirect(url_for('hrapp.form_add_view_file_type'))
                except Exception as e:
                    flash('Creating object Failed')
                    current_app.logger.error(str(e),exc_info=True)
                    return render_template('hrm/file_types.html', form=file_typeform,file_types=file_typs_zip)
            else:
                flash("Validating form failed or Something went wrong")
                return render_template('hrm/file_types.html', form=file_typeform,file_types=file_typs_zip)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            flash('Something has happened')
            render_template('hrm/file_types.html', form=file_typeform,file_types=file_typs_zip)
        finally:
            db.session.close()
    elif request.method == "PATCH":    
        try:
            dataup=loads(request.data)
            if EditFileTypeForm(**dataup).validate():
                dataup.pop('csrf_token')
                try:
                    db.session.execute(update(HrFileType).where(HrFileType.id == dataup['id']).values(**dataup))
                    db.session.commit()
                    return { "Message" : "Update Sucessful"},status.HTTP_202_ACCEPTED
                except Exception as e:
                    current_app.logger.error(str(e),exc_info=True)
                    return { "Message" : "Update Failed"},status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                flash("Validating form failed or something went worng")
                return { "Message" : "data failed to validate"},status.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            return { "Message" : str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            db.session.close()
    elif request.method == "DELETE":
        try:
            datadel=loads(request.data)
            if DeleteFileTypeForm(**datadel).validate():
                try:
                    ft=db.session.execute(delete(HrFileType).where(HrFileType.id == int(datadel['id'])))
                    db.session.commit()
                    return {"Message" : "Entry deleted successfully"},status.HTTP_202_ACCEPTED
                except Exception as e:
                    current_app.logger.error(str(e),exc_info=True)
                    return { "Message" : "Deleting Object Failed"},status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                return { "Message" : "Validating data Failed"},status.HTTP_400_BAD_REQUEST
        except Exception as e:
            current_app.logger.error(str(e),exc_info=True)
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            return { "Message" : str(e)},status.HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            db.session.close()
    else:
        return { "Message" : "Not Allowed Type of Request"},status.HTTP_405_METHOD_NOT_ALLOWED
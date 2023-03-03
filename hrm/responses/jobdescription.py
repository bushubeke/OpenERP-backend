from . import *
from user.models import Role
@hr_app.route('/jobdesc',methods=["GET","POST","PATCH","DELETE"])
def form_add_view_jd():
    jd_form=JobDescriptionForm()
    if request.method == "GET":
        jds=db.session.execute(select(JobDescription).options(joinedload(JobDescription.task_role))).unique().scalars().all()
        jds=[JobDescriptionModel.from_orm(x).dict() for x in jds]
        jdforms=[UpdateJobDescription(**x) for x in jds]
        deletejd=[DeleteJobDescription(**x) for x in jds]
        jd_typs_zip=zip(jds,jdforms,deletejd) 
        return render_template('hrm/jobdescription.html', jd_form=jd_form,jds=jds,jd_typs_zip=jd_typs_zip)
    elif request.method == 'POST':
        try:
            if jd_form.validate_on_submit():
                data=dict(jd_form.data)
                data.pop('csrf_token')
                data['role_id']=data['role_id'].id
                jt=JobDescription(**data)
                try:    
                    db.session.add(jt)
                    db.session.commit()
                    flash('Created Object successfully')
                    return redirect(url_for('hrapp.form_add_view_jd'))
                except Exception as e:
                    flash('Creating object Failed')
                    current_app.logger.error(str(e),exc_info=True)
                    return redirect(url_for('hrapp.form_add_view_jd'))
            else:
                flash("Validating form failed or Something went wrong")
                return redirect(url_for('hrapp.form_add_view_jd')) 
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(str(e),exc_info=True)
            flash('Something has happened')
            return redirect(url_for('hrapp.form_add_view_jd'))
        finally:
            db.session.close()
    elif request.method == "PATCH":    
        try:
            dataup=loads(request.data)
            if UpdateJobDescription(**dataup).validate():
                dataup.pop('csrf_token')
                try:
                    db.session.execute(update(JobDescription).where(JobDescription.id == dataup['id']).values(**dataup))
                    role=db.session.execute(select(Role).where(Role.id == int(dataup['role_id']))).scalars().unique().first().name
                    db.session.commit()
                    return { "Message" : f"{role}"},status.HTTP_202_ACCEPTED
                except Exception as e:
                    flash('Updating object Failed')
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
            if DeleteJobDescription(**datadel).validate():
                try:
                    ft=db.session.execute(delete(JobDescription).where(JobDescription.id == int(datadel['id'])))
                    db.session.commit()
                    return {"Message" : "Entry deleted successfully"},status.HTTP_202_ACCEPTED
                except Exception as e:
                    flash('Removing object Failed')
                    current_app.logger.error(str(e),exc_info=True)
                    return { "Message" : "Deleting Object Failed"},status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                flash("Validating form failed or something went worng")
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
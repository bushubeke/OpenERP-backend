import fitz
from . import *
from utils.filestoring import FileStore

@hr_app.route('/docops/<uid>',methods=["GET","POST","DELETE"])
@roles_xor('superuser','Hr Admin')
def documents(uid):
    doc_form=AddDocumentsForm()
    if request.method == "GET":
        user=db.session.execute(select(User).where(User.uid == uid)).scalars().unique().first()
        user_id=user.id
        employee=db.session.execute(select(Employee).where(Employee.user_id == int(user_id)).options(joinedload(Employee.user_files))).scalars().unique().first()
        documents=[EmployeeModelAll.from_orm(employee).dict()]
        return render_template('hrm/managedocuments.html', doc_form=doc_form,uid=uid,user_id=user_id,documents=documents,\
        name=user.name[0].name, delete_form=DeleteDocumentsForm())
    elif request.method == "POST": 
    
        data=dict(doc_form.data)
        data.pop('csrf_token')
        data=[data]
        user_id=db.session.execute(select(User).where(User.uid == uid)).scalars().unique().first().id
        employee=db.session.execute(select(Employee).where(Employee.user_id == user_id)).scalars().unique().first()
        docsdir=current_app.config['UPLOAD_FOLDER']+'/'+employee.name+'/'
        fs=FileStore()
        try: 
            
            check_exists=db.session.execute(select(HrDocuments).where(HrDocuments.employee_id == employee.id).where(HrDocuments.document_type == int(data[0]['document_type'].id) )).scalars().unique().all()
            if len(check_exists) > 0:
                db.session.execute(delete(HrDocuments).where(HrDocuments.employee_id == employee.id).where(HrDocuments.document_type == int(data[0]['document_type'].id) ))
            
            datapic=[ (docsdir+val['document_type'].name+'/',val['document_file'],val['document_type'],\
                secure_filename(f"{val['document_type']}_+{str(current_user.serialized['uid'])+'_'+str(randint(1,1000000))}")) \
                for val in data if val['document_file'].filename.rsplit('.', 1)[1].lower() != "pdf"]
            dbdatapic=[HrDocuments(file_name=docsdir+x[2].name+"/"+x[3]+".jpg",employee_id=employee.id,document_type=x[2].id) for x in datapic]
             
            #pdf data
            datapdf=[ (docsdir+val['document_type'].name+'/',val['document_file'],val['document_type'],\
                secure_filename(f"{val['document_type']}_+{str(current_user.serialized['uid'])+'_'+str(randint(1,1000000))}")) \
                for val in data if val['document_file'].filename.rsplit('.', 1)[1].lower() == "pdf"]
            
            dbdatapdf=[]
            for x in datapdf:
                if not os.path.exists(x[0]):
                    os.makedirs(x[0])
                x[1].save(x[0]+x[3])
                for i in range(len(fitz.open(x[0]+x[3]))): 
                    dbdatapdf.append(HrDocuments(file_name=docsdir+x[2].name+"/"+x[3]+f'-{i}.jpg',employee_id=employee.id,document_type=x[2].id))
            
            db.session.add_all(dbdatapic+dbdatapdf)
            db.session.commit()
            for x in datapic:
                fs.store_pic(x[0],x[1],x[3])
            for x in datapdf:
                fs.store_file(x[0],x[3])  
            
            flash("succesfull file update")
            return redirect(url_for('hrapp.documents',uid=uid))
        except Exception as e:
            fs.clean_pdf()
            fs.clean_pic()
            current_app.logger.error(str(e),exc_info=True)
            db.session.rollback()
            flash("Documents Update didnot complete successfully, please try again")
            return redirect(url_for('hrapp.documents',uid=uid))
        finally:
            db.session.close()
    elif request.method == "DELETE":
        try:
            data=loads(request.data)
            document_type=db.session.execute(select(HrFileType).where(HrFileType.name == data['document_type'])).scalars().unique().first().id
            dt=db.session.execute(delete(HrDocuments).where(HrDocuments.employee_id ==int(data['employee_id'])).where(HrDocuments.document_type == document_type))
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
                


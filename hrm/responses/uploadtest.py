from . import *

@hr_app.route('/testup',methods=["GET","POST"])
def uploadtest():
    test_up=TestUploadForm()
    if request.method == "GET":
        return render_template('hrm/test.html' ,form=test_up)
    elif request.method == "POST":
        pict=test_up.data['picture']['document_file']
        resid=test_up.data['resident']['document_file']
        # print(test_up.data['picture']['document_file'].headers)
        print(f"#####->{test_up.data['picture']['document_file'].content_length}")
        # print(dir(test_up.data['picture']['document_file']))
        pict_name=f"{os.path.join(current_app.config['UPLOAD_FOLDER'])}/pictures/{secure_filename('picture_'+str(current_user.serialized['uid'])+'_'+str(randint(1,1000000)))}"
        resid_name=f"{os.path.join(current_app.config['UPLOAD_FOLDER'])}/ids/{secure_filename('picture_'+str(current_user.serialized['uid'])+'_'+str(randint(1,1000000)))}"
        save_photo(pict,pict_name)
        save_multiple_pdf(resid,resid_name)        
        flash('Hey it worked')
        return render_template('hrm/test.html' ,form=test_up)
    else:
        flash("Request Method not Allowed")
        redirect(url_for('hrapp.uploadtest'))
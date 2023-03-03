from . import *
# from xsendfile import XSendfileApplication
# DOCUMENT_SENDING_APP = XSendfileApplication("/home/bushu/Documents/Enviroments/evasuehr/documents")

@hr_app.route('/uploads/<uid>/<name>')
@roles_xor('superuser')
def downloaded(uid,name):
   
    path_name=name.replace('@', '/')
    return send_file(path_name)


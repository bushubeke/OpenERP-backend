from . import *


@hr_app.route('/emailtest')
def send_mail():
    try:
        msg = Message('Hello from the other side!', sender = 'beimnetdegefu@aol.com', recipients = ['beimnet.degefu@gmail.com'])
        msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
        mail.send(msg)
        
        return {"message" : "Hey it worked"},status.HTTP_202_ACCEPTED
    except:
      
        return {"message" : "Hey it failed"},status.HTTP_500_INTERNAL_SERVER_ERROR
from flask_mail import Mail, Message

mail = Mail()

def init_mail(app):
    mail.init_app(app)


def send_approval_email(to_email: str, name: str):
    msg = Message(
        subject='Happy Hour Submission Approved',
        recipients=[to_email]
    )
    msg.body = f"Hi {name},\n\nYour happy hour submission has been approved and is now live!"
    mail.send(msg)


def send_rejection_email(to_email: str, name: str):
    msg = Message(
        subject='Happy Hour Submission Rejected',
        recipients=[to_email]
    )
    msg.body = f"Hi {name},\n\nWe're sorry, but your happy hour submission was not approved."
    mail.send(msg)

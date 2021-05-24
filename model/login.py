from model import db
import datetime

class Member(db.Model):
    __tablename__ = 'Member'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    # order_id = db.Column(db.Integer, autoincrement=True)
    # db_Member = db.relationship("Order", backref="Member")

db.create_all()


successful = {
        'ok':True
	}

def sign_Up(name, email, password):
    email_error = {
    'error':True,
    'message':'此Email已註冊'
    }
    space_error ={
        'error':True,
        'message':'欄位不得為空'
    }
    
    check_member = Member.query.filter_by(email=email).first()
    if name and email and password is not None:
        if check_member is not None:
            return email_error
        else:
            member_data = Member(name=name,email = email,password= password)
            db.session.add(member_data)
            db.session.commit()
            db.session.close()
            return successful
    else:
        return space_error
        
    
        


def sign_In(email, password):
    member_error = {
        'error':True,
        'message':'本次登入失敗'
    }
    
    check_login = Member.query.filter_by(email=email,password=password).first()
    if check_login is None:
        return member_error
    else:
        db.session.close()
        return successful
 

    
def get_member(email):
    check_email = Member.query.filter_by(email=email).first()
    if check_email is not None:
        member = {
            'data':{
                'id':check_email.id,
                'name':check_email.name,
                'email':check_email.email,
            }
        }
        db.session.close()
        return member
    else:
        return None
    

def sign_out():
    return successful
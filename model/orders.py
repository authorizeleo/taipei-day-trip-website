from datetime import datetime
from model import db

# class Order(db.Model):
#     __tablename__ = 'Order'
#     Order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     Order_no = db.Column(db.Integer, db.ForeignKey('Member.order_id'))
#     price = db.Column(db.Integer, nullable=False)
#     trip_id = db.Column(db.Integer, nullable=False)
#     trip_name = db.Column(db.String(50), nullable=False)
#     trip_address = db.Column(db.Text)
#     trip_image = db.Column(db.Text)
#     trip_date = db.Column(db.DateTime, nullable=False)
#     trip_time = db.Column(db.String(50), nullable=False)
#     status = db.Column(db.Integer,nullable=False)

# db.create_all()

def get_order_info(prime, name, email, phone, new_trip):
    orders_info = {
    "prime": prime,
    'order': {
        'price': new_trip['price'],
        "trip": {
            'attraction':new_trip['attraction']
        },
        'date': new_trip['date'],
        'time': new_trip['time']
    },
    'contact':{
        'name':name,
        'email':email,
        'phone':phone
    }
}

    return orders_info   
    
def successful_order(status):
    time = datetime.now()
    # Order_data = Order(name=name,email = email,password= password)
    # db.session.add(Order_data)
    # db.session.commit()
    # db.session.close()
    successful= {
        'data':{
            'number': time.strftime('%Y'"%m"'%d''%f'),
            'payment':{
                'status':status,
                'message':'付款成功'
            }
        }
    }
    return successful

def last_thank_you(number, check_data):
    copy_data = check_data.copy()
    thank_you = {
            "price": copy_data['order']['price'],
            "number": number,
            "status": 1
    }
    del copy_data['order']['price']
    copy_data.update(thank_you)
    last_data = {
        'data':copy_data
    }
    return last_data
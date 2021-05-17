from model.attraction import *

def new_travel(id, date, time, price):
    new_booking = {
        'attractionId':id,
        'date':date,
        'time':time,
        'price':price
    }
    return new_booking

def cancel_travel():
    cancel_ok = { 'ok':True}
    return cancel_ok

def get_travel(id, date, time):
    data = search_attraction_Id(id)['data'][0]
    name = data['name']
    address = data['address']
    image = data['images'][0]
    if time == 'afternoon' :
        price = 2500
    else:
        price = 2000
    get_booking = {
        'attraction':{
            'id':id,
            'name':name,
            'address':address,
            'image':image
        },
        'date':date,
        'time':time,
        'price':price
    }
    return get_booking



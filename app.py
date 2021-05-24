from flask import *
import requests
from model import app
from model.attraction import *
from model.login import *
from model.booking import *
from model.orders import *
import json


app.config.from_object('config')
init_table() 

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


sever_error = {
		"error":True,
		"message":"伺服器內部錯誤"
	}

@app.route('/api/attractions')
def taipei_api():
	page_id = int(request.args['page'])
	if 'keyword' in request.args:
		keyword = request.args['keyword']
		search_result = keyword_search(keyword, page_id)
		return jsonify(search_result)
	elif 'page' in request.args:
		return jsonify(search_page(page_id))
	else:
		return jsonify(sever_error)
	
	
@app.route('/api/attraction/<int:attractionId>')
def show_attraction(attractionId):
	if attractionId < 1 or attractionId > 319:
		id_error ={
			"error":True,
			"message":"id不在範圍內"
		}
		return jsonify(id_error)
	return jsonify(search_attraction_Id(attractionId))


@app.route('/api/user', methods=['GET','POST','PATCH','DELETE'])
def sign_api_up():
	if request.method == 'POST':
		try:
			data = request.get_json()
			name = data['name']
			email = data['email']
			password = data['password']
			return jsonify(sign_Up(name, email, password))
		except:
			return jsonify(sever_error)
	if request.method == 'PATCH':
		try:
			data = request.get_json()
			email = data['email']
			password = data['password']
			data_json = jsonify(sign_In(email, password)) 
			session['email'] = email
			return data_json
		except:
			session.pop('email', None)
			return jsonify(sever_error)
	if request.method == 'DELETE':
		session.pop('email', None)
		return jsonify(sign_out())
	if request.method == 'GET':
		email = session.get('email')
		if email:
			return jsonify(get_member(email))
		else :
			return jsonify(sever_error)

@app.route('/api/booking', methods=['GET','POST','DELETE'])
def bookings():
	email = session.get('email')
	if email:
		if request.method == 'POST':	
			data = request.get_json()
			B_id =data['attractionId']
			B_date = data['date']
			B_time = data['time']
			B_price = data['price']
			session['date'] = B_date
			session['time'] = B_time
			session['id'] = B_id
			return jsonify(new_travel(B_id, B_date, B_time, B_price))
		if request.method == 'DELETE':
			session.pop('id', None)
			session.pop('date', None)
			session.pop('time', None)
			return jsonify(cancel_travel())
		if request.method == 'GET' :
			B_id = session.get('id')
			B_date = session.get('date')
			B_time = session.get('time')
			if B_id:
				return jsonify(get_travel(B_id, B_date, B_time))
			else:
				return jsonify(sever_error)
	else:
		login_error ={
			"login_error": True,
		}
		return jsonify(login_error)
	


@app.route('/api/orders', methods=['POST'])
def orders():
	email = session.get('email')
	if email:
		data = request.get_json()
		prime = data['card']
		name = data['name']
		email = data['email']
		phone = data['phone']
		if len(name) and len(email) and len(phone) != 0:
			B_id = session.get('id')
			B_date = session.get('date')
			B_time = session.get('time')
			trip = get_travel(B_id, B_date, B_time)
			order_info = get_order_info(prime, name, email, phone, trip)
			url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
			payload = {
				"partner_key":'partner_aZcyTJgv4q9y0g1ebtdzPmTUQk4vZYgml4SlbD1TDfPO1r94qkVKOiDQ',
				"prime": prime,
				"merchant_id": "skyto122010_CTBC",
				"amount": order_info['order']['price'],
				"currency": "TWD",
				"details": order_info['order']['trip']['attraction']['name'],
				"cardholder": {
					"phone_number": order_info['contact']['phone'],
					"name": order_info['contact']['name'],
					"email": order_info['contact']['email']
				},
			}

			headers = {
				'content-type': 'application/json',
				'x-api-key': 'partner_aZcyTJgv4q9y0g1ebtdzPmTUQk4vZYgml4SlbD1TDfPO1r94qkVKOiDQ'
			}
			input_order_info = requests.post(url, data=json.dumps(payload), headers=headers)
			get_order_data = json.loads(input_order_info.text)
			status = get_order_data['status']
			number = get_order_data['bank_transaction_id']
			if status == 0:
				session['data'] = order_info
				session['number'] = number
				return jsonify(successful_order(number))
			else :
				return jsonify(lose_result(number))
		else:
			input_error ={
				'error':True,
				'message':'資料不得為空'
			}
			return input_error
	else:
		login_error ={
			"login_error": True,
		}
		return jsonify(login_error)


@app.route('/api/order/<orderNumber>')
def order_get_self_data(orderNumber):
	email = session.get('email')
	number = session.get('number')
	data  = session.get('data')
	if email:
		url = "https://sandbox.tappaysdk.com/tpc/transaction/query"
		payload = {
			"partner_key": "partner_aZcyTJgv4q9y0g1ebtdzPmTUQk4vZYgml4SlbD1TDfPO1r94qkVKOiDQ",
			"filters":{
				"bank_transaction_id":orderNumber
			}
		}
		headers = {
			'content-type': 'application/json',
			'x-api-key': 'partner_aZcyTJgv4q9y0g1ebtdzPmTUQk4vZYgml4SlbD1TDfPO1r94qkVKOiDQ'
		}

		find_order = requests.post(url, data=json.dumps(payload),headers=headers)
		find_data = json.loads(find_order.text)
		find_result = find_data['trade_records'][0]['record_status']
		return jsonify(last_thank_you(number, data, find_result))
	else:
		login_error ={
			"login_error": True,
		}
		return jsonify(login_error)




if __name__ == '__main__':
	# app.run(port=3001,debug=True)
	app.run(host="0.0.0.0",port=3000)

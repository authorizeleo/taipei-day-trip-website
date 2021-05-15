from flask import *
from model import app
from model.attraction import *
from model.login import *


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


if __name__ == '__main__':
	# app.run(port=3001,debug=True)
	app.run(host="0.0.0.0",port=3000)

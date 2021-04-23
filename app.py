from flask import *
from data.data import search_page, keyword_search, search_attraction_Id

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

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

@app.route('/api/attractions')
def taipei_api():
	sever_error = {
		"error":True,
		"message":"伺服器內部錯誤"
	}
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


	


if __name__ == '__main__':
	# app.run(port=3000,debug=True)
	app.run(host="0.0.0.0",port=3000)

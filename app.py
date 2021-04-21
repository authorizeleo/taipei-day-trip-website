from flask import *
import sys,os
from data.data import search_page, keyword_search, search_attraction_Id
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
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
	page_id = request.args['page']
	if 'page' and 'keyword' in request.args:
		keyword = request.args['keyword']
		return jsonify(keyword_search(keyword,page_id))
	elif 'page' in request.args:
		return jsonify(search_page(page_id))
	else:
		return jsonify(sever_error)
	
	
@app.route('/api/attraction/<int:attractionId>')
def show_attraction(attractionId):
	return jsonify(search_attraction_Id(attractionId))


	


if __name__ == '__main__':
	# app.run(port=3000,debug=True)
	app.run(host="0.0.0.0",port=3000)

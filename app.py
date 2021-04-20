from flask import *
from data.data import search_page, keyword_search
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

<<<<<<< HEAD
@app.route('/api/attractions')
def taipei_api():

	sever_error = {
		"error":True,
		"message":"伺服器內部錯誤"
	}
	
	if 'page' in request.args:
		page_id = request.args['page']
		return jsonify(search_page(page_id))
	if 'keyword' in request.args:
		keyword = request.args['keyword']
		return jsonify(keyword_search(keyword))
	else:
		return jsonify(sever_error)
	
	
	


if __name__ == '__main__':
	app.run(port=3000, debug=True)
=======
app.run(port=3000)
>>>>>>> 82e1ba0e47ff67b58611ad289baa89f34629bc9c

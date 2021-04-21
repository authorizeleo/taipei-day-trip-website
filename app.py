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
	filter_error ={
		"error":True,
		"message":"查無此資料"
	}
	filter_data = []
	data_box = []
	count = 0
	page_id = int(request.args['page'])
	if 'keyword' in request.args:
		keyword = request.args['keyword']
		search_result = keyword_search(keyword)
		if (len(search_result) == 0):
			return jsonify(filter_error)

		for data in search_result:
			data_box.append(data) 
			count += 1
			if(count / 12 == 1):
				filter_data.append(data_box[-12:])
		if(count % 12 != 0):
			filter_data.append(data_box[-(len(data_box) % 12):])

		for i in range(0, len(filter_data)):
			if page_id == i:
				for x in range(0, len(filter_data[i])):
					if page_id == len(filter_data)-1:
						filter_data[i][x]['nextPage'] = None
					else:
						filter_data[i][x]['nextPage'] = page_id+1
				return jsonify(filter_data[i])
			elif page_id > (len(filter_data)-1):
				return jsonify(filter_error)
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

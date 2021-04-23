from .. import db
import json


class Sightseeing(db.Model):
    __tablename__ = 'Sightseeing'
    id = db.Column(db.Integer)
    name = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.Text)
    transport = db.Column(db.Text)
    mrt = db.Column(db.String(255))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    images = db.Column(db.Integer, primary_key=True)
    db_sightseeing_img = db.relationship("Images", backref="Sightseeing")


class Images(db.Model):
    __tablename__ = 'Images'
    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image_no = db.Column(db.Integer, db.ForeignKey('Sightseeing.images'))
    src = db.Column(db.Text)
    

db.drop_all()
db.create_all()

def addTableData(data):
    db.session.add(data)
    db.session.commit()


with open(r"app/models/taipei-attractions.json", encoding="utf-8") as json_file:
    json_data = json.load(json_file)
    json_list = json_data['result']['results']
    for f in json_list:
        Sightseeing_data = Sightseeing(
                            id=f['_id'], 
                            name=f['stitle'], 
                            category=f['CAT2'], 
                            description=f['xbody'],
                            address = f['address'],
                            transport = f['info'],
                            mrt = f["MRT"],
                            latitude = float(f["latitude"]),
                            longitude = float(f["longitude"]),
                            images = f['_id']
                            )
        addTableData(Sightseeing_data)
        imagefile = f['file'].split('http:')
        for img in imagefile[1:]:
            if '.png' or '.jpg' in img.lower():
                if '.mp3' not in img.lower():   
                    if '.flv' not  in img.lower():
                        images_data = Images(
                                        image_no=f['_id'],
                                        src = "http:" + img
                                    )
                        addTableData(images_data)


def create_api_data(result):
    img_box = []
    Sightseeing_img = Images.query.filter_by(image_no=result.images).all()
    for img in Sightseeing_img:
        img_box.append(img.src)
    
    
    taipei_api_data = {
                "nextPage": "",
                "data": [
                    {
                    "id": result.id,
                    "name": result.name,
                    "category": result.category,
                    "description": result.description,
                    "address": result.address,
                    "transport": result.transport,
                    "mrt": result.mrt,
                    "latitude": result.latitude,
                    "longitude": result.longitude,
                    "images":img_box
                    }
                ]
            }  
    return taipei_api_data


def search_page(page_id):
    if int(page_id) > 26 or int(page_id) < 0:
        error = {
            "error":True,
            "message":"沒有此頁數"
        }
        return error
    
    try:
        page_box = []
        page_id = int(page_id) + 1
        max_num = page_id * 12 + 1
        min_num = max_num - 12
        Sightseeing_filter_data = Sightseeing.query.filter(Sightseeing.id.between(min_num,max_num)).all()
        for i in range(0,12):
            data = create_api_data(Sightseeing_filter_data[i])
            if page_id > 26:
                data['nextPage'] = None
            else:
                data['nextPage'] = page_id
            page_box.append(data)
        return page_box
    except:
        return page_box

  
def keyword_search(keyword, page_id):
    page_id = page_id * 12
    filter_box =[]
    Sightseeing_keyword = Sightseeing.query.filter(Sightseeing.name.like('%{}%'.format(keyword))).limit(13).offset(page_id).all()
    if len(Sightseeing_keyword) == 0 :
        error_keyword_page = {
            "error": True,
            "message": '無資料顯示'
        }
        return error_keyword_page
    for r in Sightseeing_keyword[:12]:
        data = create_api_data(r)
        if(len(Sightseeing_keyword) > 12):
            data['nextPage'] = int(page_id / 12) + 1
        else:
            data['nextPage'] = None
        filter_box.append(data)
    return filter_box 


def search_attraction_Id(attraction_Id):
    Sightseeing_id = Sightseeing.query.filter_by(id=attraction_Id).all()
    data = create_api_data(Sightseeing_id[0])
    del data['nextPage'] 
    return data
    









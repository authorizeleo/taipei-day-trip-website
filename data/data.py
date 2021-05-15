from model import db
import json


        


def create_json_data(Sightseeing,Images):
    with open(r"data/taipei-attractions.json", encoding="utf-8") as json_file:
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
        db.session.add(Sightseeing_data)
        imagefile = f['file'].split('http:')
        for img in imagefile[1:]:
            if '.png' or '.jpg' in img.lower():
                if '.mp3' not in img.lower():   
                    if '.flv' not  in img.lower():
                        images_data = Images(
                                        image_no=f['_id'],
                                        src = "http:" + img
                                    )
                        db.session.add(images_data)
        db.session.commit()
                        
                        




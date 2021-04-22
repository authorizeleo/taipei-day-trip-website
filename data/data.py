import json
import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
load_dotenv()

DB_NAME = 'TaipeiTravel'
try:
  cnx = mysql.connector.connect(
        user=os.getenv('CLEARDB_DATABASE_USER'), 
        password=os.getenv('CLEARDB_DATABASE_PASSWORD'), 
        host=os.getenv('CLEARDB_DATABASE_HOST'))

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  print("successfully")


cursor = cnx.cursor()



def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

TABLES = {}
TABLES['sightseeing'] = (
    " CREATE TABLE `sightseeing` ("
    "  `id` int NOT NULL ,"
    "  `name` varchar(50) NOT NULL,"
    "  `category` varchar(50) NOT NULL,"
    "  `description` text NOT NULL,"
    "  `address` varchar(255) NOT NULL,"
    "  `transport` text,"
    "  `mrt` text ,"
    "  `latitude` float NOT NULL,"
    "  `longitude` float NOT NULL,"
    "  `images` int NOT NULL,"
    "  PRIMARY KEY (`id`), UNIQUE KEY `images` (`images`)"
    ") ENGINE=InnoDB")


TABLES['image'] = (
    "CREATE TABLE `image` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `image_no` int NOT NULL,"
    "  `src` varchar(255) NOT NULL UNIQUE,"
    "  PRIMARY KEY (`id`),"
    "  CONSTRAINT `image_test` FOREIGN KEY (`image_no`) "
    "     REFERENCES `sightseeing` (`images`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")



    


for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print('OK')

add_data = ("INSERT IGNORE INTO sightseeing "
               "(id, name, category, description, address, transport, mrt, latitude, longitude, images) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ")

add_image = ("INSERT IGNORE INTO image "
            "(image_no, src) "
            "VALUES (%s, %s)")

with open(r"data/taipei-attractions.json", encoding="utf-8") as json_file:
    json_data = json.load(json_file)
    json_list = json_data['result']['results']
    for f in json_list:
        sightseeing_id = f['_id']
        name = f['stitle']
        category = f['CAT2']
        description = f['xbody']
        address = f['address']
        transport = f['info']
        mrt = f["MRT"]
        latitude = f["latitude"]
        longitude = f["longitude"]
        images = f['_id']
        taipei_data = (sightseeing_id, name, category, description, address, transport, mrt, latitude, longitude, images)
        cursor.execute(add_data, taipei_data)
        cnx.commit()
        imagefile = f['file'].split('http:')
        for img in imagefile[1:]:
            if '.png' or '.jpg' in img.lower():
                if '.mp3' not in img.lower():   
                    if '.flv' not  in img.lower():
                        taipei_image = (sightseeing_id, "http:" + img)
                        cursor.execute(add_image, taipei_image)
                        cnx.commit()

    

   





def search_page(page_id):
    if int(page_id) > 26 or int(page_id) < 0:
        error = {
            "error":True,
            "message":"沒有此頁數"
        }
        return error
    page_box = []
    try:
        page_id = page_id + 1
        max_num = page_id * 12 
        min_num = max_num - 11
        cursor.execute("SELECT * FROM sightseeing  WHERE id BETWEEN {} AND {}".format(min_num, max_num))
        result = cursor.fetchall()
        for i in range(0,12):
            data = create_api_data(result[i])
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
    cursor.execute("SELECT * FROM sightseeing  WHERE name like'%{}%' ORDER BY id LIMIT 13 OFFSET {} ".format(keyword, page_id))
    result = cursor.fetchall()
    if len(result) == 0 :
        error_keyword_page = {
            "error": True,
            "message": '無資料顯示'
        }
        return error_keyword_page
    for r in result[:12]:
        data = create_api_data(r)
        if(len(result) > 12):
            data['nextPage'] = int(page_id / 12) + 1
        else:
            data['nextPage'] = None
        filter_box.append(data)
    return filter_box 
    

def search_attraction_Id(attraction_Id):
    cursor.execute("SELECT * FROM sightseeing  WHERE id ={}".format(attraction_Id))
    result = cursor.fetchall()
    data = create_api_data(result[0])
    del data['nextPage'] 
    return data
    

def create_api_data(result):
    img_box = []
    cursor.execute("SELECT src FROM  image  WHERE  image_no = {}".format(result[0]))
    img_src = cursor.fetchall()
    for img in img_src:
        img_box.append(img[0])
    
    taipei_api_data = {
                "nextPage": "",
                "data": [
                    {
                    "id": result[0],
                    "name": result[1],
                    "category": result[2],
                    "description": result[3],
                    "address": result[4],
                    "transport": result[5],
                    "mrt": result[6],
                    "latitude": result[7],
                    "longitude": result[8],
                    "images":img_box
                    }
                ]
            }  
    return taipei_api_data



print('closing')



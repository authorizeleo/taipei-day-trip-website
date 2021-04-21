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
    "  `page` int NOT NULL,"
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
               "(id, name, category, description, address, transport, mrt, latitude, longitude, images, page) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ")

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
        page = int(images / 12) 
        imagefile = f['file'].split('http://')
        taipei_data = (sightseeing_id, name, category, description, address, transport, mrt, latitude, longitude, images, page)
        cursor.execute(add_data, taipei_data)
        for img in imagefile[1:]:
            if '.png' and '.jpg' in img.lower():
                    taipei_image = (images, "http://" + img)
                    cursor.execute(add_image, taipei_image)
                    cnx.commit()

    

   





def search_page(page_id):
    if int(page_id) > 26:
        error = {
            "error":True,
            "message":"沒有此頁數"
        }
        return error
    page_box = []
    for i in range(0,12):
        cursor.execute("SELECT * FROM sightseeing  WHERE page = {}".format(page_id))
        result = cursor.fetchall()
        page_box.append(create_api_data(result[i]))
    return page_box
        

def keyword_search(keyword):
    try:
        cursor.execute("SELECT * FROM sightseeing  WHERE name ='{}'".format(keyword))
        result = cursor.fetchall()
        return create_api_data(result[0])
    except:
        error = {
            "error":True,
            "message":"關鍵字錯誤"
        }
        return error

def search_attraction_Id(attraction_Id):
    cursor.execute("SELECT * FROM sightseeing  WHERE images ={}".format(attraction_Id))
    result = cursor.fetchall()
    return create_api_data(result[0])
    

def create_api_data(result):
    taipei_api_data = {}
    img_box = []
    cursor.execute("SELECT src FROM  image  WHERE  image_no = {}".format(result[0]))
    img_src = cursor.fetchall()
    for img in img_src:
        img_box.append(img[0])

    
    taipei_api_data = {
                "nextPage": result[-1],
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



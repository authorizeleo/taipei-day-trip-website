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
    "  `id` int NOT NULL AUTO_INCREMENT,"
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
    "  `src` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`id`), KEY `src` (`src`),"
    "  CONSTRAINT `image_test` FOREIGN KEY (`image_no`) "
    "     REFERENCES `sightseeing` (`images`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")


def json_mysql():
    add_data = ("INSERT INTO sightseeing "
               "(name, category, description, address, transport, mrt, latitude, longitude, images, page) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    add_image = ("INSERT IGNORE INTO image "
                "(image_no, src) "
                "VALUES (%s, %s)")

    with open(r"D:\taipei-day-trip-website\data\taipei-attractions.json", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        json_list = json_data['result']['results']
        for f in json_list:
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
            taipei_data = (name, category, description, address, transport, mrt, latitude, longitude, images, page)
            cursor.execute(add_data, taipei_data)
            cnx.commit()
            for img in imagefile[1:]:
                if '.png' and '.jpg' in img.lower():
                    taipei_image = (images, "http://" + img)
                    cursor.execute(add_image, taipei_image)
                    cnx.commit()



for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
        json_mysql()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
            
        else:
            print(err.msg)
    else:
        print("OK")



def search_page(page_id):
    if int(page_id) > 26:
        error = {
            "error":True,
            "message":"沒有此頁數"
        }
        return error
    cursor.execute("SELECT * FROM sightseeing  WHERE page = {}".format(page_id))
    result = cursor.fetchall()
    image_no = str(int(page_id) + 1)
    cursor.execute("SELECT src FROM  image  WHERE  image_no = {}".format(image_no))
    img_src = cursor.fetchall()
    return create_api_data(result, img_src)
        

def keyword_search(keyword):
    try:
        cursor.execute("SELECT * FROM sightseeing  WHERE name ='{}'".format(keyword))
        result = cursor.fetchall()
        cursor.execute("SELECT src FROM  image  WHERE  image_no = {}".format(str(result[0][-2])))
        img_src = cursor.fetchall()
        return create_api_data(result, img_src)
    except:
        error = {
            "error":True,
            "message":"關鍵字錯誤"
        }
        return error
    

def create_api_data(result, img_src):
    taipei_data_table = []
    for row in result: 
        taipei_api_data = {
            "nextPage": row[-1],
            "data": [
                {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "description": row[3],
                "address": row[4],
                "transport": row[5],
                "mrt": row[6],
                "latitude": row[7],
                "longitude": row[8],
                "images":[]
                }
            ]
        }
        for img in img_src: 
            taipei_api_data["data"][0]["images"].append(img[0])
        taipei_data_table.append(taipei_api_data)
    return taipei_data_table



print('closing')

# cursor.close()
# cnx.close()

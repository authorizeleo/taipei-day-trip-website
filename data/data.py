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
        print("OK")




add_data = ("INSERT INTO sightseeing "
               "(name, category, description, address, transport, mrt, latitude, longitude, images) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")


add_image = ("INSERT INTO image "
               "(image_no, src) "
               "VALUES (%s, %s)")

with open("taipei-attractions.json", encoding="utf-8") as json_file:
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
        imagefile = f['file'].split('http://')
        taipei_data = (name, category, description, address, transport, mrt, latitude, longitude, images)
        cursor.execute(add_data, taipei_data)
        for img in imagefile[1:]:
            if '.png' and '.jpg' in img.lower():
                taipei_image = (images, img)
                cursor.execute(add_image, taipei_image)
    

cnx.commit()
print('closing')

cursor.close()
cnx.close()

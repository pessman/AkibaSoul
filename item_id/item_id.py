import requests
import json
import logging

from mysql import connector

import constants

logging.basicConfig(filename='logs/item_id.log', level=logging.DEBUG,
                    format='%(asctime)s -- %(levelname)s: %(message)s')

'''
create db connection based on values defined in constants file
'''

db = connector.connect(
    host='localhost',
    user=constants.ITEM_DB_MYSQL_USER,
    password=constants.ITEM_DB_MYSQL_PASSWORD,
    database='akiba_apps'
)

'''
debugging statements
'''
logging.debug(db)
logging.debug(db.database)

cursor = db.cursor(buffered=True)
cursor_update = db.cursor(buffered=True)

query = ("SELECT item_id_local, jan_id, mfc_id from item")

cursor.execute(query)

'''
loop through all returned values
'''

for item_id_local, jan_id, mfc_id in cursor:
    '''
    if mfc_id is already defined, skip
    '''
    if mfc_id is not None:
        logging.info("skipping item_id_local {}... already exists... {}".format(item_id_local, mfc_id))
        continue

    url = '{}{}'.format(constants.ITEM_DB_URL, jan_id)
    logging.debug(url)

    r = requests.get(url)

    '''
    checking return status code
    api may be returning 200 status for all calls
    '''
    if r.status_code != 200:
        logging.info(r.text)
        continue

    data = json.loads(r.text)

    '''
    parse return data to get id for mfc_id
    '''
    if 'items' in data and 'item' in data['items'] and 'id' in data['items']['item']:
        item_id = data['items']['item']['id']
    else:
        logging.info('no item id returned for {}'.format(item_id_local))
        continue

    '''
    updating db with new mfc_id
    '''
    update = ("UPDATE item SET mfc_id = %s WHERE item_id_local = %s")

    cursor_update.execute(update,(int(item_id), int(item_id_local)))
    db.commit()

db.close()

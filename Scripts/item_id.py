import requests
import json

from mysql import connector

import constants

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
print(db)
print(db.database)

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
        print("skipping item_id_local {}".format(item_id_local))
        continue

    url = '{}{}'.format(constants.ITEM_DB_URL, jan_id)
    print(url)

    r = requests.get(url)

    '''
    checking return status code
    api may be returning 200 status for all calls
    '''
    if r.status_code != 200:
        print(r.text)
        continue

    data = json.loads(r.text)

    '''
    parse return data to get id for mfc_id
    '''
    if 'items' in data and 'item' in data['items'] and 'id' in data['items']['item']:
        item_id = data['items']['item']['id']
    else:
        print('no item id returned for {}'.format(item_id_local))
        continue

    '''
    updating db with new mfc_id
    '''
    update = ("UPDATE item SET mfc_id = %s WHERE item_id_local = %s")

    cursor_update.execute(update,(int(item_id), int(item_id_local)))
    db.commit()

db.close()
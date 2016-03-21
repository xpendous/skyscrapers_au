__author__ = 'viva'

import couchdb

server = couchdb.Server("http://localhost:5984/")
db = server['new_melb_coords']

try:
    db_unique = server['new_melb_coords_unique']
except:
    db_unique = server.create('new_melb_coords_unique')

i = 0


ids = []
for dbid in db:

    i += 1   # number of tweets containing coordinates
    print i

    try:
        if db[dbid]['user']['id'] not in ids:
            ids.append(db[dbid]['user']['id'])
            db_unique.save(db[dbid])
    except:
        pass    # no coordinates attribute

import json
import shapefile
import sys
import utm
import time

from shapely.geometry import Polygon, Point
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from TweetStore import TweetStore

from keys import api_keys

# Twitter API variables
TWEET_NUM = 0
LIMIT_NUM = 180
LIMIT_TIME = 900


city = sys.argv[1]
if city == 'melbourne':
    key = api_keys[0]
if city == 'sydney':
    key = api_keys[1]
if city == 'manhattan':
    key = api_keys[2]
if city == 'chicago':
    key = api_keys[3]

auth = OAuthHandler(key[0], key[1])
auth.set_access_token(key[2], key[3])


# ---- couchdb variables ----------------

USERNAME = 'server'
PASSWORD = 'couchdb'
SERVER_URL = '115.146.85.52'
DBNAME = "original_" + city + "_database"

if (USERNAME == '') or (PASSWORD == ''):
    COUCH_SERVER = 'http://' + SERVER_URL + ':5984/'
else:
    COUCH_SERVER = 'http://' + USERNAME + ':' + PASSWORD + '@' + SERVER_URL + ':5984/'

store = TweetStore(DBNAME, COUCH_SERVER)


# city variables
MELB_CORDS = [144.885028, -37.864643, 144.998765, -37.776202]
SYDN_CORDS = [151.195754, -33.879870, 151.223520, -33.856067]
MANH_CORDS = [-74.023243, 40.700021, -73.951617, 40.768575]
CHCA_CORDS = [-87.646993, 41.867209, -87.612941, 41.905048]
CITY_CORDS = {"melbourne": MELB_CORDS, "sydney": SYDN_CORDS, "manhattan": MANH_CORDS, "chicago": CHCA_CORDS}

# city municipal shape polygons
melbourne_cbd_shp = shapefile.Reader("cbd/melbourne/Melbourne Municipal Boundary.shp")
melbourne_cbd_shapes = melbourne_cbd_shp.shapes()
melbourne_cbd_points = melbourne_cbd_shapes[0].points

chicago_cbd_shp = shapefile.Reader("cbd/chicago/Central_Business_District.shp")
chicago_cbd_shapes = chicago_cbd_shp.shapes()
chicago_cbd_points = chicago_cbd_shapes[0].points

sydney_cbd = [[151.198, -33.878], [151.208, -33.881], [151.217, -33.879], [151.219, -33.875],
              [151.22, -33.868], [151.225, -33.859], [151.215, -33.855], [151.202, -33.859], [151.195, -33.87]]

manhattan = [[-74.018, 40.699], [-74.011, 40.7], [-74.005, 40.702], [-73.996, 40.707], [-73.977, 40.71],
             [-73.967, 40.728], [-73.971, 40.738], [-73.968, 40.745], [-73.963, 40.75], [-73.955, 40.76],
             [-73.97, 40.766], [-73.993, 40.775], [-73.999, 40.769], [-74.006, 40.76], [-74.01, 40.744], 
             [-7.012, 40.736], [-74.014, 40.724], [-74.018, 40.718], [-74.02 , 40.711], [-74.018, 40.703]] 

polys = {"melbourne": Polygon(melbourne_cbd_points), "sydney": Polygon(sydney_cbd),
         "manhattan": Polygon(manhattan), "chicago": Polygon(chicago_cbd_points)}


class Listener(StreamListener):
    def on_data(self, raw_data):

        try:

            global start, TWEET_NUM

            if TWEET_NUM == 0:
                start = time.time()

            item = json.loads(raw_data)
            TWEET_NUM += 1

            if item["geo"]:
                if city in ['melbourne', 'chicago']:
                    point = Point(utm.from_latlon(item["geo"]["coordinates"][0], item["geo"]["coordinates"][1])[0:2])
                else:
                    point = Point(item["geo"]["coordinates"][0], item["geo"]["coordinates"][1])

                if polys[city].contains(point):
                    store.save_tweet(item)
                    print "coordinates in " + city + " CBD, " + "created at: " + item["created_at"] + " coordinates: " + item["geo"]["coordinates"]
                else:
                    print "coordinates not in " + city + " CBD, " + "created at: " + item["created_at"] + " coordinates: " + item["geo"]["coordinates"]
                    pass
            else:
                if city in item["place"]["full_name"].lower():
                    store.save_tweet(item)
                    print "place in " + city + ", created at: " + item["created_at"]
                else:
                    print "place not in " + city
                    pass

            # protection from beyond Twitter API limit
            if TWEET_NUM == LIMIT_NUM:
                cost = time.time() - start
                TWEET_NUM = 0
                print str(LIMIT_NUM) + " tweets cost: " + str(cost) + " seconds"
                if cost < LIMIT_TIME:
                    print "Sleeping..."
                    time.sleep((LIMIT_TIME - cost))
                    print "Awake!"
        except:
            pass

    def on_error(self, status_code):
        print status_code


if __name__ == '__main__':
    while 1:
        try:
            stream = Stream(auth, Listener())
            stream.filter(locations=CITY_CORDS[city], languages=['en'])
        except:
            pass
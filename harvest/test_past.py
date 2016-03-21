import couchdb
import json
import tweepy
import time
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

# inclusive third
ckey = 'D85t75hTnZ9ZdTdPBP87jOsGm'
csecret = '0tNHkyZTzmkAIbhx5IOJtYNyjLLaNVHN78ykuLerEs6Mdbfdr5'
atoken = '3433602493-fq0l1oaUr7UaxpVJ2xxbo3Xf7JQ46evKXei129z'
asecret = 'XXNeBlreeoKSLpTv8vzyILMcOaKfXqoQfgVQgrTxUNpyP'
inclusive_third = [ckey, csecret, atoken, asecret]


# viva
# viva first
ckey = 'eo28slBEz7e1H80iRUZViRF5r'
csecret = 'lQxBtU1SVY2egaaYSAxu2NebWJpzqs6o1PL2ex95P1DqXqZEZ3'
atoken = '3441531793-YqsextJM47sbzLD4zizcLfrb7AQP1wiFZVKPK3o'
asecret = 'nwe4IMdD2qk8tIWB6vsRdMvFnA2GcOl2MyK9WpXjXrlU6'
viva_first = [ckey, csecret, atoken, asecret]

# viva second
ckey = '3d9Lx9I8T77lyyAai50tTq7QH'
csecret = '3hbvZ9fxkxqGDnufd1i0n2nnHMk0i3ks2RN3Z1wJiP0hnqsZYe'
atoken = '3441531793-jym28ucW02aGskiWYhY6ORIteO45niIukNsnp6K'
asecret = 'ZaqbGiuooi0STgdyjhX29BsSYIGUhWWnkfP1Z7nwhljM7'
viva_second = [ckey, csecret, atoken, asecret]

# viva third
ckey = 'GVgjuMGxp6DeYaFiy02wxPPBF'
csecret = 'TNGzJpUMw48QK2zh6Pl794XX2DCNfMsYnWitJT8rzHuHcl5QP8'
atoken = '3441531793-lN5CFcoxvu4shrU9iM02QPQ2FCiKUTDLTCjrPi0'
asecret = 'KKWe3KOHQsUDwCW7sTOmaNAqfmnSrn2epdnQfmpe5Tkft'
viva_third = [ckey, csecret, atoken, asecret]

api_keys = [inclusive_third, viva_first, viva_second, viva_third]

key = api_keys[1]

couch = couchdb.Server('http://127.0.0.1:5984/')
try:
    database = couch['test']
except:
    database = couch.create('test')


class Listener(StreamListener):
    def on_data(self, raw_data):

        item = json.loads(raw_data)
        database.save(item)

    def on_error(self, status_code):
        print status_code


if __name__ == '__main__':
    while 1:
        try:

            print "000"
            auth = OAuthHandler(key[0], key[1])
            auth.set_access_token(key[2], key[3])

            print "111"
            stream = Stream(auth, Listener())
            print "222"
            stream.filter(locations=[-30, -30, 60.951617, 60])
            print "333"
        except:
                pass

'''
    while 1:
        start = time.time()
        for key in api_keys:

            print "000"
            auth = OAuthHandler(key[0], key[1])
            auth.set_access_token(key[2], key[3])

            print "111"
            stream = Stream(auth, Listener())
            print "222"
            stream.filter(locations=[-30, -30, 60.951617, 60])
            print "333"
        duration = time.time() - start
        if duration < 900:
            time.sleep(900 - duration)
'''
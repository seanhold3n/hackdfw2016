import datetime

from bson import SON, ObjectId
from flask import Flask, render_template, request, make_response
import pymongo
from math import sqrt, pi, sin, cos, atan2
from pymongo import MongoClient

client = MongoClient()
db = client.world

app = Flask(__name__)



def distance(v1, v2):
    r = 6378.137
    v2[1] = float(v2[1])
    v2[0] = float(v2[0])
    v1[0] = float(v1[0])
    v1[1] = float(v1[1])
    dlat = (v1[1] - v2[1]) * pi /180
    dlong = (v1[0] - v2[0]) * pi/180
    a = sin(dlat/2) * sin(dlat/2) + cos(v1[1] * pi /180) * cos(v2[1] * pi /180) * sin(dlong/2) * sin(dlong/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = r * c
    print (d)
    return d * 1000

@app.route('/user/<user>', methods=['GET', 'POST'])
def hello_world(user):
    if request.method == 'POST':
        #add post

        #location
        location = [float(request.values['long']),float(request.values['lat'])]

        if not (len(request.values['headline']) == 0 ):
            title = request.values['headline']
            #description
            description = request.values['description']

            post = {"author": user,
                "title": title,
                "text": description,
                "loc": location,
                "date": datetime.datetime.utcnow()}

            db.events.insert_one(post)
        #include name,





        #query = {"loc": SON([("$near", location)])}
        events = db.events.find()

        ids = []
        authors = []
        titles = []
        texts = []
        locs = []
        dates = []
        for event in events:
            if(distance(location, event['loc'] ) <= 30):
                print(event['loc'])
                ids.append(event['_id'])
                authors.append(event['author'])
                titles.append(event['title'])
                texts.append(event['text'])
                locs.append(event['loc'])
                dates.append(event['date'])

        response = make_response(render_template('index.html',user=user, events=events, ids=ids, authors=authors, titles=titles, texts=texts, locs=locs, dates=dates))
        response.set_cookie('long', str(location[0]))
        response.set_cookie('lat', str(location[1]))
        return response
    else:
        #get events near user


        if('long' in request.cookies):
            location = [request.cookies.get('long'), request.cookies.get('lat')]
        else:
            location = [1, 1]

        events = db.events.find()

        ids = []
        authors = []
        titles = []
        texts = []
        locs = []
        dates = []
        for event in events:
            if(distance(location, event['loc'] ) <= 30):
                print(event['loc'])
                ids.append(event['_id'])
                authors.append(event['author'])
                titles.append(event['title'])
                texts.append(event['text'])
                locs.append(event['loc'])
                dates.append(event['date'])

        response = make_response(render_template('index.html',user=user, events=events, ids=ids, authors=authors, titles=titles, texts=texts, locs=locs, dates=dates))
        response.set_cookie('username', user)
        return response

@app.route('/event/<event_id>', methods=['GET', 'POST'])
def get_event(event_id):

    if request.method == 'POST':
        #add comment to event
        user = request.cookies.get('username')
        event_id = request.cookies.get('id')
        event = db.events.find_one({'_id': ObjectId(event_id)})
        #get description
        text = event['text']
        title = event['title']
        #posts = event['posts']

        return render_template('event_chat.html',event_id=event_id, user=user, text=text, title=title)
    else:
        #get event from id
        event = db.events.find_one({'_id': ObjectId(event_id)})
        #get description
        text = event['text']
        title = event['title']
        #get previous comments
        user = request.cookies.get('username')
        response = make_response(render_template('event_chat.html',event_id=event_id, user=user, text=text, title=title))
        response.set_cookie('id', event_id)
        return response


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)

from flask import Flask, request,redirect,url_for
from flask_restx import Api, Resource, fields, marshal
from flask import g, make_response
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import sqlite3
import requests
import time
import os
import webbrowser

DATABASE = 'z5248104.db'
app = Flask(__name__)
api = Api(app, version='1.1', title='TV Show API',
    description='A sample API for Assignment-2 ',
) 
#The function of initializing the database, if the table already exists, the table is not created
def db():
        with app.app_context():       
            g.db=sqlite3.connect(DATABASE)      
            cursor = g.db.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='TVShow'")
            g.db.commit()
            r = cursor.fetchall()
            print(r[0][0])
            if(r[0][0]==0):                       
                cursor.execute("CREATE TABLE TVShow (   id INTEGER PRIMARY KEY   AUTOINCREMENT,    name   TEXT    NOT NULL,    type           CHAR(50),    [last-update]    TEXT,    premiered      TEXT,    [tvmaze-id]      CHAR(50),    language       CHAR(50),    status         CHAR(50),    summary	   TEXT,    officialSite   TEXT,    runtime        INTEGER,    weight      INTEGER,  score        REAL,    rating         REAL,    genres         TEXT,    [schedule-time] TEXT,    [schedule-days] TEXT,    [network-id]   TEXT,    [network-name] TEXT,    [network-country-name]  TEXT,    [network-country-code]  TEXT,    [network-country-timezone]  TEXT	);")
                g.db.close()
            else:
                g.db.close()

countryModel= api.model('countryModel', {
    'name': fields.String(),
    'code': fields.String(),
    'timezone': fields.String()
})       
networkModel= api.model('networkModel', {
    'id': fields.Integer(description='Primary key'),
    'name': fields.String(),
    'country': fields.Nested(countryModel)
})
scheduleModel= api.model('scheduleModel', {
    'time': fields.String(),
    'days': fields.List( fields.String())
})
#Model of TV show details,as request body
tvModel = api.model('TVShowModel', {
    'tvmaze-id': fields.String(),    
    'name': fields.String(example=''),
    'type': fields.String(),        
    'language': fields.String(),
    'genres': fields.List( fields.String(description='Instance IDs')),
    'status': fields.String(),
    'runtime': fields.Integer(),
    'premiered': fields.String(),    
    'officialSite': fields.String(),
    'schedule': fields.Nested(scheduleModel),  
    'rating': fields.Float(),
    'weight': fields.Integer(),
    'network': fields.Nested(networkModel),
    'summary': fields.String(),
    'score': fields.Float()                
})
def connect_db():
    return sqlite3.connect(DATABASE)

#Before sending the request, connect to the database
@app.before_request
def before_request():
    g.db = connect_db()
#After sending the request, close the database
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

#Interface for testing received data
@api.route('/tvtest')
class TvTest(Resource):
    def get(self):
      return  [
    {
        "score": 25.859735,
        "show": {
            "id": 48129,
            "url": "https://www.tvmaze.com/shows/48129/good-girl",
            "name": "Good Girl",
            "type": "Reality",
            "language": "Korean",
            "genres": [],
            "status": "Running",
            "runtime": 90,
            "premiered": "2020-05-14",
            "officialSite": None,
            "schedule": {
                "time": "21:30",
                "days": [
                    "Thursday"
                ]
            },
            "rating": {
                "average": None
            },
            "weight": 76,
            "network": {
                "id": 247,
                "name": "Mnet",
                "country": {
                    "name": "Korea, Republic of",
                    "code": "KR",
                    "timezone": "Asia/Seoul"
                }
            },
            "webChannel": None,
            "externals": {
                "tvrage": None,
                "thetvdb": 381448,
                "imdb": None
            },
            "image": {
                "medium": "https://static.tvmaze.com/uploads/images/medium_portrait/257/643148.jpg",
                "original": "https://static.tvmaze.com/uploads/images/original_untouched/257/643148.jpg"
            },
            "summary": "<p><b>Good Girl </b>will feature some of the best female hip hop and R&amp;B artists around the country, including underground rappers, current idols, and popular artists. These artists will be put on a team together and will complete quests in order to win a prize.</p>",
            "updated": 1595540935,
            "_links": {
                "self": {
                    "href": "https://api.tvmaze.com/shows/48129"
                },
                "previousepisode": {
                    "href": "https://api.tvmaze.com/episodes/1866903"
                }
            }
        }
    },
    {
        "score": 5.3881726,
        "show": {
            "id": 23542,
            "url": "https://www.tvmaze.com/shows/23542/good-girls",
            "name": "Good Girls",
            "type": "Scripted",
            "language": "English",
            "genres": [
                "Drama",
                "Comedy",
                "Crime"
            ],
            "status": "Running",
            "runtime": 60,
            "premiered": "2081-02-26",
            "officialSite": "https://www.nbc.com/good-girls",
            "schedule": {
                "time": "22:00",
                "days": [
                    "Sunday"
                ]
            },
            "rating": {
                "average": 7.4
            },
            "weight": 100,
            "network": {
                "id": 1,
                "name": "NBC",
                "country": {
                    "name": "United States",
                    "code": "US",
                    "timezone": "America/New_York"
                }
            },
            "webChannel": None,
            "dvdCountry": None,
            "externals": {
                "tvrage": None,
                "thetvdb": 328577,
                "imdb": "tt6474378"
            },
            "image": {
                "medium": "https://static.tvmaze.com/uploads/images/medium_portrait/297/744253.jpg",
                "original": "https://static.tvmaze.com/uploads/images/original_untouched/297/744253.jpg"
            },
            "summary": "<p><b>Good Girls</b> follows three \"good girl\" suburban wives and mothers who suddenly find themselves in desperate circumstances and decide to stop playing it safe, and risk everything to take their power back.</p>",
            "updated": 1617116885,
            "_links": {
                "self": {
                    "href": "https://api.tvmaze.com/shows/23542"
                },
                "previousepisode": {
                    "href": "https://api.tvmaze.com/episodes/2043848"
                },
                "nextepisode": {
                    "href": "https://api.tvmaze.com/episodes/2051665"
                }
            }
        }
    },
    {
        "score": 4.508356,
        "show": {
            "id": 9409,
            "url": "https://www.tvmaze.com/shows/9409/binbougami-ga",
            "name": "Binbougami ga!",
            "type": "Animation",
            "language": "Japanese",
            "genres": [
                "Drama",
                "Anime",
                "Fantasy"
            ],
            "status": "Ended",
            "runtime": 25,
            "premiered": "2012-07-05",
            "officialSite": None,
            "schedule": {
                "time": "01:50",
                "days": [
                    "Thursday"
                ]
            },
            "rating": {
                "average": 7.5
            },
            "weight": 0,
            "network": {
                "id": 76,
                "name": "TV Tokyo",
                "country": {
                    "name": "Japan",
                    "code": "JP",
                    "timezone": "Asia/Tokyo"
                }
            },
            "webChannel": None,
            "externals": {
                "tvrage": None,
                "thetvdb": 259644,
                "imdb": "tt2250040"
            },
            "image": {
                "medium": "https://static.tvmaze.com/uploads/images/medium_portrait/33/82742.jpg",
                "original": "https://static.tvmaze.com/uploads/images/original_untouched/33/82742.jpg"
            },
            "summary": "<p>Sakura Ichiko is a 16-year-old girl who leads a charmed life and is blessed with beauty, brains, and health. She has an abundance of \"Happiness Energy\", which can make people happy, but at the cost of absorbing all the Happiness Energy from her surroundings. She has caused the energy balance of the world to become unbalanced and because of this, she becomes the target of a Poverty God named Momiji. Momiji's goal is to remove Ichiko's power of absorbing other people's Happiness Energy and to return all the energy she has taken to its rightful place.</p>",
            "updated": 1604403592,
            "_links": {
                "self": {
                    "href": "https://api.tvmaze.com/shows/9409"
                },
                "previousepisode": {
                    "href": "https://api.tvmaze.com/episodes/506807"
                }
            }
        }
    },
    {
        "score": 4.2331223,
        "show": {
            "id": 2518,
            "url": "https://www.tvmaze.com/shows/2518/good-girls-revolt",
            "name": "Good Girls Revolt",
            "type": "Scripted",
            "language": "English",
            "genres": [
                "Drama"
            ],
            "status": "Ended",
            "runtime": 55,
            "premiered": "2015-11-05",
            "officialSite": "https://www.amazon.com/Good-Girls-Revolt/dp/B017AOY4WS",
            "schedule": {
                "time": "",
                "days": [
                    "Friday"
                ]
            },
            "rating": {
                "average": 8.7
            },
            "weight": 77,
            "network": None,
            "webChannel": {
                "id": 3,
                "name": "Amazon Prime Video",
                "country": None
            },
            "externals": {
                "tvrage": 50025,
                "thetvdb": 315419,
                "imdb": "tt4687892"
            },
            "image": {
                "medium": "https://static.tvmaze.com/uploads/images/medium_portrait/70/175590.jpg",
                "original": "https://static.tvmaze.com/uploads/images/original_untouched/70/175590.jpg"
            },
            "summary": "<p>It was the 1960's - a time of economic boom and social strife. Young women poured into the workplace, but the \"Help Wanted\" ads were segregated by gender and the \"Mad Men\" office culture was rife with sexual stereotyping and discrimination. Lynn Povich was one of the lucky ones, landing a job at Newsweek, renowned for its cutting-edge coverage of civil rights and the \"Swinging Sixties.\" Nora Ephron, Jane Bryant Quinn, Ellen Goodman, and Susan Brownmiller all started there as well. It was a top-notch job - for a girl - at an exciting place. But it was a dead end.</p><p>Women researchers sometimes became reporters, rarely writers, and never editors. Any aspiring female journalist was told, \"If you want to be a writer, go somewhere else.\" On March 16, 1970, the day <i>Newsweek </i>published a cover story on the fledgling feminist movement entitled \"Women in Revolt,\" forty-six Newsweek women charged the magazine with discrimination in hiring and promotion. It was the first female class action lawsuit--the first by women journalists--and it inspired other women in the media to quickly follow suit. Lynn Povich was one of the ringleaders.</p>",
            "updated": 1584051320,
            "_links": {
                "self": {
                    "href": "https://api.tvmaze.com/shows/2518"
                },
                "previousepisode": {
                    "href": "https://api.tvmaze.com/episodes/943037"
                }
            }
        }
    },
    {
        "score": 3.0222058,
        "show": {
            "id": 24900,
            "url": "https://www.tvmaze.com/shows/24900/the-good-buy-girls",
            "name": "The Good Buy Girls",
            "type": "Reality",
            "language": "English",
            "genres": [],
            "status": "Ended",
            "runtime": 30,
            "premiered": "2013-06-05",
            "officialSite": None,
            "schedule": {
                "time": "22:00",
                "days": [
                    "Wednesday"
                ]
            },
            "rating": {
                "average": None
            },
            "weight": 13,
            "network": {
                "id": 80,
                "name": "TLC",
                "country": {
                    "name": "United States",
                    "code": "US",
                    "timezone": "America/New_York"
                }
            },
            "webChannel": None,
            "externals": {
                "tvrage": None,
                "thetvdb": 271286,
                "imdb": "tt2974548"
            },
            "image": {
                "medium": "https://static.tvmaze.com/uploads/images/medium_portrait/96/240277.jpg",
                "original": "https://static.tvmaze.com/uploads/images/original_untouched/96/240277.jpg"
            },
            "summary": "<p>Meet Brook Roberts and Tara Gray. As former pageant girls, these best friends and roommates have taken their competitive skills &amp; spirit from the stage to the TV screen as they look to elevate their home shopping network to the next level.</p>",
            "updated": 1564607332,
            "_links": {
                "self": {
                    "href": "https://api.tvmaze.com/shows/24900"
                },
                "previousepisode": {
                    "href": "https://api.tvmaze.com/episodes/1690081"
                }
            }
        }
    },
    {
        "score": 3.0222058,
        "show": {
            "id": 15082,
            "url": "https://www.tvmaze.com/shows/15082/good-girls-dont",
            "name": "Good Girls Don't",
            "type": "Scripted",
            "language": "English",
            "genres": [
                "Comedy"
            ],
            "status": "Ended",
            "runtime": 30,
            "premiered": "2021-06-04",
            "officialSite": None,
            "schedule": {
                "time": "21:00",
                "days": [
                    "Sunday"
                ]
            },
            "rating": {
                "average": None
            },
            "weight": 0,
            "network": {
                "id": 79,
                "name": "Oxygen",
                "country": {
                    "name": "United States",
                    "code": "US",
                    "timezone": "America/New_York"
                }
            },
            "webChannel": None,
            "dvdCountry": None,
            "externals": {
                "tvrage": 3713,
                "thetvdb": 127281,
                "imdb": "tt0413572"
            },
            "image": None,
            "summary": "<p>When Marjorie suggests heartbroken Jane get \"right back on the horse\" she creates a monster.</p>",
            "updated": 1616002320,
            "_links": {
                "self": {
                    "href": "https://api.tvmaze.com/shows/15082"
                },
                "previousepisode": {
                    "href": "https://api.tvmaze.com/episodes/869691"
                }
            }
        }
    },
    {
        "score": 2.6974049,
        "show": {
            "id": 45052,
            "url": "https://www.tvmaze.com/shows/45052/good-girls-guide-to-kinky-sex",
            "name": "Good Girls' Guide to Kinky Sex",
            "type": "Reality",
            "language": "English",
            "genres": [],
            "status": "Running",
            "runtime": 65,
            "premiered": "2019-11-14",
            "officialSite": "https://www.channel5.com/show/good-girls-guide-to-kinky-sex/",
            "schedule": {
                "time": "22:00",
                "days": [
                    "Thursday"
                ]
            },
            "rating": {
                "average": None
            },
            "weight": 49,
            "network": {
                "id": 135,
                "name": "Channel 5",
                "country": {
                    "name": "United Kingdom",
                    "code": "GB",
                    "timezone": "Europe/London"
                }
            },
            "webChannel": None,
            "externals": {
                "tvrage": None,
                "thetvdb": None,
                "imdb": None
            },
            "image": {
                "medium": "https://static.tvmaze.com/uploads/images/medium_portrait/224/560281.jpg",
                "original": "https://static.tvmaze.com/uploads/images/original_untouched/224/560281.jpg"
            },
            "summary": "<p>Three self-confessed good girls and their partners look for creative ways to improve their sex lives.</p><p>Over the course of six weeks, each couple will attempt 18 kinky sex challenges they have never tried before, from food play and dressing up to vibrators and handcuffs, to see if they will be inspired.</p>",
            "updated": 1607758233,
            "_links": {
                "self": {
                    "href": "https://api.tvmaze.com/shows/45052"
                },
                "previousepisode": {
                    "href": "https://api.tvmaze.com/episodes/1984520"
                }
            }
        }
    }
]

#Q1
@api.route('/tv-shows/import')
@api.doc(params={'name': 'the name of TV Show'})
class ImportTv(Resource):
    def post(self):
        name = request.args.get("name")
        #testurl = "http://127.0.0.1:5000/tvtest"
        url = "http://api.tvmaze.com/search/shows?q=?"+name
        jsondata = requests.get(url).json()
        #testr = requests.get(testurl).json()
        r = requests.get(url).json()
        sqlStr = 'INSERT INTO TVShow (name,type,[last-update],premiered,' \
               '[tvmaze-id],language,status,summary,officialSite,runtime,weight,score,rating,genres,' \
                 '[schedule-time],[schedule-days],[network-id],[network-name],[network-country-name],[network-country-code],[network-country-timezone]) ' \
               'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #tvshowmodel = jsondata['id']['show']
        # Prompt when the result is not found
        if len(r) == 0:
            return "No data found"
        else:
            # Loop to get the latest TV show date, only import the latest show
            latestTvShow = r[0]
            if r[0]['show']['premiered'] is not None:
                tempdate = r[0]['show']['premiered']
            for tvdetails in r:
                if tvdetails['show']['premiered'] is None:
                    tvdetails['show']['premiered']="0"
                if tvdetails['show']['premiered'] > tempdate:
                    latestTvShow = tvdetails
                    tempdate = tvdetails['show']['premiered']
        #Determine whether certain attributes are empty, if it is empty, you need to deal with it
            if latestTvShow['show']['rating'] is None:
                argsTupAttr1=0
            else :
                argsTupAttr1=latestTvShow['show']['rating']['average']
            if latestTvShow['show']['genres'] is None:
                argsTupAttr2=None
            else :
                argsTupAttr2=','.join(latestTvShow['show']['genres'])
            if latestTvShow['show']['schedule'] is None:
                argsTupAttr3=None
                argsTupAttr4=None
            else :
                argsTupAttr3=latestTvShow['show']['schedule']['time']
                argsTupAttr4=','.join(latestTvShow['show']['schedule']['days'])
            if latestTvShow['show']['network'] is None:
                argsTupAttr5=None
                argsTupAttr6=None
                argsTupAttr7=None
                argsTupAttr8=None
                argsTupAttr9=None
            else :
                argsTupAttr5=latestTvShow['show']['network']['id']
                argsTupAttr6=latestTvShow['show']['network']['name']
                argsTupAttr7=latestTvShow['show']['network']['country']['name']
                argsTupAttr8=latestTvShow['show']['network']['country']['code']
                argsTupAttr9=latestTvShow['show']['network']['country']['timezone']

        argsTup = (latestTvShow['show']['name'], latestTvShow['show']['type'], today, latestTvShow['show']['premiered'],
                   latestTvShow['show']['id'], latestTvShow['show']['language'], latestTvShow['show']['status'],
                   latestTvShow['show']['summary'], latestTvShow['show']['officialSite'], latestTvShow['show']['runtime'],
                   latestTvShow['show']['weight'], latestTvShow['score'], argsTupAttr1,
                   argsTupAttr2, argsTupAttr3,argsTupAttr4, argsTupAttr5,
                   argsTupAttr6, argsTupAttr7,argsTupAttr8, argsTupAttr9)
        cursor = g.db.cursor()
        cursor.execute(sqlStr, argsTup)
        g.db.commit()
        selfHref = "http://127.0.0.1:5000/tv-shows/"+str(cursor.lastrowid)
        return {
            "id": cursor.lastrowid,
            "last-update": today,
            "tvmaze-id": latestTvShow['show']['id'],
            "_links": {
                "self": {
                    "href": selfHref
                }
            }
        }

#Q2 Q3 Q4
@api.route('/tv-shows/<int:id>')
@api.doc(params={'id': 'the id of TV Show'})
class RetrieveTv(Resource):
    def get(self, id):
        sqlStr = "select * from TVShow where id='"+str(id)+"'"
        cursor = g.db.cursor()
        cursor.execute(sqlStr)
        g.db.commit()
        r = cursor.fetchall()
        if len(r) == 0:
            return "The data does not exist"
        else:
            return {
                       "tvmaze-id": r[0][5],
                       "id": r[0][0],
                       "last-update": r[0][3],
                       "name": r[0][1],
                       "type": r[0][2],
                       "language": r[0][6],
                       "genres": r[0][14].split(','),
                        "status": r[0][7],
                        "runtime": r[0][10],
                        "premiered": r[0][4],
                        "officialSite": r[0][9],
                        "schedule": {
                            "time": r[0][15],
                            "days": r[0][16].split(',')
                        },
                        "rating": {
                            "average": r[0][13]
                        },
                        "weight": r[0][11],
                        "network": {
                            "id": r[0][17],
                            "name": r[0][18],
                            "country": {
                                "name": r[0][19],
                                "code": r[0][20],
                                "timezone": r[0][21]
                            }
                        },
                        "summary": r[0][8],
                        "score": r[0][12],
                          "_links": {
                            "self": {
                              "href": "http://127.0.0.1:5000/tv-shows/"+str(r[0][0])
                            },
                            "previous": {
                              "href": "http://127.0.0.1:5000/tv-shows/"+str(r[0][0]-1)
                            },
                            "next": {
                              "href": "http://127.0.0.1:5000/tv-shows/"+str(r[0][0]+1)
                            }
                          }
                    }
    def delete(self, id):
        sqlStr = "delete from TVShow where id='" + str(id) + "'"
        cursor = g.db.cursor()
        cursor.execute(sqlStr)
        g.db.commit()
        r = cursor.rowcount
        if r == 0:
            return "The data does not exist"
        else:
            return {
                        "message": "The tv show with id "+str(id)+" was removed from the database!",
                        "id": id
                    }
    @api.expect(tvModel)
    def patch(self, id):
        cursor = g.db.cursor()  
        sqlStr = "select * from TVShow where id='"+str(id)+"'"     
        cursor.execute(sqlStr)
        r = cursor.fetchall()
        if len(r) == 0:
            return "The data does not exist"   

        attributesDict ={}
        sqlStr = "update TVShow  set name = ?,type = ?,premiered = ?,[tvmaze-id] = ?,language = ?,status = ?,summary = ?,officialSite = ?,runtime = ?,weight = ?,score = ?,rating = ?,genres = ?,[schedule-time] = ?,[schedule-days] = ?,[network-id] = ?,[network-name] = ?,[network-country-name] = ?,[network-country-code] = ?,[network-country-timezone] = ?,[last-update] = ? where id= ?"
        #Dynamically generate TV show attribute dictionary
        #Can update the value of any number of attributes，The attribute value that is not given will keep the original data unchanged
        try:    
            for attributes in tvModel.keys():
                if attributes in api.payload.keys():
                    if attributes=='genres':
                        attributesDict[attributes]=','.join(api.payload[attributes])
                    elif attributes=='schedule':   
                        attributesDict['schedule-time'] = api.payload['schedule']['time']
                        attributesDict['schedule-days'] = ','.join(api.payload['schedule']['days'])
                    elif attributes=='network':  
                        attributesDict['network-id'] = api.payload['network']['id']
                        attributesDict['network-name'] = api.payload['network']['name']
                        attributesDict['network-country-name'] = api.payload['network']['country']['name']   
                        attributesDict['network-country-code'] = api.payload['network']['country']['code']
                        attributesDict['network-country-timezone'] = api.payload['network']['country']['timezone']
                    else:                  
                        attributesDict[attributes]=api.payload[attributes]
                else:
                    if attributes=='tvmaze-id':
                        attributesDict[attributes]=r[0][5]
                    elif attributes=='name':
                        attributesDict[attributes]=r[0][1]
                    elif attributes=='type':
                        attributesDict[attributes]=r[0][2]
                    elif attributes=='language':
                        attributesDict[attributes]=r[0][6]
                    elif attributes=='genres':
                        attributesDict[attributes]=r[0][14]
                    elif attributes=='status':
                        attributesDict[attributes]=r[0][7]    
                    elif attributes=='runtime':
                        attributesDict[attributes]=r[0][10]
                    elif attributes=='premiered':
                        attributesDict[attributes]=r[0][4]
                    elif attributes=='officialSite':
                        attributesDict[attributes]=r[0][9]
                    elif attributes=='schedule':
                        attributesDict['schedule-time'] = r[0][15]
                        attributesDict['schedule-days'] = r[0][16] 
                    elif attributes=='rating':
                        attributesDict[attributes]=r[0][13]
                    elif attributes=='weight':
                        attributesDict[attributes]=r[0][11]
                    elif attributes=='network':
                        attributesDict['network-id'] = r[0][17]
                        attributesDict['network-name'] = r[0][18]
                        attributesDict['network-country-name'] = r[0][19]   
                        attributesDict['network-country-code'] = r[0][20]
                        attributesDict['network-country-timezone'] = r[0][21]
                    elif attributes=='summary':
                        attributesDict[attributes]=r[0][8]
                    elif attributes=='score':
                        attributesDict[attributes]=r[0][12]
        except:
            return "Wrong format" ,400
        else:        
            today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            argsTup=(attributesDict['name'],attributesDict['type'],attributesDict['premiered'],attributesDict['tvmaze-id'],attributesDict['language'],attributesDict['status'],attributesDict['summary'],attributesDict['officialSite'],attributesDict['runtime'],attributesDict['weight'],attributesDict['score'],attributesDict['rating'],attributesDict['genres'],attributesDict['schedule-time'],attributesDict['schedule-days'],attributesDict['network-id'],attributesDict['network-name'],attributesDict['network-country-name'],attributesDict['network-country-code'],attributesDict['network-country-timezone'],today,id)        
            cursor.execute(sqlStr, argsTup)
            g.db.commit()
            return  {  
                        "id" : id,  
                        "last-update": today,
                        "_links": {
                            "self": {
                            "href": "http://127.0.0.1:5000/tv-shows/"+str(id)
                            }
                    }
}

#Q5
@api.route('/tv-shows')
@api.doc(params=
        {   
            'order_by': 'Attributes used for sorting',
            'page': 'used for pagination',
            'page_size': 'shows the number of TV shows per page',
            'filter': 'Attributes used for display'
        })
class RetrieveListTv(Resource):
    def get(self):
        filter = request.args.get("filter")
        order_by = request.args.get("order_by")
        page = request.args.get("page")
        page_size = request.args.get("page_size")
        order_byStr=" Order by "
        order_byList=order_by.split(',')
        filter=filter.replace("network","[network-id],[network-name],[network-country-name],[network-country-code],[network-country-timezone]")
        filter=filter.replace("schedule","[schedule-time],[schedule-days]")
        try:
            for index in range(len(order_byList)):
                if order_byList[index][0]=='+':
                    if index+1 == len(order_byList):
                        order_byStr += order_byList[index][1:] + " ASC "
                    else:
                        order_byStr += order_byList[index][1:] + " ASC,"
                elif order_byList[index][0]=='-':
                    if index+1==len(order_byList):                        
                        order_byStr += order_byList[index][1:] + " DESC "
                    else:                        
                        order_byStr += order_byList[index][1:] + " DESC,"
                else :
                    return "Wrong format"
            num= (int(page)-1) * int(page_size)
            page1=str(int(page)+1)
            sqlStr = "select " +filter+" from TVShow " + order_byStr + " limit " + page_size +" offset " + str(num)+ ";"
            cursor = g.db.cursor()
            cursor.execute(sqlStr)
            g.db.commit()
            r = cursor.fetchall()
            print(sqlStr)
            print(r)
            #The data obtained by processing the query is returned as the result
            jsonData = []
            filterList=filter.split(',')
            for row in r:
                result = {}
                for index in range(len(filterList)):
                    result[filterList[index]]=row[index]
                jsonData.append(result)
        except:
            return "Wrong format" 
        else:        
            return {
                "page": page,
                "page-size": page_size,
                "tv-shows":jsonData,
                "_links": {
                    "self": {
                    "href": "http://127.0.0.1:5000/tv-shows?"+"order_by="+order_by+"&"+"page="+page+"&"+"page_size="+page_size+"&"+"filter="+filter
                    },
                    "next": {
                    "href": "http://127.0.0.1:5000/tv-shows?"+"order_by="+order_by+"&"+"page="+page1+"&"+"page_size="+page_size+"&"+"filter="+filter
                    }
      }
            }

#Q6
@api.route('/tv-shows/statistics')
@api.doc(params=
        {   
            'format': 'can be either "json" or "image"',
            'by': 'Statistical reference indicators'
        })
class statisticsTv(Resource):
    def get(self):
        format = request.args.get("format")
        by = request.args.get("by")
        cursor = g.db.cursor()
        cursor.execute("Select count(*) from TVShow;")
        g.db.commit()
        r = cursor.fetchall()
        totalNum=int(r[0][0])        
        yesterday = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-86400))
        cursor.execute("Select count(*) from TVShow where [last-update]>'"+yesterday+"';")
        g.db.commit()
        r = cursor.fetchall()
        updateNum=int(r[0][0])
        if by == "language":
            sqlStr="Select language,count(*) from TVShow group by language;"
        elif by == "status":
            sqlStr="Select status,count(*) from TVShow group by status;"
        elif by == "type":
            sqlStr="Select type,count(*) from TVShow group by type;"
        elif by == "genres":
            sqlStr="Select genres,count(*) from TVShow group by genres;"
        else:
            return "Wrong format"
        
        cursor.execute(sqlStr)
        g.db.commit()
        r = cursor.fetchall()
        if format == "json":
            if by == "genres":
                jsonData={}
                for row in r:
                    for genresSp in row[0].split(','):
                       if genresSp in jsonData.keys():
                           jsonData[genresSp] +=  row[1]/totalNum
                       else:
                           jsonData[genresSp] =   row[1]/totalNum 
                         
                for key in jsonData:                       
                    jsonData[key]='{:.1%}'.format(jsonData[key])                                                                                                                                                                                                                                                                                                                                                                                                            
                return {
                    "total": totalNum,
                    "total-updated": updateNum,
                    "values" : jsonData
                }
            else:
                jsonData={}
                for row in r:
                    jsonData[row[0]]='{:.1%}'.format(row[1]/totalNum)    
                return {
                    "total": totalNum,
                    "total-updated": updateNum,
                    "values" : jsonData
                }
        elif format == "image":           
            if by == "genres":
                try:
                    jsonData={}
                    for row in r:
                        for genresSp in row[0].split(','):
                            if genresSp in jsonData.keys():
                                jsonData[genresSp] +=  row[1]/totalNum
                            else:
                                jsonData[genresSp] =   row[1]/totalNum                                       
                    plt.figure(figsize=(20,20))
                    plt.subplot(211)
                    yDict=[]
                    xDict=[] 
                    ybarDict=[]
                    xbarDict=[]               
                    for row in r:
                        yDict.append(row[1])
                        xDict.append(row[0])
                    for key in jsonData:
                        yDict.append(jsonData[key])
                        xDict.append(key)  
                    plt.title('The statistics of TVShow\nIf the picture does not change, please refresh the page')
                    plt.pie(yDict,labels=xDict,autopct='%1.1f%%',shadow=False,startangle=150)
                    #plt.figure()
                    plt.subplot(212)
                    plt.bar(xDict, yDict,facecolor='blue', label = by)

                    isExists=os.path.exists("static")
                    if not isExists:
                        os.makedirs("static")
                    plt.savefig("static/result.jpg")
                    webbrowser.open("http://127.0.0.1:5000/static/result.jpg")
                    return "Ok,Please visit'http://127.0.0.1:5000/static/result.jpg'"
                except:
                    return "Something wrong"
            else:
                try:
                    plt.figure(figsize=(20,20))
                    yDict=[]
                    xDict=[]                
                    for row in r:
                        yDict.append(row[1])
                        xDict.append(row[0])  
                    plt.title('The statistics of TVShow\nIf the picture does not change, please refresh the page')         
                    #plt.bar(xDict, yDict,facecolor='blue', label = by)   
                    plt.pie(yDict,labels=xDict,autopct='%1.1f%%',shadow=False,startangle=150)             
                    isExists=os.path.exists("static")
                    if not isExists:
                        os.makedirs("static")
                    plt.savefig("static/result.jpg") 
                    webbrowser.open("http://127.0.0.1:5000/static/result.jpg")             
                    return "Ok,Please visit'http://127.0.0.1:5000/static/result.jpg'"  
                except:
                    return "Something wrong"                        
        else:
            return "Wrong format"

if __name__ == '__main__':
    db()
    app.run(debug=True)
    

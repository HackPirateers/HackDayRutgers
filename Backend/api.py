from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from pandas import DataFrame
import os
import io
import numpy
from sklearn.ensemble import RandomForestClassifier
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import json
import requests
import urllib3
from bs4 import BeautifulSoup
import re
import regex_function as rf

train_x = []
for i in range(1, 46):
    file = open("C:/Users/AdityaDellPC/Downloads/hack_day_data/data/cover-letter/cover-letter%s.txt" % (i), "r")
    print(i)
    #print(regex_processing(file.read()))
    train_x.append(rf.regex_processing(file.read()))
print(train_x[44])
train = DataFrame(train_x[:43],columns=['years_exp','company','degree','college','ctc'])
print(train.head())
features = list(train.columns[:4])
print(features)
y = train["ctc"]
X = train[features]

clf = RandomForestClassifier(n_estimators=10)
clf = clf.fit(X, y)
#Testing. Should be within ~$3000 dollars of correct amount.
count = 0
error = []
y = 0
f = 0
for i in range(45):
    # print(clf.predict([train_x[i][:4]])," ",(clf.predict([train_x[i][:4]])-train_x[i][4:])," ",i)
    print(train_x[i][0])
    x = clf.predict([train_x[i][:4]])-train_x[i][4:]
    y = y + train_x[i][0]
    f = f + train_x[i][4]

    if x[0] == 0:
        count = count+1
    elif (i != 29):
        error.append(x)
average_error = sum(error)/len(error)
print(average_error)
average = y/45
print(average)
print(f/45)

print("TEST",clf.predict([[100,4,4,4]]))
# degreeRankings = {'bachelors':1,'masters':2 ,'phd':3,'doctorate':4}
# educationRankings = {'mit':4,'columbia':3 ,'cit':2,'california':1}
# companyRankings = {'accenture' : 3,'ibm' : 2, 'amazon' : 4}
# for i in range(45):
#     train_x[i] = list(map(degreeRankings.get,train_x[i]))
#     train_x[i] = list(map(educationRankings.get,train_x[i]))
#     train_x[i] = list(map(companyRankings.get,train_x[i]))
#
# print(train_x[44])

# API stuff

app = Flask(__name__)
CORS(app)  # <-- CORS is necessary for React.js's Axion to be able to use the methods in the api!
api = Api(app)

notes = {}


class Test(Resource):
    def put(self):
        # Parsing. View docs(https://flask-restful.readthedocs.io/en/latest/) if this isn't what you need.
        # parser.add_argument('list', action='append') lets flask know that list an argument that can hold 2+ pieces of data in this data :
        # put('http://localhost:5000/', data={"list" : ["When was Barack Obama's birthday?", "What is 10 plus 5 equal to?"]}).json()
        # With that, you have one piece of metadata associated with 2 or more peice of data(aka a list) that can be indexed
        # args is the main class here, and since list is the subclass(an arg of class args) of args, we can mention it freely
        # and access it like this : args.list. We can index by doing args.list[index]

        parser = reqparse.RequestParser()
        parser.add_argument('input')
        args = parser.parse_args()
        # print(request.form)
        # print(args.list[0], " ", args.list[1])
        # notes[0] = args.list
        # print("Notes ")


        #http = urllib3.PoolManager()
        # url = 'http://api.glassdoor.com/api/api.htm?t.p=233537&t.k=b3Bt5z7OKJs&userip=0.0.0.0&useragent=&format=json&v=1&action=employers&jobTitle="Data Scientist"&q="IBM"'
        #
        # hdr = {'User-Agent': 'Mozilla/5.0'}
        # req = urllib3.Request(url, headers=hdr)
        # response = urllib2.urlopen(req)
        # # soup = BeautifulSoup(response)
        # hdr = {'User-Agent': 'Mozilla/5.0'}
        data = rf.regex_processing_real(args.input)
        prediction = clf.predict([data])


        # print(requests.get(
        #     'http://api.glassdoor.com/api/api.htm?t.p=233537&t.k=b3Bt5z7OKJs&userip=0.0.0.0&format=json&v=1&action=employers&jobTitle="Data Scientist"&q="IBM"').text)
        z = {'output': {'ctc': str(prediction[0]),'yrs_exp':data[0]}}  # Formatting this is important. If you don't format it right,
        return z  # React won't get anything/ won't be able to index it.


api.add_resource(Test, '/test')

if __name__ == '__main__':
    app.run(debug=True)

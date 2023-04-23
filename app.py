import csv
import json
import os
import requests
import whoosh
from  whoosh.highlight import HtmlFormatter
from  whoosh.highlight import ContextFragmenter

from dotenv import load_dotenv, find_dotenv
from flask import Flask, redirect, render_template, request, url_for, session
from os import getenv
from serpapi import GoogleSearch
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, OrGroup
from whoosh.query import *


ix = open_dir("index")
searcher = ix.searcher()
searcher.fragmenter = ContextFragmenter(maxchars=100, surround=20, charlimit=32768)
searcher.formatter = HtmlFormatter(tagname='b',between='...<br>',classname='match',termclass='',maxclasses=1)
local_results = None
web_results = None

def whoosh_query(query):
# open the index, which stores all the values in the corpus

# build a query parser, so that we can make queries
    or_group = OrGroup.factory(0.9)
    qp = QueryParser("lyrics", schema=ix.schema, group=or_group)

# get user input to make queries
    q = qp.parse(query.lower())

    results = searcher.search(q)

    return results


load_dotenv(find_dotenv())
SERP_KEY = getenv('SERP_KEY')

app = Flask(__name__)

@app.route('/')
def start():
    return redirect(url_for('google_search'))

@app.route('/google',methods=['GET','POST'])
def google_search():
    global web_results

    # if the user prformed a query, parse the results and display
    if request.method == 'POST':
        print('google')
        query = request.form['query']

        params = {
          'engine': 'google',
          'gl':'us',
          'hl':en,
          'q': query,
          'api_key': SERP_KEY
        }

        search = GoogleSearch(params)
        search_results = search.get_dict()
        web_results = search_results['organic_results']

    return render_template('google.html', results=web_results)

@app.route('/whoosh',methods=['GET','POST'])
def whoosh_search():
    
    global local_results

    # if the user performed a query, parse the results and display
    if request.method == 'POST':
        query = request.form['query']
        # Use the Whoosh library to search for the query
        # Return the search results in an HTML template
        local_results = whoosh_query(query)

    return render_template('whoosh.html', results=local_results)

@app.route('/web-display/<num>')
def web_display(num):

    global local_results

    return render_template('lyrics.html',result=local_results[int(num)])

@app.route('/local-display/<num>')
def local_display(num):

    global local_results

    return render_template('lyrics.html',result=local_results[int(num)])

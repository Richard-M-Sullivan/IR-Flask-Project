import os
import csv
import json
import whoosh
import requests

from os import getenv
from flask import Flask, redirect, render_template, request, url_for, session
from dotenv import load_dotenv, find_dotenv
from serpapi import GoogleSearch
from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.fields import *
from whoosh.qparser import QueryParser, OrGroup
from whoosh.highlight import HtmlFormatter, ContextFragmenter


def whoosh_query(query):
# open the index, which stores all the values in the corpus
    ix = open_dir("index")
    searcher = ix.searcher()
    searcher.fragmenter = ContextFragmenter(maxchars=100, surround=20, charlimit=32768)
    searcher.formatter = HtmlFormatter(tagname='b',between='...<br>',classname='match',termclass='',maxclasses=1)

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
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

@app.route('/')
def start():
    session['web_results'] = None
    session['local_query'] = None
    return redirect(url_for('google_search'))

@app.route('/google',methods=['GET','POST'])
def google_search():
    results=None

    # if the user prformed a query, parse the results and display
    if request.method == 'POST':
        query = request.form['query']
        
        if query:
            params = {
              'engine': 'google',
              'gl':'us',
              'hl':'en',
              'q': query,
              'api_key': SERP_KEY
            }

            search = GoogleSearch(params)
            search_results = search.get_dict()
            session['web_results'] = search_results['organic_results']

    if session['web_results']:
        results = session['web_results']

    return render_template('google.html', results=results)

@app.route('/whoosh',methods=['GET','POST'])
def whoosh_search():
    result = None
    # if the user performed a query, parse the results and display
    if request.method == 'POST':
        session['local_query'] = request.form['query']
        # Use the Whoosh library to search for the query
        # Return the search results in an HTML template

    if session['local_query']:
        result = whoosh_query(session['local_query'])

    return render_template('whoosh.html', results=result)

@app.route('/web-display/<num>')
def web_display(num):

    return render_template('lyrics.html',result=whoosh_query(session['local_query'])[int(num)])

@app.route('/local-display/<num>')
def local_display(num):

    return render_template('lyrics.html',result=whoosh_query(session['local_query'])[int(num)])

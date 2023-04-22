from dotenv import load_dotenv, find_dotenv
from flask import Flask, redirect, render_template, request, url_for, session
from os import getenv
from serpapi import GoogleSearch

import json
import requests
import whoosh

load_dotenv(find_dotenv())
SERP_KEY = getenv('SERP_KEY')

app = Flask(__name__)

@app.route('/')
def start():
    return redirect(url_for('google_search'))

@app.route('/google',methods=['GET','POST'])
def google_search():
    results = None

    # if the user prformed a query, parse the results and display
    if request.method == 'POST':
        print('google')
        query = request.args.get('query')

        params = {
          'engine': 'google',
          'gl':'us',
          'hl':en,
          'q': query,
          'api_key': SERP_KEY
        }

        search = GoogleSearch(params)
        search_results = search.get_dict()
        results = search_results['organic_results']

    return render_template('google.html', results=results)

@app.route('/whoosh',methods=['GET','POST'])
def whoosh_search():
    results = None

    # if the user performed a query, parse the results and display
    if request.method == 'POST':
        print('whoosh')
        query = request.args.get('query')
        # Use the Whoosh library to search for the query
        # Return the search results in an HTML template

    return render_template('whoosh.html', results=results)



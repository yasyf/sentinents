from flask import session, request, render_template, jsonify, g, redirect
from app import app, dev

@app.before_request
def preprocess_request():
  pass

@app.after_request
def postprocess_request(response):
  return response

@app.route('/')
def index_view():
  return render_template('index.html')

@app.template_filter('currency')
def currency_filter(val):
  return "${:,.2f}".format(val)

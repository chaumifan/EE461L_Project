from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def landing():
  return render_template('landing.html')

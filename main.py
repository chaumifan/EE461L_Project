from flask import Flask, render_template, json, request

app = Flask(__name__)

global query_list

@app.route('/')
def landing():
	query_list = set()
  	return render_template('landing.html')

@app.route('/signUp')
def signUp():

@app.route('/signUp', methods=['POST'])
def signUp():
	_name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    if _name and _email and _password:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/submit_query')
def submit_query(list):
	recipes = set()
	cursor = connect_db()
	for ingred in list:
		query = “SELECT * “ + ingred + “FROM db”
		cursor.execute(query)
		recipes.add(list(cursor.fetchall()))
	return render_template(‘landing.html’, res=list(recipes))

@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
	_ingredient = request.form['ingredient']
    if _ingredient:
        query_list.add(_ingredient)
    else:
    	# TODO: add error page

@app.route('/submit_query', methods=['POST'])
def submit_query():
	if query_list and len(query_list) > 0:
		submit_query(query_list)
	else:
    	# TODO: add error page
from flask import Flask, render_template, request, redirect
from google.appengine.api import users

app = Flask(__name__)

global query_list

@app.route('/', methods=['GET'])
def landing():
	query_list = set()
  	user = users.get_current_user()
  	return render_template('landing.html', user=user)

@app.route('/create', methods=['GET', 'POST'])
def create():
	user = users.get_current_user()
	if request.method == 'POST':
		# add the recipe to database
		pass
	else:
		if not user:
			return redirect(users.create_login_url(request.url))
		return render_template('create.html', user=user)

@app.context_processor
def utility_processor():
	def login_url():
		return users.create_login_url(request.url)
	def logout_url():
		return users.create_logout_url('/')
	return {'login_url': login_url, 'logout_url': logout_url}

def submit_query(list): 
	recipes = set()
	cursor = connect_db()
	for ingred in list:
		query = "SELECT * " + ingred + "FROM db"
		cursor.execute(query)
		recipes.add(list(cursor.fetchall()))
	return render_template('landing.html', res=list(recipes))

@app.route('/add_ingredient', methods=['POST']) 
def add_ingredient():
	_ingredient = request.form['ingredient']
	query_list.add(_ingredient) if _ingredient else {} #TODO add error page

@app.route('/submit_query', methods=['POST'])
def submit_query():
	submit_query(query_list) if query_list and len(query_list) > 0 else {} #TODO error page 

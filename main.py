from flask import Flask, render_template, request, redirect
from google.appengine.api import users
import database as db

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
		name = request.form['name']
		instructions = request.form['instructions']
		image_link = request.form['image_link']
		ingred_list = request.form.getlist('ingredients[]')
		db.create_recipe(name, instructions, image_link, ingred_list)
		return redirect(url_for("index"))
	else:
		if not user:
			return redirect(users.create_login_url(request.url))
		return render_template('create.html', user=user)

@app.route('/submit_query', methods=['POST'])
def submit_query():
	ingred_list = request.form.getlist('ingredients[]')
	exclude_list = request.form.getlist('exclude[]')
	recipes = db.query_ingredients(ingred_list, exclude_list)
	return render_template('recipes.html', res=recipes)

@app.context_processor
def utility_processor():
	def login_url():
		return users.create_login_url(request.url)
	def logout_url():
		return users.create_logout_url('/')
	return {'login_url': login_url, 'logout_url': logout_url}

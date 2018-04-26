from flask import Flask, render_template, request, redirect, url_for
from google.appengine.api import users
import database as db

app = Flask(__name__)

@app.route('/', methods=['GET'])
def landing():
  	user = users.get_current_user()
  	return render_template('landing.html', user=user)

@app.route('/create', methods=['GET', 'POST'])
def create():
	user = users.get_current_user()
	if not user:
		return redirect(users.create_login_url(request.url))
	if request.method == 'POST':
		name = request.form['name']
		description = request.form['description']
		instructions = request.form['instructions']
		#image_link = request.form['image_link']
		ingred_list = request.form.getlist('ingredients[]')
		if db.create_recipe(name, user, description, instructions, '', ingred_list):
			return 'OK' #Return value doesn't matter
		else:
			return 'Recipe name is not unique! Please change your recipe name.', 400
	else:
		return render_template('create.html', user=user)

@app.route('/submit_query', methods=['POST'])
def submit_query():
	ingred_list = request.form.getlist('ingredients[]')
	exclude_list = request.form.getlist('excludes[]')
	recipes = db.query_ingredients(ingred_list, exclude_list)
	return render_template('recipes.html', res=recipes)

@app.route('/save_ingredients', methods=['POST'])
def save_ingredients():
	user = users.get_current_user()
	if not user:
		return redirect(users.create_login_url(request.url))
	ingred_list = request.form.getlist('ingredients[]')
	exclude_list = request.form.getlist('excludes[]')
	db.save_ingredients_to_user(user, ingred_list, exclude_list)
	return 'OK' #Return value doesn't matter

@app.route('/load_ingredients', methods=['GET'])
def load_ingredients():
	user = users.get_current_user()
	if not user:
		return redirect(users.create_login_url(request.url))
	user_ingred = db.load_ingredients_from_user(user)
	query_params = ''
	if len(user_ingred.ingred_list) + len(user_ingred.exclude_list) > 0:
		query_params = '?ingred_list=' + ','.join(user_ingred.ingred_list) + '&exclude_list=' + ','.join(user_ingred.exclude_list)
	return redirect(url_for('landing') + query_params)

@app.route('/about', methods=['GET'])
def about():
  	user = users.get_current_user()
  	return render_template('about.html', user=user)

@app.context_processor
def utility_processor():
	def login_url():
		return users.create_login_url(request.url)
	def logout_url():
		return users.create_logout_url('/')
	return {'login_url': login_url, 'logout_url': logout_url}

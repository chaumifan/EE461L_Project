from flask import Flask, render_template, request, redirect, url_for, Response
from werkzeug.http import parse_options_header
from google.appengine.api import users
import database as db
import json, sys, os

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
		try:
			name = request.form['name']
			description = request.form['description']
			instructions = request.form['instructions']
			photo = request.files.get('photo')
			ingred_list = request.form.getlist('ingredients[]')

			if db.create_recipe(name, user, description, instructions, photo, ingred_list):
				return 'OK' #Return value doesn't matter
			else:
				return 'Recipe name is not unique! Please change your recipe name.', 400
		except Exception as e:
			return str(e), 400
	else:
		return render_template('create.html', user=user)

@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
	user = users.get_current_user()
	if not user:
		return redirect(users.create_login_url(request.url))
	uploads = db.get_user_uploads(user)
	uploads_string = render_template('recipes.html', res=uploads, user=user)
	return render_template('uploads.html', user=user, uploads=uploads_string)

@app.route('/edit/<recipe_id>', methods=['GET', 'POST'])
def edit(recipe_id):
	user = users.get_current_user()
	if not user:
		return redirect(users.create_login_url(request.url))

	recipe = db.get_recipe(recipe_id)
	if user.email() != recipe.author:
		return "You do not own this recipe!", 400

	if request.method == 'POST':
		name = request.form['name']
		description = request.form['description']
		instructions = request.form['instructions']
		ingred_list = request.form.getlist('ingredients[]')

		if 'photo' in request.files:
			photo = request.files.get('photo')

			if photo.filename == '':
				photo = None
		else:
			photo = None

		if db.edit_recipe(name, user, description, instructions, photo, ingred_list):
			return 'OK' #Return value doesn't matter
		else:
			return 'Recipe does not exist!', 400
	else:
		return render_template('edit.html', user=user, recipe=recipe)

@app.route('/delete/<recipe_id>', methods=['POST'])
def delete(recipe_id):
	user = users.get_current_user()
	if not user:
		return redirect(users.create_login_url(request.url))

	print("\n\nHere!\n\n")

	recipe = db.get_recipe(recipe_id)
	if user.email() != recipe.author:
		return "You do not own this recipe!", 400

	print("\n\nhey!\n\n")

	if db.delete_recipe(recipe_id):
		print("\n\ngood!\n\n")
		return "OK"
	else:
		print("\n\nerror!\n\n")
		return "Error when deleting!"

@app.route("/img/<key>")
def img(key):
	image = db.get_image(key)
	return Response(image.blob, mimetype=image.mimetype)

@app.route('/submit_query', methods=['POST'])
def submit_query():
	user = users.get_current_user()

	ingred_list = request.form.getlist('ingredients[]')
	exclude_list = request.form.getlist('excludes[]')
	recipes = db.query_ingredients(ingred_list, exclude_list)
	recipes = sorted(recipes, key=lambda r: (-r.rating, r.name.lower())) # sort ascending by rating and then name if tied
	return render_template('recipes.html', res=recipes, user=user)

@app.route('/save_ingredients', methods=['POST'])
def save_ingredients():
	user = users.get_current_user()
	if not user:
		return redirect(users.create_login_url(request.url))
	ingred_list = request.form.getlist('ingredients[]')
	exclude_list = request.form.getlist('excludes[]')
	db.save_ingredients_to_user(user, ingred_list, exclude_list)
	return 'OK' #Return value doesn't matter

@app.route('/load_ingredients', methods=['POST'])
def load_ingredients():
	user = users.get_current_user()
	if not user:
		return redirect(users.create_login_url(request.url))
	user_ingred = db.load_ingredients_from_user(user)
	return json.dumps({'ingred_list': user_ingred.ingred_list, 'exclude_list': user_ingred.exclude_list})

@app.route('/about', methods=['GET'])
def about():
  	user = users.get_current_user()
  	return render_template('about.html', user=user)

@app.route('/rate', methods=['POST'])
def rate():
	user = users.get_current_user()
	if not user:
		#return redirect(users.create_login_url(request.url))
                return 'Please log in to rate!', 400

	recipe = db.get_recipe(request.form['recipe'])
	rating = float(request.form['rating'])
	
	if user.email() in recipe.raters:
		return 'You have already rated this item!', 400

	number_of_raters = len(recipe.raters)
	recipe.rating = (recipe.rating*number_of_raters + rating) / (number_of_raters+1)
	recipe.raters.append(user.email())
	db.save_recipe(recipe)

	return str(recipe.rating)

@app.context_processor
def utility_processor():
	def login_url():
		return users.create_login_url(request.url)
	def logout_url():
		return users.create_logout_url('/')
	return {'login_url': login_url, 'logout_url': logout_url}

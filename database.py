from google.appengine.ext import ndb

import sys

def create_recipe(name, user, description, instructions, photo, ingred_list):
	if ndb.Key(Recipe, name).get():
		return False

	image = Image(mimetype=photo.mimetype, blob=photo.stream.read(), id=name)
	image.put()

	recipe = Recipe(
		name=name,
		author=user.email(),
		description=description,
		instructions=instructions,
		image_link='/img/{}'.format(name),
		ingred_list=ingred_list,
		id=name
		)
	recipe.put()
	for ingred in ingred_list:
		q = contains_ingred(ingred)
		#if ingredient exists, link recipe
		if q:
			q.recipe_list.append(name)
		#if not, create new ingredient with initial recipe
		else:
			q = Ingredient(name=ingred, recipe_list=[name], id = ingred)
		q.put()
	return True


def contains_ingred(ingred):
	q = Ingredient.query(Ingredient.name == ingred)
	return q.get()


def query_ingredients(ingred_list, exclude_list):
	if len(ingred_list) == 0 and len(exclude_list) == 0:
		return []

	recipes = set()
	if ingred_list is not None and len(ingred_list) > 0:
		q = Ingredient.query(Ingredient.name.IN(ingred_list))
		include_results = q.fetch()
	else:
		include_results = list()
	if exclude_list is not None and len(exclude_list) > 0:
		p = Ingredient.query(Ingredient.name.IN(exclude_list))
		exclude_results = p.fetch()
	else:
		exclude_results = list()

	for i in include_results:
		recipes.update(i.recipe_list)
	for e in exclude_results:
		recipes.difference_update(e.recipe_list)

	# Loop through the resulting recipes, query the database for these entries, return the list of results
	ret = []
	for r in recipes:
		key = ndb.Key(Recipe, r)
		ret.append(key.get())
	return ret

def save_ingredients_to_user(user, ingred_list, exclude_list):
	u = ndb.Key(UserIngredients, user.email()).get()
	if u:
		u.ingred_list = ingred_list
		u.exclude_list = exclude_list
	else:
		u = UserIngredients(
			user_email = user.email(),
			ingred_list = ingred_list,
			exclude_list = exclude_list,
			id = user.email()
			)
	u.put()

def load_ingredients_from_user(user):
	u = ndb.Key(UserIngredients, user.email()).get()
	if u:
		return u
	else:
		return UserIngredients(
			user_email = user.email(),
			ingred_list = [],
			exclude_list = [],
			id = user.email()
			)

def get_image(recipe_name):
	return ndb.Key(Image, recipe_name).get()

class Recipe(ndb.Model):
	name = ndb.StringProperty()
	author = ndb.StringProperty()
	description=ndb.StringProperty()
	instructions = ndb.StringProperty()
	image_link = ndb.StringProperty()
	ingred_list = ndb.StringProperty(repeated=True)

class Ingredient(ndb.Model):
	name = ndb.StringProperty()
	recipe_list = ndb.StringProperty(repeated=True)

class UserIngredients(ndb.Model):
	user_email = ndb.StringProperty()
	ingred_list = ndb.StringProperty(repeated=True)
	exclude_list = ndb.StringProperty(repeated=True)

class Image(ndb.Model):
	blob = ndb.BlobProperty()
	mimetype = ndb.StringProperty()

from google.appengine.ext import ndb
from google.cloud import datastore


def create_recipe(name, instructions, image_link, ingred_list):
	recipe = Recipe(name = name, instructions = instructions, image_link = image_link, ingred_list = ingred_list, id = name )
	recipe.put()
	for ingred in ingred_list:
		q = contains_ingred(ingred)
		#if ingredient exists, link recipe
		if(q):
			q.recipe_list.append(name)
		#if not, create new ingredient with initial recipe
		else:
			q = Ingredient(name=ingred, recipe_list=[name], id = name)
		q.put()


def contains_ingred(ingred):
	q = Ingredient.query(ingred)
	return q is None;


def query_ingredients(ingred_list, exclude_list):
	recipes = set()
	q = Ingredient.query(Ingredient.name.IN(ingred_list))
	include_results = q.fetch()
	p = Ingredient.query(Ingredient.name.IN(exclude_list))
	exclude_results = p.fetch()
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

def save_ingredients_to_user(user, ingred_list):
	pass

def load_ingredients_from_user(user):
	pass

class Recipe(ndb.Model):
	name = ndb.StringProperty()
	instructions = ndb.StringProperty()
	image_link = ndb.StringProperty()
	ingred_list = ndb.StringProperty(repeated=True)

class Ingredient(ndb.Model):
	name = ndb.StringProperty()
	recipe_list = ndb.StringProperty(repeated=True)
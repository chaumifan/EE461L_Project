from google.appengine.ext import ndb

def create_recipe(name, instructions, image_link, ingred_list):
	recipe = Recipe(
		name=name,
		instructions=instructions,
		image_link=image_link,
		ingred_list=ingred_list,
		id=name
		)
	recipe.put()
	for ingred in ingred_list:
		pass
		# TODO
		# If ingredient is in datastore
			# grab it and then update the ingred_list
		# Else
			# Create new ingredient

def contains_ingred(ingred):
	q = Ingredient.query(Ingredient.name == ingred)
	result = q.fetch()
	return not(result is None) and len(result) > 0;


def query_ingredients(ingred_list, exclude_list):
	if (len(ingred_list) == 0 and len(exclude_list) == 0):
		return None

	recipes = set()
	if not(ingred_list is None) and len(ingred_list) > 0:
		q = Ingredient.query(Ingredient.name.IN(ingred_list))
		include_results = q.fetch()
	else:
		include_results = list()
	if not(exclude_list is None) and len(exclude_list) > 0:
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
import unittest
import sys

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
import database as db

class DatastoreTestCase(unittest.TestCase):
	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		ndb.get_context().clear_cache()

	def tearDown(self):
		self.testbed.deactivate()

	def populate():
		db.create_recipe('rice', 'steam them', 'https://rice.com', list(rice, water, salt))
		db.create_recipe('veggies', 'cook them', 'https://vegies.com', list(veggies, oil))
		db.create_recipe('potatoes', 'fry them', 'https://fries.com', list(potato, salt, pepper, oil))
		db.create_recipe('eggs', 'stir them', 'https://eggs.com', list(eggs, milk))

	#################
	# TEST CONTAINS #
	#################
	def test_contains(self):
		v1 = db.contains_ingred('rice');
		v2 = db.contains_ingred('veggies');
		v3 = db.contains_ingred('eggs');
		v4 = db.contains_ingred('oil');
		v5 = db.contains_ingred('pizza');
		v6 = db.contains_ingred('');
		expected = [True, True, True, True, False, False]
		actual = [v1, v2, v3, v4, v5, v6]
		self.assertListEqual(expected, actual)

	##############
	# TEST QUERY #
	##############
	def test_query_empty(self):
		res = db.query_ingredients(list(), list())
		self.assertEquals(res, None)

	def test_query_simple(self):
		include = ['rice', 'water']
		res = db.query_ingredients(include, list())
		self.assertEquals(len(res), 1)
		# TODO: create recipe obj and test equals

	def test_query_multiple(self):
		include = ['rice, potato']
		res = db.query_ingredients(include, list())
		self.assertEquals(len(res), 2)
		# TODO: create recipe obj and test equals

	def test_query_duplicate(self):
		include = ['oil']
		res = db.query_ingredients(include, list())
		self.assertEquals(len(res), 2)
		# TODO:create recipe obj and test equals

	def test_query_exclude(self):
		include = ['oil']
		exclude = ['potato']
		res = db.query_ingredients(include, exclude)
		self.assertEquals(len(res), 1)
		# TODO:create recipe obj and test equals

	def test_query_all_exclude(self):
		include = ['oil']
		exclude = ['potato', 'veggies', 'salt']
		res = db.query_ingredients(include, exclude)
		self.assertEquals(len(res), 0)
		# TODO:create recipe obj and test equals

	###############
	# TEST CREATE #
	###############

if __name__ == '__main__':
	unittest.main()
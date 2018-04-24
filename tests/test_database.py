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

	def test_contains(self):
		v1 = db.contains_ingred('rice');
		v2 = db.contains_ingred('veggies');
		v3 = db.contains_ingred('eggs');
		v4 = db.contains_ingred('oil');
		v5 = db.contains_ingred('pizza');
		v6 = db.contains_ingred('');
		expected = [True, True, True, True, False, False]
		actual = [v1, v2, v3, v4, v5, v6]
		if expected == actual:
			print "PASSED TEST_CONTAINS"
		else:
			print "FAILED TEST_CONTAINS"


if __name__ == '__main__':
	unittest.main()
import unittest

from google.appengine.api import users
from google.appengine.ext import testbed
from google.appengine.api import memcache
from google.appengine.ext import ndb
from main import app

DEFAULT_EMAIL = 'user@example.com'

class ControllerTest(unittest.TestCase):
	def setUp(self):
		app.config['TESTING'] = True
		self.app = app.test_client()
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_user_stub()
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		ndb.get_context().clear_cache()

	def tearDown(self):
		self.testbed.deactivate()

	def loginUser(self, email=DEFAULT_EMAIL, id='123'):
		self.testbed.setup_env(
			user_email=email,
			user_id=id,
			user_is_admin='0',
			overwrite=True)

	def testLogin(self):
		self.assertFalse(users.get_current_user())
		self.loginUser()
		self.assertEquals(users.get_current_user().email(), DEFAULT_EMAIL)

	def testGetCreate(self):
		self.assertFalse(users.get_current_user())
		result = self.app.get('/create')
		# Redirects to login when trying to load create page with no user
		self.assertEquals(result.status_code, 302)
		self.assertEquals(result.location, 'https://www.google.com/accounts/Login?continue=http%3A//localhost/create')
		self.loginUser()
		result = self.app.get('/create')
		self.assertEquals(result.status_code, 200)

	def testPostCreate(self):
		self.assertFalse(users.get_current_user())
		result = self.app.post('/create', data = {
				'name' : 'Hamburger',
				'description' : 'The American Dream',
				'instructions' : 'https://hamburger.com',
				'image_link' : 'www.google.com',
				'ingredients[]' : ['burger', 'buns']
			})
		self.assertEquals(result.status_code, 302)
		self.assertEquals(result.location, 'https://www.google.com/accounts/Login?continue=http%3A//localhost/create')
		self.loginUser()
		result = self.app.post('/create', data = {
				'name' : 'Hamburger',
				'description' : 'The American Dream',
				'instructions' : 'https://hamburger.com',
				'image_link' : 'www.google.com',
				'ingredients[]' : ['burger', 'buns']
			})
		self.assertEquals(result.status_code, 200)

	def testSaveIngredients(self):
		self.assertFalse(users.get_current_user())
		result = self.app.post('/save_ingredients', data = {
				'ingredients[]' : ['burger', 'buns'],
				'excludes[]' : ['lettuce', 'tomato']
			})
		self.assertEquals(result.status_code, 302)
		self.assertEquals(result.location, 'https://www.google.com/accounts/Login?continue=http%3A//localhost/save_ingredients')
		self.loginUser()
		result = self.app.post('/save_ingredients', data = {
				'ingredients[]' : ['burger', 'buns'],
				'excludes[]' : ['lettuce', 'tomato']
			})
		self.assertEquals(result.status_code, 200)
		self.assertEquals(result.get_data(True), 'OK')

	def testLoadIngredients(self):
		self.assertFalse(users.get_current_user())
		result = self.app.get('/load_ingredients')
		self.assertEquals(result.status_code, 302)
		self.assertEquals(result.location, 'https://www.google.com/accounts/Login?continue=http%3A//localhost/load_ingredients')
		self.loginUser()
		result = self.app.get('/load_ingredients')
		self.assertEquals(result.status_code, 302)
		self.assertEquals(result.location, 'http://localhost/')

	def testSaveAndLoadIngredients(self):
		self.loginUser()
		result = self.app.post('/save_ingredients', data = {
				'ingredients[]' : ['burger', 'buns'],
				'excludes[]' : ['lettuce', 'tomato']
			})
		self.assertEquals(result.status_code, 200)
		self.assertEquals(result.get_data(True), 'OK')
		result = self.app.get('/load_ingredients')
		self.assertEquals(result.status_code, 302)
		self.assertEquals(result.location, 'http://localhost/?ingred_list=burger,buns&exclude_list=lettuce,tomato')
	
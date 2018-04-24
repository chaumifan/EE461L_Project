import unittest

from google.appengine.api import users
from google.appengine.ext import testbed

DEFAULT_EMAIL = 'user@example.com'

class ControllerTest(unittest.TestCase):
	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_user_stub()

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

	
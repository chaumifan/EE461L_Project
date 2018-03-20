from flask import Flask, render_template, request, redirect
from google.appengine.api import users

app = Flask(__name__)

@app.route('/', methods=['GET'])
def landing():
  user = users.get_current_user()
  return render_template('landing.html', user=user)

@app.route('/create', methods=['GET', 'POST'])
def create():
	user = users.get_current_user()
	if request.method == 'POST':
		# add the recipe to database
		pass
	else:
		if not user:
			return redirect(users.create_login_url(request.url))
		return render_template('create.html', user=user)

@app.context_processor
def utility_processor():
	def login_url():
		return users.create_login_url(request.url)
	def logout_url():
		return users.create_logout_url('/')
	return {'login_url': login_url, 'logout_url': logout_url}
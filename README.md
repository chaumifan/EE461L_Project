# EE461L Project

## How to setup and run
In the root directory, setup a virtual environment using the following commands:
```
virtualenv env
source env/bin/activate
pip install -t lib -r requirements.txt
```

To run the server locally, `dev_appserver.py app.yaml`

## How to run Unit Tests
We use the test runner, test.py, to run all the unit tests contained in the test folder. test.py takes in 2 commands, the first is the path to the Google App Engine SDK (make sure to refer to google-cloud-sdk/platform/google_appengine/ and not google-cloud-sdk/bin) and the second argument is the path to the test directory.

Here is how I run it on my machine: ./test.py /mnt/d/Users/cwly1/AppData/Local/Google/Cloud\ SDK/google-cloud-sdk/platform/google_appengine/ tests/

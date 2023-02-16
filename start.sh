gunicorn "app:app"

# This says that when we access this application, we look for the kick-off ("app" folder)for the application
# and then finding the command "app" (the flask app) inside the init.py file
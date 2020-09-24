from flask import Flask
# from flask_session import Session

app = Flask(__name__)
app.secret_key = "a37Sdkfhx@"
# SESSION_TYPE = 'redis'
# app.config.from_object(__name__)
# Session(app)
# app/__init__.py
import os
from flask import Flask
from app.routes import configure_routes
from app.Database.context import DbContext

app = Flask(__name__)
db_path = os.path.join(os.getcwd(), "DB", "DOTERS.db")
DbContext(db_path)
configure_routes(app)

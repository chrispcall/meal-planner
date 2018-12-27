from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename='mealplanner.log', filemode='a', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.debug('Started Mealplanner')

app = Flask(__name__)

login = LoginManager(app)

app.secret_key = "wejkrhwkehrkwjehr,wer323r23r"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)


from app import routes, models, forms, listIngredients, getAllDates, getFavRecipes
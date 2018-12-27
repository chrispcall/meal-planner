from flask import request, render_template, redirect, url_for, flash
from flask.json import jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from werkzeug.urls import url_parse
from app import app
from app.forms import addMeal, LoginForm
from app.models import Post, User, update
from app.getAllDates import get_all_dates
from app.listIngredients import ingredients_from_web
import logging
logger = logging.getLogger(__name__)

# set up Logger so we can fetch favorite recipes
formatter = logging.Formatter('%(message)s')
handler = logging.FileHandler('past_recipes.log')
handler.setFormatter(formatter)
recipe_logger = logging.getLogger('fav_recipes')
recipe_logger.setLevel('INFO')
recipe_logger.addHandler(handler)


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
       logging.debug(f'{request.remote_addr} User "{current_user.username}" is logged in so we are redirecting them to "add_meal_weeks"')
       return redirect(url_for('add_meal_weeks',w=0))
    else:
        logging.debug(f'{request.remote_addr} Client accessed "/" but no user is logged in. Redirecting to "login"')
        return redirect(url_for('login'))


@app.route('/week/<w>', methods=['GET', 'POST'])
# this decorator was here but instead, I'm using a check for 'if current_user.is_authenticated' @login_required
# not sure if this is the best method but when the decorator is here, we get a forbidden message on the client
def add_meal_weeks(w):
    if current_user.is_authenticated:
        form = addMeal(request.form)
        if request.method == 'POST':
            date = request.form['date']
            title = request.form['title']
            ingredients = request.form['ingredients']
            url = request.form['url']
            if "http" in url:
                recipe_logger.info(url)
                parsed_ingredients = ingredients_from_web(url)
                if parsed_ingredients:
                    # only override the user's ingredients if we got some parsed back 
                    ingredients = parsed_ingredients
            notes = request.form['notes']
            logging.debug(f'{request.remote_addr} POSTING to DB: {date} - {title} - {ingredients} - {url} - {notes}')
            update(date, title, ingredients, url, notes)

        return render_template('calendar.html', all_week_dates=get_all_dates(w),
                               days=['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat'],
                               posts=Post.query.all(), w=w, form=form)
    else:
        logging.debug(f'{request.remote_addr} Client accessed "/week/<i>" but no user is logged in. Redirecting to "login"')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        logging.debug(f'User "{current_user.username}" logged in from IP:{request.remote_addr}')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logging.debug(f'User "{current_user.username}" logged out of app')
    logout_user()
    return redirect(url_for('login'))


@app.route('/get_values/<input_date>')
def get_values_in_background(input_date):
    post = Post.query.filter_by(date=input_date).first()
    if post:
        response = jsonify({"date": input_date, "title": post.title, "ingredients": post.ingredients, "url": post.url ,"notes": post.notes})    
    else:
        response = jsonify({"date": input_date, "title": "", "ingredients": "", "url": "", "notes": "", })   
    response.headers.set("Content-Type", "application/octet-stream")
    return response

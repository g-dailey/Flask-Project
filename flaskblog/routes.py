from flask import render_template, redirect, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegisterationForm, LoginForm
from flaskblog.models import User, Post

posts = [
  {
    'author': 'Janie Doe',
    'title': 'Blog Post 1',
    'content': 'Second post content',
    'date_posted': 'Sept-20-2022'
  },
    {
    'author': 'John Doe',
    'title': 'Blog Post 2',
    'content': 'Second post2 content',
    'date_posted': 'Sept-22-2022'
  }
]



@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html', posts=posts)


@app.route("/about")
def about():
  return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
  form = RegisterationForm()
  if form.validate_on_submit():
    flash(f'Account Created for {form.username.data}!', 'success')
    return redirect(url_for('home'))
  # if not form.validate_on_submit():
  #   flash(f'Something was wrong with your account creation, {form.username.data}!')
  return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if form.email.data == 'admin@blog.com' and form.password.data == 'password':
      flash('You have been logged in!', 'success')
      return redirect(url_for('home'))
    else:
      flash('Login Failed, please check username and password', 'danger')
  return render_template('login.html', title='Login', form=form)

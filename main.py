from flask import Flask, render_template, url_for
from forms import RegisterationForm, LoginForm
app = Flask (__name__)

app.config['SECRET_KEY'] = '3459sldcwjeoir2sdflk231'

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


@app.route("/register")
def register():
  form = RegisterationForm()
  return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
  form = LoginForm()
  return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
  app.run(debug=True)

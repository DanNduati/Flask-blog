from flask import Flask, render_template,url_for,flash,redirect
from forms import RegistrationForm,LoginForm
app = Flask(__name__)
#csrf
app.config['SECRET_KEY'] = '9a3cc8feaddaf1f84c1900967581d0ad'
#pseudo posts for views tests 
posts = [
    {
        'author':'Daniel',
        'title':'Blog post 1',
        'content':'First blogpost go brr',
        'date_posted':'July 6, 2021'
    },
    {
        'author':'Chege',
        'title':'Blog post test',
        'content':'First blogpost test',
        'date_posted':'July 5, 2021'
    },
    {
        'author':'Nduati',
        'title':'Blog post',
        'content':'What to write',
        'date_posted':'July 4, 2021'
    }
]
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title ='About')
 
@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Successfully logged in!','success')
        return redirect(url_for('home'))
    return render_template('login.html',title='login',form=form)

if __name__ == '__main__':
    app.run(debug=True)
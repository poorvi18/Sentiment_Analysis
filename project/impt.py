from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm ,sentimentform ,PostForm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    '''image_file = db.Column(db.String(20), nullable=False, default='default.jpg')'''
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


'''posts = [
    {
        'author': 'XYZ - Consultant',
        'title': 'Talk_Place',
        'content': 'Many people know TalkSpace as a source for online therapy. They work to make it more accessible and affordable for people to get mental health treatment. They also have a blog with resources on specific issues. Their posts on depression cover everything from applying to jobs while depressed, to how a breast cancer diagnosis might affect your mental health, to parenting with depression. The blog is a great resource for anyone who wants to learn more about mental health, whether they have a diagnosis or not, including those who are supporting someone else with mental illness. It can also be helpful for medical providers, caregivers, and other support workers.',
        'date_posted': 'Oct 3, 2020'
    },
    {
        'author': 'Dane ',
        'title': 'Depression can effect anyone,there is not always a reason! ',
        'content': 'My story? Well, I only realised that I had symptoms of clinical depression recently. And probably that I have had it a lot longer than I thought. I was always of the belief that depression was a result of a traumatic event, a loss, stress, unhappiness at home, being bullied, those types of things. But it turns out you can just have bad brain chemistry. My brain just doesnot produce enough serotonin.',
        'date_posted': 'October 1, 2020'
    },

    {
        'author': 'Cambria',
        'title': 'When I keep quite!!!!!',
        'content': 'Before I was diagnosed with depression, anxiety and severe ADHD, I was quite oblivious to mental health issues. Since then, I have gained a much deeper insight on how society views and deals with these issues. I have also come to realise how my words effect the way people interact with me, and how they view me as a person. Words are powerful. Which is why I have said publicly, “when I keep quite, stigma wins – and I can’t let that happen”.',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'Ananya',
        'title': 'Depression does not mean I am lazy or rude!!!',
        'content': 'It started with feeling irritated over small issues. I did not look forward to spending time with my baby. My in-laws would make me loose my nerve. For no reason at all, I was getting angry at home. Even in the office, I didn’t feel like working anymore. I was losing enthusiasm for life and struggling to enjoy the things that would usually make me happy.',
        'date_posted': 'May 26, 2020'
    }
]'''


@app.route("/")
@app.route("/home")
def home():
    form=sentimentform()
    if form.validate_on_submit():
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict_1 = sid_obj.polarity_scores(form.q1.data)
        sentiment_dict_2 = sid_obj.polarity_scores(form.q2.data)
        sentiment_dict_3 = sid_obj.polarity_scores(form.q3.data)
        sentiment_dict_4 = sid_obj.polarity_scores(form.q4.data)
        sentiment_dict_5 = sid_obj.polarity_scores(form.q5.data)
        form.result.data= sentiment_dict_1['compound']+sentiment_dict_2['compound']+sentiment_dict_3['compound']+sentiment_dict_4['compound']+sentiment_dict_5['compound']
        return redirect(url_for('result'))
    return render_template('home.html',title='home')


@app.route("/result")
def result():
    form=sentimentform()
    return render_template('result.html',title='result',result=form.result.data)


@app.route("/about")
def about():
    return render_template('about.html',title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}! Your appointment is confirmed with Dr. {form.Cname.data} .More details will be conveyed through E-mail', 'success.')
        return redirect(url_for('about'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'harshitajoshi048@gmail.com' and form.password.data == 'kkk':
            flash('You have been logged in!', 'success')
            return redirect(url_for('about'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/appointment")
def appointment():
    return render_template('appointment.html',title='Appointment')





@app.route("/consultation")
def consultation():
    return render_template('consultation.html',title='Consultant')

@app.route("/know_each_other")
def KEO():
    posts= PostForm()
    if posts.validate_on_submit():
        post = Post(title=posts.title.data, content=posts.content.data, author=posts.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('KEO.html',posts=posts,title='KEO')


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask,render_template, request, redirect, url_for,abort
from flask_sqlalchemy import SQLAlchemy 
from . import main
from ..models import Blog,User
from ..forms import CommentForm,Blogpost, PostForm
from flask_login import login_required, current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://khalyz:1234@localhost/blog'


db = SQLAlchemy(app)


@main.route('/blogs')
@login_required
def blogs():
    all_blogs = Blog.query.order_by(db.desc(Blog.created_at)).limit(15)

    return render_template('blogs.html', all_blogs=all_blogs)

@main.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).first()

    return render_template('post.html', post=post)

@main.route('/post')
def add():
    return render_template('post.html')

@main.route('/addblog', methods=['GET','POST'])
@login_required
def addpost():

    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_blog = Blog(title=title,
                        content=content, user=current_user)

        new_blog.save_blog()
        return redirect(url_for('main.index'))

    return render_template('new_blog.html', form=form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile.html", user=user)


if __name__ == '__main__':
    app.run(debug=True)
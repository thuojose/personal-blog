import os
from flask import Flask, render_template, request,redirect,url_for,abort, flash
from . import main
from ..models import User, Blogpost, Comment
from .forms import SharePostForm, UpdateProfile,CommentForm
from ..import db, photos
from flask_login import login_required, current_user
from ..request import get_quote


#Views

# home page
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    quote = get_quote()
    
    title = 'Blog Busters'
    return render_template('index.html', title=title, quote= quote)

# share blogpost 
@main.route('/sharepost', methods=['GET','POST'])
def sharepost():
    '''
    View share post page function that returns the post sharing page and its data
    '''
    quote = get_quote()
        
    form = SharePostForm()
    # blogposts = Blogpost.query.all()
    
    if form.validate_on_submit():
        blogpost = Blogpost(category=form.topic.data, blogpost=form.content.data)
        db.session.add(blogpost)
        db.session.commit()
    
        return redirect(url_for('main.goToBlogposts'))
    
    title = 'Blog Busters'
    return render_template('sharepost.html', title=title, SharePostForm=form, quote=quote)

# user profile page
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    title = 'Blog Busters: myProfile'
    return render_template("profile/profile.html", user = user, title=title)

# update profile page - update user bio
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    
    title = 'Blog Busters'
    return render_template('profile/update.html',form =form, user=user, title=title)

# update prof pic
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


# Redirect to blogpost page
@main.route('/blogposts', methods=['GET','POST'])
def goToBlogposts():
    '''
    View blogposts page function that returns the pitches page and its details
    '''   
    TechSavyPosts = Blogpost.query.filter_by(category='TechSavy').all()
    MoneySmartPosts = Blogpost.query.filter_by(category='MoneySmart').all()
    LifenLaughterPosts = Blogpost.query.filter_by(category='Life & Laughter').all()
    
    comment_form = CommentForm()
    # comments = Blogpost.query.filter_by(blogpost_id=id)
    # comments = Comment.query.filter_by(blogpost_id=id).first()
    comments = Comment.query.filter(Comment.blogpost_id > 0).all()

    
    title = 'Blog Busters'
    return render_template('/blogposts.html', TechSavyPosts=TechSavyPosts, MoneySmartPosts=MoneySmartPosts, LifenLaughterPosts=LifenLaughterPosts, comments = comments, CommentForm=comment_form, title=title)

#posting comments
@main.route('/blogposts', methods = ['GET','POST'])
def postComments(blogpost_id):
    '''
    View comments function that returns the blogposts page with the posted comments
    '''
    TechSavyPosts = Blogpost.query.filter_by(category='TechSavy').first()
    MoneySmartPosts = Blogpost.query.filter_by(category='MoneySmart').first()
    LifenLaughterPosts = Blogpost.query.filter_by(category='Life & Laughter').first()
    
    comment_form = CommentForm()
    comment =Comment.query.filter_by(blogpost_id=id)
    comment = Comment.query.filter_by(blogpost_id=id).first()
    comment = Comment.query.filter(Comment.blogpost_id > 0).all()

    print('===================================================')
    
    commentform = CommentForm()
        
    print('===================================================')
    
    if commentform.validate_on_submit():
        comment = Comment(comment=commentform.comment.data, blogpost_id=blogpost_id, users_id=1)
        print(comment)
        print('===================================================')
        db.session.add(comment)
        db.session.commit()
    
        return redirect(url_for('main.goToBlogposts'))
    
    title='Blog Busters'
    return render_template('/blogposts.html', TechSavyPosts=TechSavyPosts, MoneySmartPosts=MoneySmartPosts, LifenLaughterPosts=LifenLaughterPosts, comment = comment, CommentForm=comment_form, title=title)
    
@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    blog = Blogpost.query.get_or_404(id)
    if blog.user != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('main.goToBlogposts'))
@main.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment =Comment.query.get_or_404(comment_id)
    if (comment.user.id) != current_user.id:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('comment succesfully deleted')
    return redirect (url_for('main.goToBlogposts'))


  
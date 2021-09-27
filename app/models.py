from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager


# User model
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    blogposts = db.relationship('Blogpost',backref = 'user',lazy="dynamic")
    comments = db.relationship('Comment',backref = 'user',lazy="dynamic")


    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    def __repr__(self):
        return f'{self.username}'
    

# Blogpost Model
class Blogpost(db.Model):
    __tablename__='blogposts'
    id = db.Column(db.Integer,primary_key = True)
    blogpost = db.Column(db.String(700))
    category = db.Column(db.String(255))
    users_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    comments = db.relationship('Comment',backref = 'blogpost',lazy="dynamic")
    
    def save_blogpost(self):
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'{self.blogpost}'
    

# Comment Model
class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(255))
    users_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    blogpost_id = db.Column(db.Integer,db.ForeignKey('blogposts.id'))

    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    
    
    def __repr__(self):
        return f'{self.comment}, {self.users_id}, {self.blogpost_id}'
    
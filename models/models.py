from db_connect import db


class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publication_date=db.Column(db.Date)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    link = db.Column(db.Text(), nullable=False)
    img = db.Column(db.String(125), nullable=False)
    in_stock = db.Column(db.Integer, nullable=False,default=5)
    rating = db.Column(db.Integer, nullable=False,default=0)
    def __init__(self, title, publication_date ,author, publisher,pages, isbn, description,link, img):
        self.title=title        
        self.author=author
        self.publisher=publisher
        self.publication_date=publication_date
        self.pages=pages
        self.isbn=isbn
        self.description=description
        self.link=link
        self.img=img

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class BookReview(db.Model):
    __tablename__ = 'BookReview'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    comment_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    comment = db.Column(db.Text(), nullable=False)
    star = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, comment_date, user_id, book_id, comment, star):
        self.comment_date = comment_date
        self.user_id = user_id
        self.book_id = book_id
        self.comment = comment
        self.star = star


class BookRental(db.Model):
    __tablename__ = 'BookRental'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    rental_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    is_returned = db.Column(db.Integer, nullable=False, default=False)
    return_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, rental_date, user_id, book_id, is_returned, return_date):
        self.rental_date = rental_date
        self.user_id = user_id
        self.book_id = book_id
        self.is_returned = is_returned
        self.return_date = return_date

''' 
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from datetime import datetime
from db_connect import db

class Book(db.Model):
    __tablename__='Book'

    id = db.Column(db.Integer, primary_key=True, nullable =False,autoincrement=True )
    book_title=db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable =False)
    publisher=db.Column(db.Integer,db.ForeignKey('Publisher.id', ondelete='CASCADE', onupdate='CASCADE'),nullable=False)
    author=db.Column(db.Integer,db.ForeignKey('Author.id', ondelete='CASCADE', onupdate='CASCADE'),nullable=False)
    publication_date=db.Column(db.DateTime, nullable =False)
    pages=id = db.Column(db.Integer, nullable =False)
    isbn=db.Column(db.Integer, nullable =False)
    description=db.Column(db.String(200, 'utf8mb4_unicode_ci'))
    link=db.Column(db.TEXT( 'utf8mb4_unicode_ci'))
    
    ed=db.Column(db.Integer,default=1)
    img=db.Column(db.String(512, 'utf8mb4_unicode_ci'))
    no_in_stock=db.Column(db.Integer,default=1)

    def __init__(self, book_title, publication_date ,author_id, publisher_id,pages, isbn, description,link, ed,img_src):
        self.book_title=book_title        
        self.author_id=author_id
        self.publisher_id=publisher_id
        self.publication_date=publication_date
        self.pages=pages
        self.isbn=isbn
        self.description=description
        self.link=link
        self.img_src=img_src
    Author = relationship('Author')
    Publisher = relationship('Publisher')

class Publiher(db.Model):
    __tablename__='Publiher'
    id = db.Column(db.Integer, primary_key=True, nullable =False,autoincrement=True )
    publiher_name=db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable =False)

    def __init__(self, publiher_name):
        self.publiher_name=publiher_name


class Author(db.Model):
    __tablename__='Author '
    id = db.Column(db.Integer, primary_key=True, nullable =False,autoincrement=True )
    author_name=db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable =False)

    def __init__(self, author_name):
        self.author_name=author_name


class User(db.Model):
    __tablename__='User'

    id = db.Column(db.String(255,'utf8mb4_unicode_ci') , primary_key=True, nullable =False) 
    name=db.Column(db.String(20, 'utf8mb4_unicode_ci'), nullable =False)
    pwd=db.Column(db.String(255, 'utf8mb4_unicode_ci'), nullable =False)
    user_type=db.Column(db.String(1, 'utf8mb4_unicode_ci'), defualt=0)


    def __init__ (self, user_id, name, pwd):
        self.user_id=user_id
        self.name=name
        self.pwd=pwd

    class  Rental(db.Model):
        __tablename__='Rental'

        id = db.Column(db.Integer, primary_key=True, nullable =False,autoincrement=True )
        book_id =db.Column(db.Integer,db.ForeignKey('Book.id', ondelete='CASCADE', onupdate='CASCADE'), nullable =False)
        user_id = db.Column(db.String(255,'utf8mb4_unicode_ci') ,db.ForeignKey('User.id', ondelete='CASCADE', onupdate='CASCADE'),nullable =False) 
        rental_date=db.Column(db.DateTime, nullable =False, default=datetime.datetime.utcnow)
        renewed =db.Column(db.Integer, default=0)
        rating=db.Column(db.Integer, default=5)
            
        Book = relationship('Book')
        User = relationship('User')


    class Review(db.Model):
        __tablename__='Review'

        id = db.Column(db.Integer, primary_key=True, nullable =False,autoIncrement=True )
        commented_date=db.Column(db.DateTime,nullable=False)
        comment=db.Column(db.String(200, 'utf8mb4_unicode_ci'))
        rating=db.Column(db.Integer,default=5,nullable=False)

        book_id =db.Column(db.Integer,  db.ForeignKey('Book.id', ondelete='CASCADE', onupdate='CASCADE'),nullable=False)
        user_id = db.Column(db.String(255,'utf8mb4_unicode_ci'),db.ForeignKey('User.id', ondelete='CASCADE', onupdate='CASCADE') , nullable =False) 

        def __init__(self,comment,rating,book_id,user_id):
            self.comment=comment
            self.rating=rating
            self.book_id=book_id
            self.user_id=user_id

        Book = relationship('Book')
        User = relationship('User')
'''
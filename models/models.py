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
    is_returned = db.Column(db.Integer, nullable=False, default=0)
    return_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, rental_date, user_id, book_id, is_returned, return_date):
        self.rental_date = rental_date
        self.user_id = user_id
        self.book_id = book_id
        self.is_returned = is_returned
        self.return_date = return_date
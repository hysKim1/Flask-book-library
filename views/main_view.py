from flask import Blueprint,render_template,session,redirect,request,url_for
from models.models import Book,BookRental
from db_connect import db
bp=Blueprint('main',__name__,url_prefix='/')

@bp.route('/')
def home():
    no=Book.query.count()
    if no==0:
        import load_data
        load_data.load_data()
    page = request.args.get('page', default=1, type=int)
    book_list = Book.query.order_by(Book.id.asc())
    book_list=book_list.paginate( page, per_page=8)

    return render_template('home.html', book_list=book_list )





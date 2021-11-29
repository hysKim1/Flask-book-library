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


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')

    # 조회
    book_list = Book.query.order_by(Book.title.asc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Book.title, Book.author , Book.description, Book.isbn).filter(
                    Book.title.ilike(search) |  # 책 제목
                    Book.author.ilike(search) |  # 저자
                    Book.description.ilike(search) |  # 설명
                    Book.isbn.ilike(search) )   #isbn              
    # 페이징
    book_list = book_list.paginate(page, per_page=10)
    return render_template('home.html', book_list=book_list, page=page, kw=kw)


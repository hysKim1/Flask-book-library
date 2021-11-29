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
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    # 조회
    book_list = Book.query.order_by(Book.title.asc())
    if kw:
        search = '%%{}%%'.format(kw)
        book_list = book_list.filter(
                    Book.title.ilike(search) |  # 책 제목
                    Book.author.ilike(search) |  # 저자
                    Book.description.ilike(search) |  # 설명
                    Book.isbn.ilike(search) ).order_by(Book.title.asc())   #isbn              
    # 페이징
    book_list = book_list.paginate(page, per_page=8)

    return render_template('search_result.html', book_list=book_list, page=page, kw=kw)
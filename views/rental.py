
from flask  import Blueprint,render_template, redirect, url_for, flash
from db_connect import db
from models.models import Book, BookRental,User
from datetime import datetime 
from flask_login import login_required,current_user

bp=Blueprint('rental',__name__,url_prefix='/rental')

@bp.route("/rented_list")
@login_required
def book_rented():
    #유저가 대여한 모든 책
    rental_info = BookRental.query.filter( (BookRental.user_id ==  current_user.id)&(BookRental.is_returned==0)).order_by(BookRental.rental_date.desc()).all()
    if len(rental_info) == 0:
        flash('대여한 기록이 존재하지 않습니다.', 'danger')
        return render_template('rental.html')
    
    else:
        rented_list = []

        for rented_book in rental_info:
            book_info = Book.query.filter(Book.id == rented_book.book_id).first()
            rented_list.append((book_info, rented_book))

    return render_template('rental.html', rented_list=rented_list)

@bp.route("/returned_list")
@login_required
def book_returned():
    #유저가 반납한 책
    rental_info = BookRental.query.filter( (BookRental.user_id ==  current_user.id)&(BookRental.is_returned==1)).order_by(BookRental.rental_date.desc()).all()
    if len(rental_info) == 0:
        flash('반납한 기록이 존재하지 않습니다.', 'danger')
        return render_template('return.html')
    
    else:
        rented_list = []

        for rented_book in rental_info:
            book_info = Book.query.filter(Book.id == rented_book.book_id).first()
            rented_list.append((book_info, rented_book))

    return render_template('return.html', rented_list=rented_list)


@bp.route('rent/<int:book_id>', methods=('GET', 'POST'))
@login_required
def rent(book_id):
    book = Book.query.filter(Book.id == book_id).first()

    message, messageType = None, None

    if book.in_stock== 0:
        flash('책이 존재하지 않습니다.', 'warning')
        return redirect('/')

    elif len( BookRental.query.filter( (BookRental.book_id == book_id) & (BookRental.user_id == current_user.id) & (BookRental.is_returned == 0)).all()) >=1: 
        flash('이미 대여한 책입니다.', 'warning')
        return redirect('/')
    else:
        book.in_stock -= 1
        book_rental = BookRental( datetime.now(),  current_user.id, book_id, 0, datetime.now())
        db.session.add(book_rental)
        db.session.commit()
        message, messageType = '성공적으로 대여하였습니다.', 'success'
    
    flash(message=message, category=messageType)
    return redirect('/')

@bp.route("/return/<int:book_id>", methods=['GET', 'POST'])
@login_required
def book_return(book_id):
    #해당 유저가 대여한 책 중 반납
    rented_book = BookRental.query.filter((BookRental.book_id == book_id) & (BookRental.is_returned == 0) & (BookRental.user_id == current_user.id) ).first()
    message, messageType = None, None

    if not rented_book :
        message, messageType = '현재 대여한 책이 존재하지 않습니다.', 'danger'
        return redirect('/')
    else:
        rented_book.is_returned = 1
        rented_book.return_date = datetime.now()
        db.session.commit()

        book = Book.query.filter(Book.id == book_id).first()
        book.in_stock += 1
        db.session.commit()
            
        rental_info = BookRental.query.filter( (BookRental.user_id == current_user.id) & (BookRental.is_returned == 0)).all()
        rented_list = []

        for rented_book in rental_info:
            book_info = Book.query.filter(Book.id == rented_book.book_id).first()
            rented_list.append((book_info,rented_book))
        message, messageType = '반납 완료', 'success'

    flash(message=message, category=messageType)
    return redirect(url_for('rental.book_return',book_id=book_id, rented_list=rented_list))
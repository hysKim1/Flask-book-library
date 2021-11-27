from flask  import Blueprint, request, session, redirect, url_for, flash,render_template
from db_connect import db
from models.models import Book,BookReview,User
from datetime import datetime

bp=Blueprint('book',__name__,url_prefix='/book')

@bp.route('/<int:book_id>', methods=['GET','POST'])
def book_indetail(book_id):
    book_info=Book.query.filter_by(id=book_id).first_or_404()

    review_info=BookReview.query.filter_by(book_id=book_id).order_by(BookReview.comment_date.desc())
    
    cnt,rating_sum,avg=0,0,0
    for review in review_info:
        rating_sum+=  review.star 
        cnt+=1
        avg = round(rating_sum/cnt)
    book_info.rating=avg #평균평점 업데이트
    db.session.commit()

    page = request.args.get('page', type=int, default=1)  # 페이지

    review_info =review_info.paginate(page, per_page=8)

    return render_template('book_indetail.html',book_id=book_id, book= book_info,review_info=review_info,avg=avg)
    

@bp.route('/wr_review/<int:book_id>', methods=['GET', 'POST'])
def create_review(book_id):
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('권한이 없습니다.')
            return redirect(url_for('main.home'))

        user_id = session['user_id']

        # 대여자 중 최초 작성자에 한해
        if BookReview.query.filter((BookReview.user_id==user_id) & (BookReview.book_id==book_id)).first() is None:

            review_content=request.form.get('content',None)
            review_rating =request.form.get('rating',None)
            review= BookReview(user_id=user_id , book_id=book_id, star=review_rating, comment=review_content,comment_date=datetime.now())
            db.session.add(review)
            db.session.commit()

            flash('리뷰 등록 완료')
            return redirect(url_for('book.book_indetail', book_id=book_id))
        flash('이미 작성하셨습니다.')
        return redirect(url_for('book.book_indetail',book_id=book_id))

    return redirect('/')

@bp.route('/del_review/<int:review_id>')
def del_review(review_id):    
    review_info = BookReview.query.filter_by(id=review_id).first()

    db.session.delete(review_info)
    db.session.commit()

    flash("정상적으로 삭제 되었습니다.")

    book_info = Book.query.filter_by(id=review_info.book_id).first()
    return redirect(url_for("book.book_indetail",review_id=review_id ,book_id=book_info.id))
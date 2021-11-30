from flask  import Blueprint, request, session, redirect, url_for, flash,render_template
from db_connect import db
from models.models import Book,BookReview,BookRental
from datetime import datetime
from flask_login import login_required,current_user

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
    

@bp.route('/wr_review/<int:book_id>', methods=('POST','GET'))
@login_required
def create_review(book_id):
    # 대여자 중 최초 작성자
    if request.method=='POST':
        if BookReview.query.join(BookRental,BookRental.book_id==BookReview.book_id).filter((BookReview.user_id==current_user.id)  & (BookReview.user_id==BookRental.user_id)).first() == None :         
            review_content=request.form.get('content',None)
            review_rating =request.form.get('rating',None)
            review= BookReview(user_id=current_user.id , book_id=book_id, star=review_rating, comment=review_content,comment_date=datetime.now())
            db.session.add(review)
            db.session.commit()
            flash('리뷰 등록 완료')
            return redirect('{}#review_redirecting1{}'.format(url_for('book.book_indetail', book_id=book_id),review.id))
        else:
            flash('이미 작성하셨습니다.')
        return redirect(url_for('book.book_indetail',book_id=book_id))
    else:
        return redirect(url_for('book.book_indetail',book_id=book_id))
    

@bp.route('/del_review/<int:review_id>')
@login_required
def del_review(review_id):    
    review_info = BookReview.query.filter_by(id=review_id).first()
    book_id=review_info.book_id
    db.session.delete(review_info)
    db.session.commit()

    flash("정상적으로 삭제 되었습니다.")

    return redirect(url_for("book.book_indetail",book_id=book_id))
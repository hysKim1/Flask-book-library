import csv
from datetime import  datetime

from db_connect import db
from models.models import Book
from app import create_app
app = create_app()
app.app_context().push()

def load_data():
    with open('static/book_list.csv', 'r') as f:
        reader = csv.DictReader(f)

        for r in reader:
            publication_date = r['publication_date']
            image_path = f"static/book_img/{r['id']}"
            try:
                open(f'{image_path}.png')
                image_path += '.png'
            except:
                image_path += '.jpg'

            publication_date = datetime.strptime(publication_date, '%Y-%m-%d').date()
            book = Book(
                title=r['book_name'], publisher=r['publisher'],
                author=r['author'], publication_date=publication_date, pages=int(r['pages']),
                isbn=r['isbn'], description=r['description'],link=r['link'], img=image_path, 
            )
            db.session.add(book)
        db.session.commit()

load_data()



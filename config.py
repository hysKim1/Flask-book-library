import os

BASE_DIR = os.path.dirname(__file__) # 폴더 구조가 달라져도, 현재 폴더를 가져와서 사용할 수 있도록 설정합니다.

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'Library.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 이걸 켜면 메모리 사용량이 늘어나서, 꺼주는게 좋아요.
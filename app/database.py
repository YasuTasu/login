from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
from passlib.context import CryptContext

# データベースのURL（SQLiteを使用）
DATABASE_URL = "sqlite:///./users.db"

# データベース接続
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# パスワードハッシュ化用
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ユーザーテーブルのモデル
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")  # "user" or "admin"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# データベースの初期化関数
def init_db():
    Base.metadata.create_all(bind=engine)

# 事前登録するユーザーを追加
def add_default_users():
    db = SessionLocal()

    users = [
        {"user_id": "test_user", "password": "securepassword123", "role": "user"},
        {"user_id": "admin_user", "password": "adminpassword123", "role": "admin"}
    ]

    for user in users:
        existing_user = db.query(User).filter(User.user_id == user["user_id"]).first()
        if not existing_user:
            hashed_password = pwd_context.hash(user["password"])  # bcrypt ハッシュ化
            new_user = User(user_id=user["user_id"], password_hash=hashed_password, role=user["role"])
            db.add(new_user)
            print(f"ユーザー {user['user_id']}（{user['role']}）を登録しました。")
        else:
            print(f"ユーザー {user['user_id']} は既に存在します。")

    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    add_default_users()
    print("データベースを初期化しました！")

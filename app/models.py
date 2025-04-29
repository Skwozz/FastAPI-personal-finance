from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True,index=True,nullable=False)
    email = Column(String,unique=True,index=True,nullable=False)
    hashed_password = Column(String,nullable=False)

    categories = relationship('Category', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')


class CategoryType(enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(CategoryType), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User',back_populates='categories')
    transactions = relationship('Transaction',back_populates='category')


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey('users.id'))
    is_deleted = Column(Boolean,default=False)

    category = relationship("Category", back_populates='transactions')
    user = relationship('User', back_populates='transactions')
import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from database import Base


class User(Base):
    """ A model for defining a user object"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=True)
    f_name = Column(String(50), nullable=False)
    l_name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    pin = Column(String)
    balance = Column(String(50), server_default='500')
    birth_month = Column(String(50))
    birth_year = Column(String(50))
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    sent_transactions = relationship('Transaction', back_populates='sender', foreign_keys='Transaction.sender_id')
    received_transactions = relationship('Transaction', back_populates='receiver',
                                         foreign_keys='Transaction.receiver_id')


class Transaction(Base):
    """ A model for defining a transaction object"""
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, nullable=True)
    transaction_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    phone = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)
    balance = Column(Integer)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    sender = relationship('User', back_populates='sent_transactions', foreign_keys=[sender_id])
    receiver = relationship('User', back_populates='received_transactions', foreign_keys=[receiver_id])

from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Table, func, UniqueConstraint
#from sqlalchemy.dialects import mysql
#from sqlalchemy.ext.associationproxy import association_proxy
#from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
#from sqlalchemy.sql import expression

from punto_venta_app.database import Base

user_role = Table('UserRole',
                  Base.metadata,
                  Column('id', Integer, primary_key=True),
                  Column('roleId', Integer, ForeignKey('Role.id'), nullable=True),
                  Column('userId', Integer, ForeignKey('User.id'), nullable=True)
                  )


class User(Base):
    __tablename__ = 'User'
    __table_args__ = (
        UniqueConstraint('username'),
        UniqueConstraint('phone_number'),
        UniqueConstraint('email'),
    )

    # todo: add deletion or modification date for logging funcs

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=True)
    password = Column(String(250), nullable=False)
    firstname = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    isActive = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)

    roles: List['Role'] = relationship('Role', secondary=user_role, back_populates='users')


class Role(Base):
    __tablename__ = 'Role'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    isActive = Column(Integer, nullable=True)

    users: List[User] = relationship('User', secondary=user_role, back_populates='roles')

    def __repr__(self) -> str:
        return '<Role [id={}] [name={}]>'.format(self.id, self.name)
    
tables_shortnames = {
}

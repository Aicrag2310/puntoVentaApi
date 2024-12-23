from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Table, func, UniqueConstraint, Float
#from sqlalchemy.dialects import mysql
#from sqlalchemy.ext.associationproxy import association_proxy
#from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
#from sqlalchemy.sql import expression
from datetime import datetime

from punto_venta_app.database import Base

user_role = Table('UserRole',
                  Base.metadata,
                  Column('id', Integer, primary_key=True),
                  Column('roleId', Integer, ForeignKey('Role.id'), nullable=True),
                  Column('userId', Integer, ForeignKey('User.id'), nullable=True)
                  )


class Product(Base):
    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    purchase_price = Column(Float, nullable=False)    
    retail_price = Column(Float, nullable=False)
    wholesale_price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    min_stock = Column(Integer, nullable=False, default=0)
    max_stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    isActive = Column(Integer, nullable=False, default=1)

    category_id = Column(Integer, ForeignKey('Category.id'), nullable=False)
    category = relationship('Category', back_populates='products')

class Category(Base):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    isActive = Column(Integer, nullable=False, default=1)

    products: List[Product] = relationship('Product', back_populates='category')

    def __repr__(self):
        return f'<Category [id={self.id}] [name={self.name}]>'


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

class SaleDetail(Base):
    __tablename__ = 'SaleDetail'

    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('Sale.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('Product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    sale_type = Column(String(50), nullable=False)
    subtotal = Column(Float, nullable=False)

    sale = relationship('Sale', back_populates='sale_details')
    product = relationship('Product')

    def __repr__(self):
        return f'<SaleDetail [id={self.id}] [product_id={self.product_id}] [quantity={self.quantity}]>'


class Sale(Base):
    __tablename__ = 'Sale'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    total = Column(Float, nullable=False)
    sale_date = Column(DateTime, nullable=False, default=datetime.now)
    payment_method = Column(String(50), nullable=True)
    client_name = Column(String(150), nullable=True)
    isActive = Column(Integer, nullable=False, default=1)

    user = relationship('User')
    sale_details = relationship('SaleDetail', back_populates='sale')

    def __repr__(self):
        return f'<Sale [id={self.id}] [total={self.total}] [date={self.sale_date}]>'


tables_shortnames = {
}

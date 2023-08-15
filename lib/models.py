from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# Table object to connects tables
game_user = Table(
    'game_users',
    Base.metadata,
    Column('game_id', ForeignKey('games.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True,
)
# Adds the game model
class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    users = relationship('User', secondary=game_user, back_populates='games') # users relationship with back_populates
    reviews = relationship('Review', backref=backref('game')) # relationship with the Review table

    def __repr__(self):
        return f'Game(id={self.id}, ' + \
            f'title={self.title}, ' + \
            f'platform={self.platform})'
# Adds Review model
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    comment = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())
    
    game_id = Column(Integer(), ForeignKey('games.id'))  # Adds foreign key that establishes relationship to game
    user_id = Column(Integer(), ForeignKey('users.id')) # Adds foreign key that establishes relationship to user

    def __repr__(self):
        return f'Review(id={self.id}, ' + \
            f'score={self.score}, ' + \
            f'game_id={self.game_id})'
    
# adds user model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    games = relationship('Game', secondary=game_user, back_populates='users')
    reviews = relationship('Review', backref=backref('user')) # Relationship with the Review table

    # don't forget your __repr__()!
    def __repr__(self):
        return f'User(id={self.id}, ' + \
            f'name={self.name})'
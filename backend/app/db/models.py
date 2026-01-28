from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    sector = Column(String)
    industry = Column(String)
    
    momentums = relationship("MomentumData", back_populates="stock")
    reddit_mentions = relationship("RedditMention", back_populates="stock")
    insider_trades = relationship("InsiderTrade", back_populates="stock")

class MomentumData(Base):
    __tablename__ = "momentum_data"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    price = Column(Float)
    change_1d = Column(Float)
    change_5d = Column(Float)
    change_20d = Column(Float)
    rsi_14 = Column(Float)
    volume = Column(Float)
    
    stock = relationship("Stock", back_populates="momentums")

class RedditMention(Base):
    __tablename__ = "reddit_mentions"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    subreddit = Column(String)
    post_id = Column(String)
    sentiment_score = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    
    stock = relationship("Stock", back_populates="reddit_mentions")

class InsiderTrade(Base):
    __tablename__ = "insider_trades"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    filing_date = Column(DateTime(timezone=True))
    insider_name = Column(String)
    transaction_type = Column(String) # Buy or Sell
    shares = Column(Float)
    price = Column(Float)
    value = Column(Float)
    
    stock = relationship("Stock", back_populates="insider_trades")

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    name = Column(String)
    quantity = Column(Float)
    avg_price = Column(Float)
    current_price = Column(Float, nullable=True)
    asset_type = Column(String, default="Stock") # Stock, Option, etc.

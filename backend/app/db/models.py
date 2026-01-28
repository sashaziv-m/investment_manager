from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Stock(Base):
    __tablename__ = "stocks"
    __table_args__ = {'extend_existing': True}

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
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=True) # Check if we enforce FK or just symbol logic for momentum
    # MVP: MarketDataService likely just stores by symbol or we link to stock if we have it. 
    # For now, let's keep it simple. The original plan implies linking.
    # But wait, MarketDataService in MVP fetches from YFinance and returns dict? 
    # The models previously defined 'symbol' column directly. Let's support both or just symbol.
    symbol = Column(String, index=True) 
    
    date = Column(DateTime(timezone=True), server_default=func.now())
    price = Column(Float)
    change_1d = Column(Float)
    change_5d = Column(Float)
    change_20d = Column(Float)
    rsi_14 = Column(Float)
    volume = Column(Float)
    
    # New fields from recent addition
    sma_50 = Column(Float)
    sma_200 = Column(Float)
    momentum_score = Column(Float) 
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    stock = relationship("Stock", back_populates="momentums")

class RedditMention(Base):
    __tablename__ = "reddit_mentions"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    subreddit = Column(String)
    post_id = Column(String)
    sentiment_score = Column(Float)
    timestamp = Column(DateTime(timezone=True))
    
    stock = relationship("Stock", back_populates="reddit_mentions")

class InsiderTrade(Base):
    __tablename__ = "insider_trades"
    __table_args__ = {'extend_existing': True}

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
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    name = Column(String)
    quantity = Column(Float)
    avg_price = Column(Float)
    current_price = Column(Float, nullable=True)
    asset_type = Column(String, default="Stock") # Stock, Option, etc.

class AlertRule(Base):
    __tablename__ = "alert_rules"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    metric = Column(String) # e.g. "VIX", "AAPL_PRICE"
    operator = Column(String) # ">", "<", ">=", "<="
    value = Column(Float)
    contact_info = Column(String) # email or phone
    is_active = Column(Boolean, default=True)

class AlertLog(Base):
    __tablename__ = "alert_logs"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("alert_rules.id"))
    message = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    rule = relationship("AlertRule")

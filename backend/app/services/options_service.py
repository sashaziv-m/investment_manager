import logging
import yfinance as yf
from typing import List, Dict

logger = logging.getLogger(__name__)

class OptionsService:
    async def get_unusual_activity(self, tickers: List[str] = ["SPY", "QQQ", "TSLA", "NVDA", "AMD", "AAPL"]) -> List[Dict]:
        """
        Scans for high volume options chains.
        Note: Real-time options flow is expensive. This uses delayed data via yfinance
        to find "Unusual" volume (Volume > Open Interest).
        """
        activity = []
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                # Get earliest expiration
                expirations = stock.options
                if not expirations:
                    continue
                
                # Check closest expiration (weekly activity)
                chain = stock.option_chain(expirations[0])
                
                # Filter Calls
                calls = chain.calls
                # Volume > 500 and Volume > OpenInterest (Signal of aggressive opening)
                unusual_calls = calls[(calls['volume'] > 500) & (calls['volume'] > calls['openInterest'])]
                
                for _, row in unusual_calls.iterrows():
                    activity.append({
                        "symbol": ticker,
                        "type": "Call",
                        "strike": row['strike'],
                        "expiration": expirations[0],
                        "volume": int(row['volume']),
                        "open_interest": int(row['openInterest']),
                        "vol_oi_ratio": round(row['volume'] / (row['openInterest'] or 1), 1),
                        "last_price": row['lastPrice']
                    })

                # Filter Puts
                puts = chain.puts
                unusual_puts = puts[(puts['volume'] > 500) & (puts['volume'] > puts['openInterest'])]
                
                for _, row in unusual_puts.iterrows():
                    activity.append({
                        "symbol": ticker,
                        "type": "Put",
                        "strike": row['strike'],
                        "expiration": expirations[0],
                        "volume": int(row['volume']),
                        "open_interest": int(row['openInterest']),
                        "vol_oi_ratio": round(row['volume'] / (row['openInterest'] or 1), 1),
                        "last_price": row['lastPrice']
                    })
                    
            except Exception as e:
                logger.error(f"Error fetching options for {ticker}: {e}")
                
        # Sort by Volume desc
        activity.sort(key=lambda x: x['volume'], reverse=True)
        return activity[:20]

    async def get_market_sentiment(self):
        """
        Calculates Put/Call Ratio for SPY and QQQ.
        High Ratio (> 1.0) = Bearish/Hedging
        Low Ratio (< 0.7) = Bullish
        """
        sentiment = []
        for ticker in ["SPY", "QQQ"]:
            try:
                stock = yf.Ticker(ticker)
                expirations = stock.options
                if not expirations:
                    continue
                
                # Aggregate volume for near-term expiration
                chain = stock.option_chain(expirations[0])
                
                total_call_vol = chain.calls['volume'].sum()
                total_put_vol = chain.puts['volume'].sum()
                
                pc_ratio = round(total_put_vol / (total_call_vol or 1), 2)
                
                signal = "Neutral"
                if pc_ratio > 1.0: signal = "Bearish (High Puts)"
                elif pc_ratio < 0.7: signal = "Bullish (High Calls)"
                
                sentiment.append({
                    "symbol": ticker,
                    "pc_ratio": pc_ratio,
                    "signal": signal,
                    "total_volume": int(total_call_vol + total_put_vol)
                })
            except Exception as e:
                logger.error(f"Error fetching sentiment for {ticker}: {e}")
                
        return sentiment

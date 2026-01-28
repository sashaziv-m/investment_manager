import praw
from textblob import TextBlob
import re
from collections import Counter
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class RedditService:
    def __init__(self):
        self.reddit = None
        if settings.REDDIT_CLIENT_ID and settings.REDDIT_CLIENT_SECRET:
            self.reddit = praw.Reddit(
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                user_agent=settings.REDDIT_USER_AGENT
            )

    def analyze_sentiment(self, text: str) -> float:
        return TextBlob(text).sentiment.polarity

    def extract_tickers(self, text: str) -> list:
        # Simple regex for $TICKER (e.g. $AAPL) and common uppercase words of 3-5 chars
        # Avoiding common words like "THE", "AND", "FOR" is hard with just regex, 
        # but for MVP we focus on $Cashtags primarily or very obvious caps.
        # Let's stick to $TICKER for high precision in MVP.
        comp = re.compile(r'\$([A-Z]{2,5})')
        return comp.findall(text)

    async def get_trends(self, subreddit_name="wallstreetbets", limit=50):
        if not self.reddit:
            logger.warning("Reddit credentials not set. Returning mock data.")
            return self._get_mock_data()

        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            tickers = []
            sentiment_map = {} # tick -> [scores]

            # Determining hot posts is synchronous in PRAW, might block event loop.
            # For MVP it's acceptable, but ideally run in executor.
            for submission in subreddit.hot(limit=limit):
                text = f"{submission.title} {submission.selftext}"
                found_tickers = self.extract_tickers(text)
                
                # Sentiment of the post
                score = self.analyze_sentiment(text)
                
                for ticker in found_tickers:
                    tickers.append(ticker)
                    if ticker not in sentiment_map:
                        sentiment_map[ticker] = []
                    sentiment_map[ticker].append(score)

            # Aggregate
            counts = Counter(tickers)
            results = []
            for ticker, count in counts.most_common(10):
                scores = sentiment_map[ticker]
                avg_sentiment = sum(scores) / len(scores) if scores else 0
                results.append({
                    "symbol": ticker,
                    "mentions": count,
                    "sentiment": round(avg_sentiment, 2)
                })
            
            return results

        except Exception as e:
            logger.error(f"Error fetching Reddit trends: {e}")
            return []

    def _get_mock_data(self):
        return [
            {"symbol": "SPY", "mentions": 42, "sentiment": -0.15},
            {"symbol": "NVDA", "mentions": 35, "sentiment": 0.45},
            {"symbol": "TSLA", "mentions": 28, "sentiment": 0.12},
            {"symbol": "AMD", "mentions": 20, "sentiment": 0.33},
            {"symbol": "AAPL", "mentions": 15, "sentiment": 0.05},
        ]

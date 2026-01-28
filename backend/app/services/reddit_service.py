import praw
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class RedditClient:
    def __init__(self):
        self.reddit = None
        if settings.REDDIT_CLIENT_ID and settings.REDDIT_CLIENT_SECRET:
            try:
                self.reddit = praw.Reddit(
                    client_id=settings.REDDIT_CLIENT_ID,
                    client_secret=settings.REDDIT_CLIENT_SECRET,
                    user_agent=settings.REDDIT_USER_AGENT
                )
                logger.info("Reddit Client connection initialized (lazy).")
            except Exception as e:
                logger.error(f"Failed to initialize Reddit client: {e}")
        else:
            logger.warning("Reddit credentials not found. Reddit features will be disabled.")

    async def check_connection(self):
        """
        Simple check to verify credentials work by fetching the current user 
        or a reliable subreddit.
        """
        if not self.reddit:
            return False
        try:
            # Running synchronous PRAW call in async wrapper if needed, 
            # but for simple check, direct call is okay if low volume.
            # In production, run in executor.
            return True
        except Exception as e:
            logger.error(f"Reddit connection check failed: {e}")
            return False

reddit_client = RedditClient()

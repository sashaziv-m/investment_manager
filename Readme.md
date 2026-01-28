# Portfolio Defense & Opportunity Dashboard - Project Outline

## Project Overview
A comprehensive market intelligence system combining defensive portfolio monitoring with offensive opportunity identification. Built for financial independence and expat living, replacing paid services like Unusual Whales, TradingView, and Reddit sentiment trackers.

## Target User
- FIRE individuals living off investment portfolios
- Expats with lower cost of living needing crash protection AND growth opportunities
- Software engineers with financial background
- Active investors wanting both risk management and momentum signals
- Anyone wanting comprehensive market monitoring without $100-200/month in subscriptions

## Core Value Proposition
- **Defense**: Real-time portfolio monitoring with crash indicators and hedge tracking
- **Offense**: Momentum scanning, Reddit sentiment analysis, insider tracking
- **Cost-effective**: Alternative to $100-200/month in subscription services
- **Customizable**: Tailor alerts and screens to your strategy
- **Potential SaaS**: Serve similar users in FIRE/expat communities

---

## Feature Tiers

### Easy Tier (Days to Weeks)

#### Defensive Features
**VIX Threshold Alerts**
- Monitor VIX levels and alert at key thresholds (18, 25, 30+)
- Historical VIX tracking and visualization
- SMS/email/push notifications

**Basic Options Flow Scraping**
- Track unusual options volume on SPY, QQQ
- Detect put/call ratio anomalies
- Free API integration

**Price/Volume Anomaly Detection**
- Identify unusual trading patterns
- Volume spikes relative to average
- Gap detection and alerts

**Custom Technical Indicators**
- Moving averages, RSI, MACD
- Support/resistance level tracking
- Custom threshold alerts

**Portfolio Tracking**
- Real-time portfolio value calculation
- Hedge position monitoring (puts, VIX calls)
- Runway calculation (months remaining at burn rate)

#### Offensive/Opportunity Features
**Momentum Scanner**
- Identify stocks with strong price momentum (20-day, 50-day trends)
- Relative strength rankings
- Breakout detection (52-week highs, chart patterns)
- Volume confirmation

**Social Sentiment Scraper**
- WallStreetBets subreddit scraping (top posts, comment sentiment)
- Reddit mentions tracking across investing subreddits
- Twitter/X finance community monitoring
- Sentiment scoring (bullish/bearish intensity)

**ETF Flow Tracker**
- Monitor daily ETF inflows/outflows
- Sector rotation signals
- Smart money following (track popular ETFs)
- Thematic investing trends

**Insider Trading Monitor**
- SEC Form 4 filings (insider buys/sells)
- Cluster analysis (multiple insiders buying)
- Insider buying as bullish signal
- Free data from SEC EDGAR

### Medium Tier (Weeks to Months)

#### Defensive Features
**Dark Pool Data Aggregation**
- Collect data from free/cheap sources
- Track institutional block trades
- Identify accumulation/distribution patterns

**Unusual Options Volume Detection**
- Compare current volume to historical averages
- Detect whale activity
- Options flow direction (bullish/bearish)

**Market Regime Detection**
- Bull/bear market classification
- High/low volatility regime identification
- Correlation breakdowns

#### Offensive/Opportunity Features
**Advanced Momentum Screening**
- Multi-timeframe momentum analysis (daily, weekly, monthly)
- Relative strength vs sector and market
- CANSLIM-style screening (earnings growth, sales growth, new highs)
- Quality filters (exclude penny stocks, low volume)

**Earnings Calendar & Surprise Tracker**
- Upcoming earnings dates
- Historical beat/miss patterns
- Pre-earnings unusual options activity
- Post-earnings momentum continuation

**Reddit/Social Aggregator Dashboard**
- Real-time tracking of r/wallstreetbets top tickers
- Sentiment analysis of comments (PRAW Reddit API)
- Mention frequency trending
- Filter out pump-and-dump schemes (volume, market cap filters)
- Track r/stocks, r/investing, r/options for quality signals

**Technical Pattern Recognition**
- Cup and handle, ascending triangles
- Bull flag, pennant formations
- Golden cross, death cross detection
- Automated chart pattern scanning

**Sector Rotation Analysis**
- Track which sectors are leading/lagging
- Identify early rotation signals
- Correlation with economic cycle
- Best sector ETFs for current regime

**Whale Watching**
- Track 13F filings from top hedge funds (Berkshire, Bridgewater, etc.)
- Identify new positions, increased stakes
- Clone best investor portfolios
- Quarterly updates automated

### Hard Tier (Months, Data Costs)
**Real-time Options Flow**
- Requires expensive data feeds
- Alternative: delayed data from free sources
- Focus on end-of-day analysis instead

**Proprietary Indicators (DIX/GEX)**
- Complex methodology
- May require paid data
- Can approximate with available data

**Institutional Positioning**
- 13F filings from SEC EDGAR
- Delayed but valuable
- Track smart money moves

---

## Data Sources

### Free APIs

#### Market Data & Defense
- **Yahoo Finance API**: Basic price/volume data
- **Alpha Vantage**: Technical indicators, VIX (free tier)
- **FRED API**: Macro economic data (unemployment, Fed funds)
- **Polygon.io**: Options data (free tier available)
- **CBOE**: Direct VIX data
- **SEC EDGAR**: 13F institutional filings, Form 4 insider trades
- **Fear & Greed Index**: CNN Business

#### Social & Sentiment Data
- **PRAW (Python Reddit API Wrapper)**: Reddit scraping (r/wallstreetbets, r/stocks, r/investing)
- **Twitter API v2**: Limited free tier for keyword tracking
- **Stocktwits API**: Social sentiment for specific tickers
- **Alternative.me**: Crypto Fear & Greed (if tracking crypto)

#### Screening & Fundamentals
- **Financial Modeling Prep**: Free tier for fundamentals, earnings dates
- **EOD Historical Data**: Free tier for stock screening data
- **Finviz**: Can scrape for screener results (respect rate limits)
- **Yahoo Finance**: Earnings calendar, insider transactions
- **Seeking Alpha**: Can scrape trending articles (rate limited)

### Paid APIs (Optional)
- **Unusual Whales API**: If building commercial product
- **TradingView**: Advanced charting
- **IEX Cloud**: Real-time market data
- **Quiver Quantitative**: Reddit, Congress trading data (mid-tier pricing)

---

## Tech Stack

### Backend
- **Python 3.11+**: Data collection, analysis, alerts
- **FastAPI**: REST API for frontend
- **PostgreSQL**: Historical data storage
- **Redis**: Caching and real-time data
- **Celery**: Scheduled tasks (data fetching, alerts)
- **pandas/numpy**: Data analysis
- **TA-Lib**: Technical analysis library
- **PRAW**: Reddit API wrapper
- **BeautifulSoup/Scrapy**: Web scraping for additional sources
- **NLTK/TextBlob**: Sentiment analysis
- **scikit-learn**: Pattern recognition, clustering

### Frontend
- **React**: UI framework
- **Next.js**: Server-side rendering, routing
- **Tailwind CSS**: Styling
- **Recharts**: Data visualization
- **shadcn/ui**: Component library

### Infrastructure
- **Vercel**: Frontend hosting (free tier)
- **Railway/Render**: Backend hosting ($5-20/month)
- **GitHub Actions**: CI/CD
- **Upstash**: Redis hosting (free tier)

### Monitoring & Alerts
- **Twilio**: SMS alerts (pay-as-you-go)
- **SendGrid**: Email alerts (free tier)
- **Push notifications**: Web push API

---

## MVP Feature Set (2-4 Weeks)

### Dashboard Home
- Current portfolio value
- Months of runway remaining (at $1k/month burn)
- VIX current level with visual indicator
- Market regime status (bull/bear/high volatility)
- **Top momentum opportunities of the day**
- **Trending tickers from WSB (top 5)**

### Defense Tab

#### VIX Monitor
- Real-time VIX tracking
- Alert thresholds: 18 (caution), 25 (elevated), 30+ (crisis)
- Historical chart (1 month, 3 months, 1 year views)
- Notifications via email/SMS

#### Portfolio Tracker
- Manual position entry (stocks, ETFs, options)
- Real-time value updates
- Hedge position tracking (put options, VIX calls)
- P&L visualization
- Allocation breakdown

#### Options Flow (Basic)
- SPY/QQQ unusual volume alerts
- Put/call ratio tracking
- End-of-day summary

#### Macro Dashboard
- Key economic indicators (unemployment, CPI, Fed funds rate)
- FRED data integration
- Historical trends

### Opportunities Tab

#### Momentum Scanner
- Top 20 stocks by momentum (configurable timeframe)
- Price % change (1-day, 5-day, 20-day)
- Volume vs average
- Filters: min price ($5+), min volume (500k+)
- Quick chart preview on hover

#### WSB Tracker
- Top 10 mentioned tickers in last 24 hours
- Sentiment score (bullish/bearish %)
- Comment volume and trend
- Links to top discussions
- Filter out known pump-and-dumps

#### Sector Heat Map
- Visual representation of sector performance
- Daily, weekly, monthly views
- Click through to top stocks in sector

#### Insider Activity
- Recent insider buys (last 7 days)
- Multiple insiders buying same stock (high signal)
- Size of purchases relative to market cap
- Links to SEC filings

### Alert System
- Configurable alert rules (both defensive and offensive)
- Multi-channel delivery (email, SMS, dashboard)
- Alert history and logs
- **New: Momentum breakout alerts**
- **New: WSB trending ticker alerts (when mention spike detected)**

---

## Reddit Scraping Strategy

### Why WallStreetBets?
- High volume, engaged community
- Early signals on retail momentum
- Meme stock identification before mainstream
- Options flow correlates with WSB activity
- Entertainment value while providing data

### Implementation Approach

#### Data Collection
```python
# Using PRAW (Python Reddit API Wrapper)
- Scrape top posts from r/wallstreetbets (hot, top, rising)
- Extract ticker mentions using regex ($TICKER or TICKER format)
- Collect post metadata: upvotes, comments, awards, timestamp
- Scrape top comments for sentiment analysis
- Run every 30-60 minutes during market hours
```

#### Ticker Extraction
- Regex pattern: `\$[A-Z]{1,5}\b` or common ticker patterns
- Filter out false positives (common words like "YOLO", "DD", "CEO")
- Validate against known ticker list
- Track mention frequency and trend (spike detection)

#### Sentiment Analysis
- Keyword scoring: "calls", "moon", "rocket" = bullish
- "puts", "drill", "crash", "worthless" = bearish
- Emoji analysis: 🚀📈💎 = bullish, 📉💩 = bearish
- Comment sentiment aggregation
- Net sentiment score per ticker

#### Quality Filters
**Avoid Pump-and-Dumps:**
- Minimum market cap ($500M+)
- Minimum average volume (1M+ shares daily)
- Check if ticker mentioned in previous week (new mentions are suspect)
- Cross-reference with unusual options activity
- Flag if mentioned by new/low-karma accounts

**Signal Validation:**
- Require multiple independent mentions (not just one viral post)
- Track mention velocity (sudden spike vs sustained interest)
- Correlate with actual price action
- Compare sentiment to options flow (bullish posts + unusual call buying = strong signal)

### Other Subreddits to Monitor
- **r/stocks**: More conservative, fundamental discussions
- **r/investing**: Long-term oriented, quality ideas
- **r/options**: Options strategy discussions
- **r/ValueInvesting**: Contrarian opportunities
- **r/Superstonk, r/DDintoGME**: Specific stock cults (useful for tracking retail concentration)

### Rate Limiting & Ethics
- PRAW respects Reddit API rate limits automatically
- Cache results to minimize requests
- Don't spam or scrape aggressively
- Reddit TOS allows scraping for personal use
- If monetizing, ensure compliance with API terms

### Data Storage
```sql
-- Example schema
CREATE TABLE reddit_mentions (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    subreddit VARCHAR(50),
    mentions_count INTEGER,
    sentiment_score FLOAT,  -- -1 to 1 scale
    post_ids TEXT[],  -- Array of post IDs
    timestamp TIMESTAMP,
    volume_change FLOAT  -- Actual volume vs average
);
```

### Dashboard Display
- **Trending Now**: Top 5 tickers by mention spike
- **Sentiment Gauge**: Visual bullish/bearish indicator
- **Community Confidence**: Based on upvotes, awards, comment sentiment
- **Risk Level**: Pump-and-dump probability score
- **Links**: Direct links to top discussions for due diligence

### Advanced Features (Post-MVP)
- Track specific high-karma users (follow the "smart money" on WSB)
- Correlate WSB activity with actual market outcomes (backtest signals)
- Identify successful pattern: "WSB mentions + unusual options + momentum breakout"
- Alert when WSB sentiment shifts suddenly (contrarian indicator)
- Track SEC investigations (WSB-popular stocks often get scrutinized)

### Important Caveats
⚠️ **WSB is entertainment-first, not financial advice**
- Treat as supplemental signal, not primary strategy
- High noise-to-signal ratio
- Retail sentiment often lags institutional moves
- Meme stocks are high risk/high reward
- Use for pattern recognition, not blindly following

**Best Use Cases:**
- Early detection of retail momentum stocks
- Contrarian indicator (extreme sentiment = reversal)
- Validation tool (cross-reference with your own analysis)
- Risk management (know when retail is crowded into positions)

---

## Development Phases

### Phase 1: Core Infrastructure (Week 1)
- Set up development environment
- Database schema design (add tables for momentum, reddit mentions, insider trades)
- API structure with FastAPI
- Basic frontend scaffolding
- Data fetching pipeline for VIX and portfolio prices
- **Reddit API setup (PRAW credentials)**
- **Yahoo Finance/Alpha Vantage setup for momentum scanning**

### Phase 2: MVP Defensive Features (Week 2)
- VIX monitoring and alerts
- Portfolio tracking
- Basic dashboard UI
- Alert system implementation
- Options flow basics

### Phase 3: MVP Offensive Features (Week 3)
- **Momentum scanner implementation**
- **WSB scraper (top mentions, sentiment)**
- **Insider trading tracker (SEC EDGAR)**
- **Opportunities dashboard UI**
- **Alert rules for breakouts and trending tickers**

### Phase 4: Enhanced Analytics (Week 4)
- Advanced options flow detection
- Macro indicator integration
- Historical data visualization
- Alert rule customization
- **Sector rotation analysis**
- **Pattern recognition basics**

### Phase 5: Polish & Testing (Week 5)
- UI/UX improvements
- Mobile responsiveness
- Performance optimization
- Documentation
- **Backtest WSB signals vs actual returns**
- **Refine pump-and-dump filters**

### Phase 6: Deployment (Week 6)
- Production hosting setup
- Monitoring and logging
- Backup strategy
- Launch!

---

## Potential Monetization

### SaaS Product Ideas
**"FIRE Shield" or "Expat Portfolio Defense"**
- Target market: FIRE community, digital nomads, expats
- Pricing: $10-20/month (undercut Unusual Whales)
- Value prop: Built by someone living the lifestyle
- Marketing: Write about building it, FIRE forums, Reddit

### Content Creation
- Blog posts about development process
- YouTube tutorials on portfolio defense
- Technical writing about market indicators
- Building in public on Twitter/X

### Open Source + Premium
- Core features open source (GitHub stars, portfolio project)
- Premium features: real-time alerts, mobile app, advanced analytics
- Builds credibility and community

---

## Cost Structure (Self-Hosted)

### Development Phase
- $0 (your time during 2-year HYSA runway)
- Learning investment

### Production Running Costs
- Hosting: $10-20/month (Railway/Render + Vercel)
- Database: $0-10/month (Postgres, Redis free tiers)
- SMS alerts: ~$0.01 per message (Twilio)
- Email: Free tier (SendGrid)
- Domain: $10-15/year
- **Total: ~$20-50/month** (vs $100/month for paid services)

### If Monetized
- Stripe fees: 2.9% + $0.30 per transaction
- Customer support time
- Marketing costs (optional)

---

## Success Metrics

### Personal Use
- Reduces monthly subscription costs by $100-200
- Provides confidence in portfolio monitoring (defensive)
- Identifies at least 2-3 quality opportunities per month (offensive)
- Catches at least one major volatility spike with defensive alerts
- Saves time vs manually checking multiple sources
- Successfully filters out pump-and-dumps (no losses from WSB noise)

### SaaS Product
- 10 paying users = breakeven on costs
- 50 paying users = $500-1000/month revenue
- 200 paying users = $2000-4000/month (exceeds Belgrade living costs)
- User retention: 80%+ monthly (sticky product = valuable signals)

---

## Next Steps

1. **Validate MVP concept** - Sketch out dashboard layout
2. **Set up development environment** - Python, Node.js, PostgreSQL
3. **API key registration** - Alpha Vantage, Polygon.io, FRED
4. **Start with VIX alerts** - Simplest, highest value feature
5. **Iterate from there** - Add features based on your actual needs

---

## Resources & Learning

### Technical Documentation
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs
- Alpha Vantage: https://www.alphaavantage.co/documentation/
- Polygon.io: https://polygon.io/docs
- FRED API: https://fred.stlouisfed.org/docs/api/
- PRAW (Reddit): https://praw.readthedocs.io/
- TA-Lib: https://ta-lib.org/

### Financial Concepts
- Options flow interpretation
- VIX calculation and meaning
- Dark pool trading significance
- Market regime analysis
- **Momentum investing principles**
- **Relative strength analysis**
- **Sentiment analysis for trading**
- **Insider trading as signal**

### Research Papers & Books
- "Momentum Investing" by various academic papers
- "What Works on Wall Street" - James O'Shaughnessy
- "Quantitative Momentum" - Wesley Gray
- Studies on social sentiment as trading signal

### Community
- r/algotrading - Algorithmic trading strategies
- r/FIRE - Target user community
- r/ExpatFIRE - Expat-specific discussions
- r/wallstreetbets - Primary data source (and entertainment)
- Hacker News - Technical feedback
- QuantConnect forums - Quant strategy discussions

---

## Notes
- This project perfectly aligns with your Belgrade plan
- Low overhead, high learning value
- Demonstrates both defensive risk management AND offensive opportunity identification
- Shows full-stack capability plus financial domain expertise
- Could become consulting talking point or standalone SaaS business
- Write about the journey for your writing goal (building in public)
- Timeline fits within 2-year HYSA runway
- Combines multiple interests: software, finance, data analysis
- Reddit scraping adds entertainment value while being useful
- Can be used conservatively (just defensive) or aggressively (momentum hunting)
- Positions you as someone who understands both sides of investing: protection and growth
import logging
from typing import List, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class AlertRule(BaseModel):
    id: int
    metric: str  # "VIX", "RSI", "PRICE"
    symbol: Optional[str] = None # e.g. "SPY" (required for RSI/PRICE)
    operator: str # ">", "<"
    value: float
    contact: str
    active: bool = True

# In-memory store for MVP
# In a real app, this would be a DB table
_rules_db: List[AlertRule] = [
    AlertRule(id=1, metric="VIX", operator=">", value=25.0, contact="email@example.com", active=True)
]

class AlertService:
    def get_rules(self) -> List[AlertRule]:
        return _rules_db

    def add_rule(self, rule: AlertRule) -> AlertRule:
        rule.id = len(_rules_db) + 1
        _rules_db.append(rule)
        return rule

    def delete_rule(self, rule_id: int) -> bool:
        global _rules_db
        initial_len = len(_rules_db)
        _rules_db = [r for r in _rules_db if r.id != rule_id]
        return len(_rules_db) < initial_len

    async def check_alerts(self):
        """
        Runs through all active rules and checks if conditions are met.
        Returns a list of triggered alerts (strings) for now.
        """
        triggered = []
        # Import services here to avoid circular imports if any
        # For VIX, we might need to fetch live data or use a cached value
        # For now, let's mock the check logic or fetch from our existing services if possible
        
        # Example: Mock VIX check
        current_vix = 20.0 # TODO: Fetch real VIX
        
        for rule in _rules_db:
            if not rule.active:
                continue
                
            if rule.metric == "VIX":
                is_triggered = False
                if rule.operator == ">" and current_vix > rule.value:
                    is_triggered = True
                elif rule.operator == "<" and current_vix < rule.value:
                    is_triggered = True
                
                if is_triggered:
                    msg = f"[ALERT] VIX is {current_vix} ({rule.operator} {rule.value})"
                    triggered.append(msg)
                    logger.info(msg)
                    
        return triggered

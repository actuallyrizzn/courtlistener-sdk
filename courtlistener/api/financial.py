"""Financial API module for CourtListener SDK."""

from typing import Dict, Any, Optional
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel


class FinancialDisclosure(BaseModel):
    """Model for financial disclosure data."""
    pass


class Investment(BaseModel):
    """Model for investment data."""
    pass


class NonInvestmentIncome(BaseModel):
    """Model for non-investment income data."""
    pass


class FinancialAPI:
    """API client for financial disclosure functionality."""
    
    def __init__(self, client):
        self.client = client
    
    def list_disclosures(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List financial disclosures with optional filtering."""
        params = filters or {}
        return self.client.get('financial-disclosures/', params=params)
    
    def get_disclosure(self, disclosure_id: int) -> FinancialDisclosure:
        """Get a specific financial disclosure by ID."""
        validate_id(disclosure_id)
        data = self.client.get(f'financial-disclosures/{disclosure_id}/')
        return FinancialDisclosure(data) 
"""Financial API module for CourtListener SDK."""

from typing import Dict, Any, Optional, List
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel
from .base import BaseAPI


class FinancialDisclosure(BaseModel):
    """Model for financial disclosure data."""
    pass


class Investment(BaseModel):
    """Model for investment data."""
    pass


class NonInvestmentIncome(BaseModel):
    """Model for non-investment income data."""
    pass


class FinancialAPI(BaseAPI):
    """API client for financial disclosure functionality."""
    
    def __init__(self, client):
        self.client = client
    
    def _get_endpoint(self) -> str:
        """Get the API endpoint for this module."""
        return "financial-disclosures/"
    
    def _get_model_class(self):
        """Get the model class associated with this API."""
        return FinancialDisclosure
    
    def list_disclosures(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List financial disclosures with optional filtering."""
        params = filters or {}
        return self.client.get('financial-disclosures/', params=params)
    
    def get_disclosure(self, disclosure_id: int) -> FinancialDisclosure:
        """Get a specific financial disclosure by ID."""
        validate_id(disclosure_id)
        data = self.client.get(f'financial-disclosures/{disclosure_id}/')
        return FinancialDisclosure(data)

    def list_financial(self, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        params['page'] = page
        return self.client.get('financial-disclosures/', params=params)

    def search_financial(self, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        params['page'] = page
        return self.client.get('financial-disclosures/', params=params)

    def list_financial_disclosures(self, page: int = 1, q: str = None, **filters) -> List[FinancialDisclosure]:
        """List financial disclosures."""
        params = {"page": page}
        if q:
            params["q"] = q
        params.update(filters)
        
        response = self.client._make_request("GET", "/financial-disclosures/", params=params)
        return [FinancialDisclosure(item) for item in response.get("results", [])]
    
    def search_financial_disclosures(self, q: str, page: int = 1, **filters) -> List[FinancialDisclosure]:
        """Search financial disclosures."""
        return self.list_financial_disclosures(page=page, q=q, **filters) 
"""Financial models for CourtListener SDK."""

from .base import BaseModel


class FinancialDisclosure(BaseModel):
    """Model for financial disclosure data."""
    
    def _parse_data(self):
        """Parse financial disclosure data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date_received'):
            self.date_received = self._parse_date(self.date_received)


class Investment(BaseModel):
    """Model for investment data."""
    
    def _parse_data(self):
        """Parse investment data."""
        super()._parse_data()


class NonInvestmentIncome(BaseModel):
    """Model for non-investment income data."""
    
    def _parse_data(self):
        """Parse non-investment income data."""
        super()._parse_data()


class Agreement(BaseModel):
    """Model for agreement data."""
    
    def _parse_data(self):
        """Parse agreement data."""
        super()._parse_data()


class Gift(BaseModel):
    """Model for gift data."""
    
    def _parse_data(self):
        """Parse gift data."""
        super()._parse_data()


class Reimbursement(BaseModel):
    """Model for reimbursement data."""
    
    def _parse_data(self):
        """Parse reimbursement data."""
        super()._parse_data()


class Debt(BaseModel):
    """Model for debt/liability data."""
    
    def _parse_data(self):
        """Parse debt data."""
        super()._parse_data() 
"""Financial models for CourtListener SDK."""

from .base import BaseModel


class FinancialDisclosure(BaseModel):
    """Model for financial disclosure data."""
    
    def _parse_data(self):
        """Parse financial disclosure data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date_received'):
            self.date_received = self._parse_datetime(self.date_received)
        if hasattr(self, 'date_filed'):
            self.date_filed = self._parse_datetime(self.date_filed)


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


class Financial(BaseModel):
    """Model for financial data."""
    
    def _parse_data(self):
        """Parse financial data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date'):
            self.date = self._parse_datetime(self.date)
    
    @property
    def is_filing_fee(self) -> bool:
        """Check if this is a filing fee."""
        return getattr(self, 'type', '').lower() == 'filing_fee'
    
    @property
    def is_costs(self) -> bool:
        """Check if this is costs."""
        return getattr(self, 'type', '').lower() == 'costs'
    
    @property
    def is_damages(self) -> bool:
        """Check if this is damages."""
        return getattr(self, 'type', '').lower() == 'damages'
    
    @property
    def is_positive(self) -> bool:
        """Check if amount is positive."""
        amount = getattr(self, 'amount', 0)
        return amount > 0
    
    @property
    def is_negative(self) -> bool:
        """Check if amount is negative."""
        amount = getattr(self, 'amount', 0)
        return amount < 0
    
    @property
    def amount_formatted(self) -> str:
        """Get formatted amount string."""
        amount = getattr(self, 'amount', 0)
        if not amount:
            return '$0.00'
        
        if amount < 0:
            return f"-${abs(amount):,.2f}"
        return f"${amount:,.2f}"
    
    def __repr__(self) -> str:
        """String representation of the financial record."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            amount = getattr(self, 'amount', 0)
            description = getattr(self, 'description', 'Unknown')
            return f"{class_name}(id={self.id}, amount={amount}, description='{description}')"
        return f"{class_name}()" 
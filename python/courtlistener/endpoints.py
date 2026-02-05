"""
API Endpoint Registry for the CourtListener SDK.

This module centralizes API endpoint paths and handles endpoint module initialization.
"""

from .exceptions import CourtListenerError


class DisabledEndpoint:
    """Placeholder for disabled endpoints."""
    
    def __init__(self, endpoint_name: str, reason: str):
        self.endpoint_name = endpoint_name
        self.reason = reason
    
    def __getattr__(self, name):
        """Raise an informative error for any method call."""
        raise CourtListenerError(
            f"Endpoint '{self.endpoint_name}' is disabled: {self.reason}. "
            f"This endpoint requires special permissions or does not exist in the API."
        )


class EndpointRegistry:
    """Manages API endpoint modules and initialization."""
    
    def __init__(self, client):
        """
        Initialize endpoint registry.
        
        Args:
            client: CourtListener client instance
        """
        self.client = client
        self._init_api_modules()
    
    def _init_api_modules(self):
        """Initialize API endpoint modules."""
        # Import API modules here to avoid circular imports
        from .api.search import SearchAPI
        from .api.dockets import DocketsAPI
        from .api.opinions import OpinionsAPI
        from .api.judges import JudgesAPI
        from .api.courts import CourtsAPI
        from .api.audio import AudioAPI
        from .api.clusters import ClustersAPI
        from .api.positions import PositionsAPI
        from .api.financial import FinancialAPI
        from .api.docket_entries import DocketEntriesAPI
        from .api.attorneys import AttorneysAPI
        from .api.parties import PartiesAPI
        from .api.documents import DocumentsAPI
        from .api.citations import CitationsAPI
        from .api.recap_documents import RecapDocumentsAPI
        from .api.financial_disclosures import FinancialDisclosuresAPI
        from .api.investments import InvestmentsAPI
        from .api.non_investment_incomes import NonInvestmentIncomesAPI
        from .api.agreements import AgreementsAPI
        from .api.gifts import GiftsAPI
        from .api.reimbursements import ReimbursementsAPI
        from .api.debts import DebtsAPI
        from .api.disclosure_positions import DisclosurePositionsAPI
        from .api.spouse_incomes import SpouseIncomesAPI
        from .api.opinions_cited import OpinionsCitedAPI
        from .api.alerts import AlertsAPI
        from .api.docket_alerts import DocketAlertsAPI
        from .api.people import PeopleAPI
        from .api.schools import SchoolsAPI
        from .api.educations import EducationsAPI
        from .api.sources import SourcesAPI
        from .api.retention_events import RetentionEventsAPI
        from .api.aba_ratings import ABARatingsAPI
        from .api.political_affiliations import PoliticalAffiliationsAPI
        from .api.tag import TagAPI
        from .api.recap_fetch import RecapFetchAPI
        from .api.recap_query import RecapQueryAPI
        from .api.originating_court_information import OriginatingCourtInformationAPI
        from .api.fjc_integrated_database import FJCIntegratedDatabaseAPI
        
        # Initialize core API modules
        self.courts = CourtsAPI(self.client)
        self.clusters = ClustersAPI(self.client)
        self.opinions = OpinionsAPI(self.client)
        self.dockets = DocketsAPI(self.client)
        self.judges = JudgesAPI(self.client)
        self.opinion_clusters = self.clusters  # Alias for compatibility
        
        # Available endpoints
        self.positions = PositionsAPI(self.client)
        self.financial = FinancialAPI(self.client)
        self.audio = AudioAPI(self.client)
        self.search = SearchAPI(self.client)
        
        # New endpoints - all available
        self.docket_entries = DocketEntriesAPI(self.client)
        self.attorneys = AttorneysAPI(self.client)
        self.parties = PartiesAPI(self.client)
        self.documents = DocumentsAPI(self.client)
        self.citations = CitationsAPI(self.client)
        self.recap_documents = RecapDocumentsAPI(self.client)
        self.financial_disclosures = FinancialDisclosuresAPI(self.client)
        self.investments = InvestmentsAPI(self.client)
        self.non_investment_incomes = NonInvestmentIncomesAPI(self.client)
        self.agreements = AgreementsAPI(self.client)
        self.gifts = GiftsAPI(self.client)
        self.reimbursements = ReimbursementsAPI(self.client)
        self.debts = DebtsAPI(self.client)
        self.disclosure_positions = DisclosurePositionsAPI(self.client)
        self.spouse_incomes = SpouseIncomesAPI(self.client)
        self.opinions_cited = OpinionsCitedAPI(self.client)
        self.alerts = AlertsAPI(self.client)
        self.docket_alerts = DocketAlertsAPI(self.client)
        self.people = PeopleAPI(self.client)
        self.schools = SchoolsAPI(self.client)
        self.educations = EducationsAPI(self.client)
        self.sources = SourcesAPI(self.client)
        self.retention_events = RetentionEventsAPI(self.client)
        self.aba_ratings = ABARatingsAPI(self.client)
        self.political_affiliations = PoliticalAffiliationsAPI(self.client)
        self.tag = TagAPI(self.client)
        self.recap_fetch = RecapFetchAPI(self.client)
        self.recap_query = RecapQueryAPI(self.client)
        self.originating_court_information = OriginatingCourtInformationAPI(self.client)
        self.fjc_integrated_database = FJCIntegratedDatabaseAPI(self.client)
        
        # Legacy disabled endpoints - now enabled
        self._disabled_endpoints = {}

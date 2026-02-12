"""
API Endpoint Registry for the CourtListener SDK.

Manages initialization and organization of all API endpoint modules.
"""

from typing import Dict, Any
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
    """Manages API endpoint modules and their initialization."""
    
    def __init__(self, client):
        """
        Initialize endpoint registry with client instance.
        
        Args:
            client: CourtListenerClient instance
        """
        self.client = client
        self._endpoints = {}
        self._disabled_endpoints = {}
    
    def initialize_all(self):
        """Initialize all API endpoint modules."""
        # Import all API modules
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
        
        # Core endpoints
        self._endpoints['courts'] = CourtsAPI(self.client)
        self._endpoints['clusters'] = ClustersAPI(self.client)
        self._endpoints['opinions'] = OpinionsAPI(self.client)
        self._endpoints['dockets'] = DocketsAPI(self.client)
        self._endpoints['judges'] = JudgesAPI(self.client)
        
        # Alias for compatibility
        self._endpoints['opinion_clusters'] = self._endpoints['clusters']
        
        # Standard endpoints
        self._endpoints['positions'] = PositionsAPI(self.client)
        self._endpoints['financial'] = FinancialAPI(self.client)
        self._endpoints['audio'] = AudioAPI(self.client)
        self._endpoints['search'] = SearchAPI(self.client)
        
        # Extended endpoints
        self._endpoints['docket_entries'] = DocketEntriesAPI(self.client)
        self._endpoints['attorneys'] = AttorneysAPI(self.client)
        self._endpoints['parties'] = PartiesAPI(self.client)
        self._endpoints['documents'] = DocumentsAPI(self.client)
        self._endpoints['citations'] = CitationsAPI(self.client)
        self._endpoints['recap_documents'] = RecapDocumentsAPI(self.client)
        self._endpoints['financial_disclosures'] = FinancialDisclosuresAPI(self.client)
        self._endpoints['investments'] = InvestmentsAPI(self.client)
        self._endpoints['non_investment_incomes'] = NonInvestmentIncomesAPI(self.client)
        self._endpoints['agreements'] = AgreementsAPI(self.client)
        self._endpoints['gifts'] = GiftsAPI(self.client)
        self._endpoints['reimbursements'] = ReimbursementsAPI(self.client)
        self._endpoints['debts'] = DebtsAPI(self.client)
        self._endpoints['disclosure_positions'] = DisclosurePositionsAPI(self.client)
        self._endpoints['spouse_incomes'] = SpouseIncomesAPI(self.client)
        self._endpoints['opinions_cited'] = OpinionsCitedAPI(self.client)
        self._endpoints['alerts'] = AlertsAPI(self.client)
        self._endpoints['docket_alerts'] = DocketAlertsAPI(self.client)
        self._endpoints['people'] = PeopleAPI(self.client)
        self._endpoints['schools'] = SchoolsAPI(self.client)
        self._endpoints['educations'] = EducationsAPI(self.client)
        self._endpoints['sources'] = SourcesAPI(self.client)
        self._endpoints['retention_events'] = RetentionEventsAPI(self.client)
        self._endpoints['aba_ratings'] = ABARatingsAPI(self.client)
        self._endpoints['political_affiliations'] = PoliticalAffiliationsAPI(self.client)
        self._endpoints['tag'] = TagAPI(self.client)
        self._endpoints['recap_fetch'] = RecapFetchAPI(self.client)
        self._endpoints['recap_query'] = RecapQueryAPI(self.client)
        self._endpoints['originating_court_information'] = OriginatingCourtInformationAPI(self.client)
        self._endpoints['fjc_integrated_database'] = FJCIntegratedDatabaseAPI(self.client)
    
    def get_endpoint(self, name: str) -> Any:
        """
        Get an API endpoint module by name.
        
        Args:
            name: Endpoint name
        
        Returns:
            API module instance
        
        Raises:
            AttributeError: If endpoint not found
        """
        if name in self._endpoints:
            return self._endpoints[name]
        elif name in self._disabled_endpoints:
            return self._disabled_endpoints[name]
        else:
            raise AttributeError(f"Endpoint '{name}' not found")
    
    def disable_endpoint(self, name: str, reason: str):
        """
        Disable an endpoint.
        
        Args:
            name: Endpoint name
            reason: Reason for disabling
        """
        self._disabled_endpoints[name] = DisabledEndpoint(name, reason)
    
    def list_endpoints(self) -> Dict[str, Any]:
        """
        List all available endpoints.
        
        Returns:
            Dictionary of endpoint names and their modules
        """
        return self._endpoints.copy()
    
    def __getattr__(self, name: str) -> Any:
        """Allow direct attribute access to endpoints."""
        return self.get_endpoint(name)

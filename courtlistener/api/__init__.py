"""
API endpoint modules for the CourtListener SDK.
"""

from .search import SearchAPI
from .dockets import DocketsAPI
from .opinions import OpinionsAPI
from .judges import JudgesAPI
from .courts import CourtsAPI
from .parties import PartiesAPI
from .attorneys import AttorneysAPI
from .documents import DocumentsAPI
from .audio import AudioAPI
from .financial import FinancialAPI
from .citations import CitationsAPI
from .clusters import ClustersAPI
from .positions import PositionsAPI
from .docket_entries import DocketEntriesAPI
from .recap_documents import RecapDocumentsAPI
from .financial_disclosures import FinancialDisclosuresAPI
from .investments import InvestmentsAPI
from .non_investment_incomes import NonInvestmentIncomesAPI
from .agreements import AgreementsAPI
from .gifts import GiftsAPI
from .reimbursements import ReimbursementsAPI
from .debts import DebtsAPI
from .disclosure_positions import DisclosurePositionsAPI
from .spouse_incomes import SpouseIncomesAPI
from .opinions_cited import OpinionsCitedAPI
from .alerts import AlertsAPI
from .docket_alerts import DocketAlertsAPI
from .people import PeopleAPI
from .schools import SchoolsAPI
from .educations import EducationsAPI
from .sources import SourcesAPI
from .retention_events import RetentionEventsAPI
from .aba_ratings import ABARatingsAPI
from .political_affiliations import PoliticalAffiliationsAPI
from .tag import TagAPI
from .recap_fetch import RecapFetchAPI
from .recap_query import RecapQueryAPI
from .originating_court_information import OriginatingCourtInformationAPI
from .fjc_integrated_database import FJCIntegratedDatabaseAPI

__all__ = [
    "SearchAPI",
    "DocketsAPI",
    "OpinionsAPI",
    "JudgesAPI",
    "CourtsAPI",
    "PartiesAPI",
    "AttorneysAPI",
    "DocumentsAPI",
    "AudioAPI",
    "FinancialAPI",
    "CitationsAPI",
    "ClustersAPI",
    "PositionsAPI",
    "DocketEntriesAPI",
    "RecapDocumentsAPI",
    "FinancialDisclosuresAPI",
    "InvestmentsAPI",
    "NonInvestmentIncomesAPI",
    "AgreementsAPI",
    "GiftsAPI",
    "ReimbursementsAPI",
    "DebtsAPI",
    "DisclosurePositionsAPI",
    "SpouseIncomesAPI",
    "OpinionsCitedAPI",
    "AlertsAPI",
    "DocketAlertsAPI",
    "PeopleAPI",
    "SchoolsAPI",
    "EducationsAPI",
    "SourcesAPI",
    "RetentionEventsAPI",
    "ABARatingsAPI",
    "PoliticalAffiliationsAPI",
    "TagAPI",
    "RecapFetchAPI",
    "RecapQueryAPI",
    "OriginatingCourtInformationAPI",
    "FJCIntegratedDatabaseAPI",
] 
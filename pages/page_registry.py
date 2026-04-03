from __future__ import annotations

from collections.abc import Mapping

from pages.a11y_page import A11yPage
from pages.auth_page import AuthPage
from pages.base_page import BasePage
from pages.components_page import ComponentsPage
from pages.dynamic_page import DynamicPage
from pages.errors_page import ErrorsPage
from pages.experiments_page import ExperimentsPage
from pages.files_page import FilesPage
from pages.forms_page import FormsPage
from pages.grpc_page import GrpcPage
from pages.home_page import HomePage
from pages.i18n_page import I18nPage
from pages.integrations_page import IntegrationsPage
from pages.mobile_page import MobilePage
from pages.performance_page import PerformancePage
from pages.system_page import SystemPage
from pages.tables_page import TablesPage


PAGE_CLASSES: tuple[type[BasePage], ...] = (
    HomePage,
    AuthPage,
    FormsPage,
    TablesPage,
    DynamicPage,
    FilesPage,
    A11yPage,
    I18nPage,
    SystemPage,
    IntegrationsPage,
    PerformancePage,
    ErrorsPage,
    ExperimentsPage,
    ComponentsPage,
    MobilePage,
    GrpcPage,
)

PAGE_REGISTRY: Mapping[str, type[BasePage]] = {
    page_class.route_name(): page_class for page_class in PAGE_CLASSES
}


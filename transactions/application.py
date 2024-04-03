from petisco_sanic.extra.sanic.application.sanic_application import SanicApplication

from . import (
    APPLICATION_LATEST_DEPLOY,
    APPLICATION_NAME,
    APPLICATION_VERSION,
    ORGANIZATION,
    ACCOUNTS_ORGANIZATION,
    ACCOUNTS_APP_NAME
)
from transactions.configurer import sanic_configurer
from transactions.petisco_config.configurers import configurers
from transactions.petisco_config.dependencies import dependencies_provider

application = SanicApplication(
    name=APPLICATION_NAME,
    version=APPLICATION_VERSION,
    organization=ORGANIZATION,
    deployed_at=APPLICATION_LATEST_DEPLOY,
    dependencies_provider=dependencies_provider,
    configurers=configurers,
    sanic_configurer=sanic_configurer,
)
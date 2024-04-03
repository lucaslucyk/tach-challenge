import os
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def read_application_latest_deploy(filename: str) -> datetime:
    deploy_time = open(filename).read().rstrip()
    return datetime.strptime(deploy_time[:-6], TIME_FORMAT)


def read_application_version(filename: str) -> str:
    return open(filename).read().rstrip()


ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
ORGANIZATION = "tach"
APPLICATION_NAME = "transactions-app"
ACCOUNTS_ORGANIZATION = "tach"
ACCOUNTS_APP_NAME = "accounts-app"
APPLICATION_VERSION = read_application_version(f"{ROOT_PATH}/VERSION")
APPLICATION_LATEST_DEPLOY = read_application_latest_deploy(f"{ROOT_PATH}/DEPLOY")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local").lower()
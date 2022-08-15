from datetime import datetime
import base64
import httpx
import os

from ...controllers.configuration import ConfigurationController
from ...utils.constants import CFG_KEY_LAST_ISSUE_DATE_TIME
from ...utils.constants import REDMINE_ISSUES_PATH
from ...utils.constants import REDMINE_URL

class RedmineNewIssuesWrapper():
    """
    Wrapper to get all new Issues from Redmine

    """

    async def get_new_issues(self, last_date_time=None, include_closed=True):
        if last_date_time is None:
            configController = ConfigurationController()

            dft_last_date_time = datetime(1900, 1, 1, 0, 0, 0)
            last_date_time = await configController.get_configuration(
                CFG_KEY_LAST_ISSUE_DATE_TIME, dft_last_date_time
            )

        return await self.__get_redmine_issues(last_date_time, include_closed)

    async def __get_redmine_issues(self, last_date_time=None,
                                   include_closed=True):
        result = []
        status_filter = ""
        if include_closed:
            status_filter = "status_id=*"
        created_filter = ""
        if last_date_time is not None:
            created_filter = "created_on=%3E%3D" + \
                last_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        search_str = "?sort=created_on&" + (status_filter + "&" if status_filter else "") + \
            created_filter

        async with httpx.AsyncClient() as client:
            url_to_call = os.environ.get(REDMINE_URL) + \
                REDMINE_ISSUES_PATH + search_str

            r = await client.get(url_to_call)
            result = r.json().get("issues", [])

        return result
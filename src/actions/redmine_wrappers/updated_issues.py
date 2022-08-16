from datetime import datetime
import base64
import httpx
import os

from ...controllers.configuration import ConfigurationController
from ...utils.constants import CFG_KEY_LAST_UPDATED_ISSUE_DATE_TIME
from ...utils.constants import REDMINE_ISSUES_PATH
from ...utils.constants import REDMINE_URL

class RedmineUpdatedIssuesWrapper():
    """
    Wrapper to get all updated Issues from Redmine

    """

    async def get_updated_issues(self, last_date_time=None, include_closed=True):
        if last_date_time is None:
            configController = ConfigurationController()

            dft_last_date_time = datetime(1900, 1, 1, 0, 0, 0)
            last_date_time = await configController.get_configuration(
                CFG_KEY_LAST_UPDATED_ISSUE_DATE_TIME, dft_last_date_time
            )

        return await self.__get_redmine_updated_issues(last_date_time, include_closed)

    async def __get_redmine_updated_issues(self, last_date_time=None,
                                   include_closed=True):
        result = []
        status_filter = ""
        if include_closed:
            status_filter = "status_id=*"
        updated_filter = ""
        if last_date_time is not None:
            updated_filter = "updated_on=%3E%3D" + \
                last_date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        search_str = "?sort=updated_on&" + (status_filter + "&" if status_filter else "") + \
            updated_filter

        async with httpx.AsyncClient() as client:
            url_to_call = os.environ.get(REDMINE_URL) + \
                REDMINE_ISSUES_PATH + search_str

            r = await client.get(url_to_call)
            result = r.json().get("issues", [])

        return result
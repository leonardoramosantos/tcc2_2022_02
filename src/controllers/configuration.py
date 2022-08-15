from ..utils.constants import TB_CONFIG_KEY
from ..utils.constants import TB_CONFIG_VALUE
from ..utils.db_connection import db_prediction_mechanism

class ConfigurationController():
    """
    Wrapper to operate on the Database using Models

    """

    def __init__(self):
        self.cfg_collection = db_prediction_mechanism["app_configuration"]

    async def get_configuration(self, cfg_key, dft_value):
        result = dft_value

        cfg_filter = {
            TB_CONFIG_KEY: cfg_key
        }

        find_result = await self.cfg_collection.find_one(cfg_filter)
        if find_result:
            result = find_result[TB_CONFIG_VALUE]

        return result

    async def save_configuration(self, cfg_key, cfg_value):
        cfg_filter = {
            TB_CONFIG_KEY: cfg_key
        }

        cfg_update = {
            "$set": {
                TB_CONFIG_KEY: cfg_key,
                TB_CONFIG_VALUE: cfg_value
            }
        }

        result = await self.cfg_collection.update_one(cfg_filter, 
                                                      cfg_update,
                                                      True)

        return result.raw_result.get(TB_CONFIG_VALUE)
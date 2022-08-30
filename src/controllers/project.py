from ..utils.db_connection import db_prediction_mechanism

class ProjectController:
    """
    Wrapper to operate on the Database using Models

    """

    def __init__(self):
        self.project_collec = db_prediction_mechanism["project"]

    async def save_existing_project(self, project_to_save):
        project_to_save_dict = {k: v for k, v in project_to_save.dict().items() \
            if v is not None}

        project_filter = {
            "_id": project_to_save.id
        }

        project_update = {
            "$set": project_to_save_dict
        }

        await self.project_collec.update_one(project_filter,
                                             project_update,
                                             True)

        return await self.project_collec.find_one(project_filter)
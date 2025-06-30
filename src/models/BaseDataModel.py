from helpers.config import get_settings, Settings

class BaseDataModel:

    def __init__(self, db_client: object):
        self.db_client = db_client
        self.app_settings = get_settings()


    async def create_indexes(self, indexes: list[dict]):
        """
        indexes: a list of dicts, each with keys:
          - "key": the index spec (e.g. [("field", 1)])
          - "name": the index name
          - "unique": bool
        """
        for idx in indexes:
            await self.collection.create_index(
                idx["key"],
                name=idx["name"],
                unique=idx.get("unique", False)
            )
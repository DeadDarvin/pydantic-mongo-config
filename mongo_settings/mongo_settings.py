from pydantic_settings import BaseSettings
from cachetools import TTLCache
from pymongo import MongoClient
from pymongo.collection import Collection

from .attributes import FromMongo


class MongoEnvMixin:
    """
    Special handler for FromMongo attributes.
    Set connection with MongoDB collection.
    Use cache for variables from MongoDB.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        m_con = self.MongoConnector
        self._env_collection = self._get_env_collection(
            db=m_con.db,
            collection=m_con.collection,
            creds=m_con.creds
        )
        self._cache = TTLCache(maxsize=64, ttl=120)

    def __getattribute__(self, item):
        field = super().__getattribute__(item)
        if not isinstance(field, FromMongo):
            return field
        try:
            return self._cache[item]
        except KeyError:
            value = field.get(self._env_collection, item)
        if value is None:
            raise AttributeError(
                f'{type(self).__name__!r} object has no attribute {item!r}'
            )
        self._cache[item] = value
        return value

    @staticmethod
    def _get_env_collection(db: str, collection: str, creds: BaseSettings) -> Collection:
        client = MongoClient(
            host=creds.host,
            port=creds.port,
            username=creds.username,
            password=creds.password
        )
        db = client[db]
        collection = db[collection]
        return collection


class FromMongoSettings(MongoEnvMixin, BaseSettings):
    """
    Base class for access to variables from MongoDB.
    """
    def __init__(self, *args, **kwargs):
        try:
            self.MongoConnector
        except AttributeError:
            raise AttributeError(
                f"{type(self).__name__!r} object has not required attribute 'MongoConnector'"
            )
        super().__init__(*args, **kwargs)


__all__ = [
    'FromMongoSettings'
]

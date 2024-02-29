import os, enum, string, dotenv
from bson import ObjectId
from pymongo import *
import pymongo
from pymongo.database import Database, Collection

from ..constants.config import FROM_NAME, LOGGER
from ..utils.base import Singleton
from ..utils.commons import get_id, get_timestamp, hash_bcrypt


dotenv.load_dotenv()


class Model:
    property_to_remove_on_db_dump = ["models"]

    def __init__(
        self,
        models: "Models",
        _id: str = "",
        id: str = "",
        created_timestamp: int = 0,
        **kwargs,
    ) -> None:
        self.models = models

        self._id = _id
        self.id = id
        self.created_timestamp = created_timestamp

    @property
    def dict(self) -> dict:
        d = {}
        for k, v in self.__dict__.items():
            if isinstance(v, enum.Enum):
                v = v.value
            if k not in self.property_to_remove_on_db_dump:
                d[k] = v
        return d

    @property
    def db_dump(self) -> dict:
        _dict = self.dict
        del _dict["_id"]
        return _dict

    def save(self):
        self.models.update_child(self)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and value:
                setattr(self, key, value)
        self.save()


class Models(Singleton):
    model_class = Model
    MONGO: MongoClient = None
    DATABASE: Database = None

    def __init__(self):
        Singleton.__init__(self)

        if not Models.MONGO:
            mongodb = os.environ.get("mongodb")

            LOGGER.info(f"Connecting to MongoDB on {mongodb}.")
            Models.MONGO = MongoClient(mongodb)
            Models.MONGO.admin.command("ping")
            Models.DATABASE = Models.MONGO[FROM_NAME]

            LOGGER.info(
                "Pinged your deployment. You successfully connected to MongoDB!"
            )
        else:
            collections = Models.DATABASE.list_collection_names()
            if self.name not in collections:
                Models.DATABASE.create_collection(self.name)

        self.collection.create_index("id", unique=True)

    @property
    def name(self) -> str:
        underscore = "_"
        ns = ""
        for n in self.__class__.__name__:
            if n in string.ascii_uppercase:
                n = f"{underscore}{n.lower()}"
            ns += n
        ns = ns.strip(underscore)
        return ns

    @property
    def collection(self) -> Collection:
        return Models.DATABASE[self.name]

    def exists(self, id: str) -> bool:
        return self.child_exists("id", id)

    def child_exists(self, key: str, value: str) -> bool:
        c = self.collection.count_documents({key: value})
        return bool(c)

    def child(self, key: str, value: str):
        return self.find_one({key: value})

    def find_child(self, id: str) -> Model | None:
        return self.find_one({"id": id})

    def delete_child(self, id: str):
        self.collection.delete_one({"_id": ObjectId(id)})
        return True

    def create(
        self,
        id: str = "",
        created_timestamp: int = 0,
        **kwargs,
    ) -> Model:
        if password := kwargs.get("password"):
            kwargs.update(password=hash_bcrypt(password))

        if pin := kwargs.get("pin"):
            kwargs.update(pin=hash_bcrypt(pin))

        kwargs.update(
            id=id or get_id(),
            created_timestamp=created_timestamp or get_timestamp(),
        )

        model = self.model_class(self, **kwargs)
        p = self.collection.insert_one(model.db_dump)
        model._id = str(p.inserted_id)

        return model

    def find(
        self,
        filters: dict = {},
        limit: int = 0,
        skip: int = 0,
        sort: list[str] | str = None,
        descending: bool = False,
        search_or: list = [],
        search_and: list = [],
        count: bool = False,
    ):
        if search_or:
            filters["$or"] = search_or

        if search_and:
            filters["$and"] = search_and

        if count:
            return self.collection.count_documents(filters)

        items = self.collection.find(filters)
        if skip:
            items = items.skip(skip)
        if limit:
            items = items.limit(limit)
        if sort:
            items = items.sort(
                sort,
                direction=pymongo.DESCENDING if descending else pymongo.ASCENDING,
            )
        items = list(items)
        # print(items)
        return [self.model_class(self, **item) for item in items]

    def find_one(
        self,
        filters: dict = {},
        search_or: list = [],
        search_and: list = [],
    ):
        if search_or:
            filters["$or"] = search_or

        if search_and:
            filters["$and"] = search_and

        one = self.collection.find_one(filters)
        if one:
            return self.model_class(self, **one)

    def update_child(self, child: Model):
        self.collection.update_one(
            {"_id": ObjectId(child._id)}, {"$set": child.db_dump}
        )

    def drop(self):
        self.collection.drop()

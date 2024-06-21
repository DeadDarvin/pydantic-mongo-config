from typing import Any, TypeAlias, Type, NoReturn
from pymongo.collection import Collection
from pydantic_core import ValidationError, InitErrorDetails, PydanticCustomError


AllowedType: TypeAlias = float | list | set | dict


class FromMongo:
    def __init__(self, _type: Type[AllowedType],  default: Any | None = None):
        self.env_type = _type
        self.default = default

    def get(self, collection: Collection, env_name: str) -> AllowedType | NoReturn:
        res = collection.find_one({"key": env_name})
        if res is None:
            return self.default
        value = res["value"]
        try:
            return self.env_type(value)
        except (TypeError, ValueError):
            raise ValidationError.from_exception_data(
                title=type(self).__name__,
                line_errors=[
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "mongo_parsing",
                            f"Input should be a valid {self.env_type.__name__}, "
                            f"unable to parse {value} as an {self.env_type.__name__}"
                        )
                    )
                ]
            )
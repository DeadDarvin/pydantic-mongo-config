# pydantic-mongo-config
Extends the BaseSettings interface from the pydantic_settings library. Provides convenient access to constants from MongoDB, while preserving the full functionality of BaseSettings.


## Instruction
### 1. Import
```python
from pydantic_settings import BaseSettings
from pydantic_mongo_config import FromMongoSettings, FromMongo
```
### 2. Create BaseSettings contains mongo credentials.
```python
class MongoCreds(BaseSettings):
    MONGO_DB_ADDRESS: str
    MONGO_DB_PORT: int
    MONGO_DB_USER: str
    MONGO_DB_PASSWORD: str

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'
```
### 3. Create any standard Settings contains your variables. Inherit from FromMongoSettings
```python
class Settings(FromMongoSettings):
    HARDCODE_ENV: str = 'value'
    FROM_FILE_ENV: str

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
```
### 4. Add required MongoConnector subclass
```python
class Settings(FromMongoSettings):
    ...
    
    class MongoConnector:
        db = "YourDB"
        collection = "envsCollection"
        creds = MongoCreds()
```
### 5. Use FromMongo for declare attribute as field from MongoDB
```python
class Settings(FromMongoSettings):
    FROM_MONGO_ENV: FromMongo = FromMongo(str, "Any default value")
```
### 6. Result
```python
from pydantic_settings import BaseSettings
from pydantic_mongo_config import FromMongoSettings, FromMongo


class MongoCreds(BaseSettings):
    MONGO_DB_ADDRESS: str
    MONGO_DB_PORT: int
    MONGO_DB_USER: str
    MONGO_DB_PASSWORD: str

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'

        
class Settings(FromMongoSettings):
    HARDCODE_ENV: str = 'value'
    FROM_FILE_ENV: str
    FROM_MONGO_ENV: FromMongo = FromMongo(str, "Any default value")
    
    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'

    class MongoConnector:
        db = "YourDB"
        collection = "envsCollection"
        creds = MongoCreds()
```
### 7. Access an attribute
```python
settings = Settings()
settings.FROM_MONGO_ENV
```
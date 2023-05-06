from typing import List, Dict, Union, Optional
from pydantic import BaseModel, BaseSettings, root_validator


class WebTask(BaseModel):
    url: str

    class Config:
        extra = 'allow'
        

# Storage
class StorageConfig(BaseSettings):
    storage_type = 'mongo'
    # dev database connection string
    mongo_conn: str = ''
    blob_conn: str = ''
    db_name: str = ''
    query: Union[Dict, str, None] = None

    class Config:
        fields = {
            'conn_str': {'env': 'MONGO_CONN'}
        }
        extra = 'allow'


class SpiderConfig(BaseSettings):
    headers: Dict = {'User-Agent': 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36'}
    user_agent: str = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36'
    environment: str = 'local_pc_wsl'
    storage_config: BaseSettings = None

    @root_validator
    def estab_storage(cls, values):
        if values['environment'] == 'local_pc_wsl':
            values['storage_config'] = StorageConfig()
        else:
            raise RuntimeError(f'Unsupported storage: {values["environment"]}')
        return values
    
    class Config:
        extra = 'allow'


class PlaywrightSpiderConfig(SpiderConfig):
    
    class Config:
        extra = 'ignore'


class ParserConfig(BaseSettings):
    ...


if __name__ == '__main__':
    config = PlaywrightSpiderConfig()
    print(config.dict())
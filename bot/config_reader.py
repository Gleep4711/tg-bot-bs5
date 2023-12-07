from typing import Optional
from enum import Enum

from pydantic import BaseModel, RedisDsn, SecretStr, field_validator, FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Redis(BaseModel):
    host: str
    port: int = 6379
    db: int


class FSMMode(str, Enum):
    MEMORY = 'memory'
    REDIS = 'redis'


class Settings(BaseSettings):
    bot_token: SecretStr
    fsm_mode: str
    redis: Optional[RedisDsn] = None
    admin: int
    logs_channel_id: int
    logs_error_channel_id: int
    bot_manager_chat_id: int
    bots_manager_group_id_main_chat: int
    bs_id: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    @field_validator('redis', mode='after')
    @classmethod
    def skip_validating_redis(cls, v: Optional[RedisDsn], info: FieldValidationInfo):
        if info.data.get('fsm_mode') == FSMMode.REDIS and v is None:
            err = 'FSM Mode is set to "Redis", but Redis DNS is missing!'
            raise ValueError(err)
        return v

    # @validator("fsm_mode")
    # def fsm_type_check(cls, v):
    #     if v not in ("memory", "redis"):
    #         raise ValueError("Incorrect fsm_mode. Must be one of: memory, redis")
    #     return v

    # @validator("redis")
    # def skip_validating_redis(cls, v, values):
    #     if values["fsm_mode"] == "redis" and v is None:
    #         raise ValueError("Redis config is missing, though fsm_type is 'redis'")
    #     return v

    # class Config:
    #     env_file = '.env'
    #     env_file_encoding = 'utf-8'
    #     env_nested_delimiter = '__'


config = Settings()

from typing import TYPE_CHECKING

from bisheng.services.cache.service import BaseCacheService, InMemoryCache, RedisCache
from bisheng.services.factory import ServiceFactory
from bisheng.utils.logger import logger

if TYPE_CHECKING:
    from bisheng.services.settings.service import SettingsService


class CacheServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(BaseCacheService)

    def create(self, settings_service: 'SettingsService'):
        # Here you would have logic to create and configure a CacheService
        # based on the settings_service

        if settings_service.settings.CACHE_TYPE == 'redis':
            logger.debug('Creating Redis cache')
            redis_cache = RedisCache(
                host=settings_service.settings.REDIS_HOST,
                port=settings_service.settings.REDIS_PORT,
                db=settings_service.settings.REDIS_DB,
                expiration_time=settings_service.settings.REDIS_CACHE_EXPIRE,
            )
            if redis_cache.is_connected():
                logger.debug('Redis cache is connected')
                return redis_cache
            logger.warning('Redis cache is not connected, falling back to in-memory cache')
            return InMemoryCache()

        elif settings_service.settings.CACHE_TYPE == 'memory':
            return InMemoryCache()

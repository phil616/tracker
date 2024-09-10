from response.std import URFRouter
from fastapi import Depends
from core.cache import get_global_kv, MemStorage
from pydantic import BaseModel
from fastapi import Security
from core.authorize import check_permissions
class CacheItem(BaseModel):
    key:str
    value:str

cache_router = URFRouter(prefix="/cache",dependencies=[Security(check_permissions,scopes=["system:read","system:write"])])

@cache_router.get("/get/{key}")
def get_cache(key:str, cache:MemStorage = Depends(get_global_kv)):
    return cache.get_value(key)

@cache_router.post("/set")
async def set_cache(item:CacheItem, cache:MemStorage = Depends(get_global_kv)):
    cache.set_value(item.key, item.value)
    return {"success":True}

@cache_router.delete("/delete/{key}")
def delete_cache(key:str, cache:MemStorage = Depends(get_global_kv)):
    cache.delete_value(key)
    return {"success":True}

@cache_router.get("/all")
def get_all_cache(cache:MemStorage = Depends(get_global_kv)):
    return cache.get_all_values()
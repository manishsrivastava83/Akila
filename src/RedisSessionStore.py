import asyncio
import asyncio_redis
from asyncio_redis import RedisProtocol
import time
import  pickle
from uuid import uuid4
import time

class RedisSessionStore:
    __shared_state = {}
    def __init__(self, **options):
        self.__dict__ = self.__shared_state
        self.options = {
            'key_prefix': 'session',
            'expire': 7200,
        }
        self.options.update(options)
        self.redis_connection_pool = None
        print(self.redis_connection_pool)
    
    async def get_redis_pool(self):
        if not self.redis_connection_pool:
            self.redis_connection_pool = await asyncio_redis.Pool.create(
                host='localhost', port=6379, poolsize=10
            )
        return self.redis_connection_pool

    #def foo(self):
    #    return getattr(RedisProtocol(),name)
    #def __getattr__(self, name):
    #    # Only proxy commands.
    #    if name not in _all_commands:
    #        raise AttributeError

    #    return getattr(self.protocol, name)

    #def __repr__(self):
    #    return 'Connection(host=%r, port=%r)' % (self.host, self.port)

    #@asyncio.coroutine 
    #def rpop(self,key,value):
    #    print('set_session')
    #    connection = yield from self.get_redis_pool()
    #    yield from connection.blpop(key,value)

    #@asyncio.coroutine 
    #def set(self,key,value):
    #    print('set_session')
    #    connection = yield from self.get_redis_pool()
    #    yield from connection.set(key,value)

    #@asyncio.coroutine 
    #def append(self,key,value):
    #    print('set_session')
    #    connection = yield from self.get_redis_pool()
    #    yield from connection.append(key,value)

    #@asyncio.coroutine 
    #def get(self,key):
    #    print('get_session')
    #    val = yield from self.redis_connection_pool.get(key)
    #    return val


@asyncio.coroutine 
def foo_test():
    redisSessionStore = RedisSessionStore()
    connection = yield from redisSessionStore.get_redis_pool()
    #connection = redisSessionStore.get_redis_pool()
    yield from connection.set('myKey','myValue1')
    val = yield from connection.get('myKey')
    print(val)
    yield from connection.flushdb()
    yield from connection.flushall()
    #val = yield from connection.get('myKey')
    #print(val)
    subjects = ['physics', 'chemistry', 'maths', 'biology'];
    yield from connection.lpush('mySubjects',subjects)
    #yield from connection.lpush('mySubjects',list('maths'))
    #yield from connection.lpush('mySubjects',list('physics'))
    #yield from connection.lpush('mySubjects',list('biology'))
    listReply= yield from connection.lrange('mySubjects')
    myList = listReply.aslist()
    print(myList)
    for f in listReply:
        item = yield from f
        print(item)

#@asyncio.coroutine 
#def foo():
#    connection1 = yield from redisSessionStore.get_redis_pool()
#    yield from connection1.flushdb()
#    yield from connection1.flushall()
#    for i in range(1000):
#        connection = yield from redisSessionStore.get_redis_pool()
#        #yield from connection.set(str(i),str(i))
#        #yield from connection.append(str(i),str(i))
#        val = yield from connection.get(str(i))
#
#
#        #loop.run_until_complete(redisSessionStore.set(str(i),str(i)))
#        #loop.run_until_complete(redisSessionStore.append(str(i),str(i)))
#        #val = loop.run_until_complete(redisSessionStore1.get(str(i)))
#        print(val)
# 
#
#loop = asyncio.get_event_loop()
##future = asyncio.Future()
##asyncio.ensure_future(redisSessionStore.set_session(future))
#redisSessionStore = RedisSessionStore()
#redisSessionStore1 = RedisSessionStore()
##val=redisSessionStore1.foo()
#loop.run_until_complete(foo_test())
#time.sleep(500)
##print(future.result())
#loop.close()

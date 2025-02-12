import redis

r = redis.StrictRedis(host='172.17.0.2', port=6379, decode_responses=True)
r.set('test', 'value')
print(r.get('test'))
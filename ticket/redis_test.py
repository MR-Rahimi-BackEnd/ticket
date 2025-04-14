import redis


r = redis.Redis(host='localhost', port=6379, db=0)


r.set('greeting', 'salam mohammadreza')

value = r.get('greeting')

print(value.decode())

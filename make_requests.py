import urllib.request
import time

print("Making requests in 1 second...")
time.sleep(1)

for route in ['/', '/test', '/health']:
    try:
        urllib.request.urlopen(f'http://127.0.0.1:3000{route}')
    except:
        pass
    time.sleep(0.2)
print("Done")

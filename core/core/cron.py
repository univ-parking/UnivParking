def crontab_every_minute():
    import requests

    url = 'http://localhost:8000/api/v1/parking/'
    res = requests.get(url)
    print(res.json())


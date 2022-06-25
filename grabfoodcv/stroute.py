def get_coordinates(cities):
  coordinates = []
  import http.client, urllib.parse
  import json
  conn = http.client.HTTPConnection('api.positionstack.com')
  for city in cities:
    params = urllib.parse.urlencode({
        'access_key': '3327d83d1f4f3dcbd5b50579808e69e4',
        'query': city,
        'limit': 1,
        })

    conn.request('GET', '/v1/forward?{}'.format(params))

    res = conn.getresponse()
    data = res.read()
    data = data.decode('utf-8')
    coordinate = (json.loads(data)['data'][0]['longitude'],json.loads(data)['data'][0]['latitude'])
    coordinates.append(coordinate)
  return coordinates

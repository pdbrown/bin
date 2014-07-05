import sys
import httplib
import re

zip_code = 94043

conn = httplib.HTTPConnection('wsf.cdyne.com')
body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <GetCityWeatherByZIP xmlns="http://ws.cdyne.com/WeatherWS/">
      <ZIP>%d</ZIP>
    </GetCityWeatherByZIP>
  </soap:Body>
</soap:Envelope>""" % zip_code
headers = {
        'Host': 'wsf.cdyne.com',
        'Content-Type': 'text/xml; charset=utf-8',
        'Content-Length': len(body),
        'SOAPAction': 'http://ws.cdyne.com/WeatherWS/GetCityWeatherByZIP'
}

conn.request('POST', '/WeatherWS/Weather.asmx', body, headers)
response = conn.getresponse()
if not response.status == httplib.OK:
    print response.status
    sys.exit(1)

temp_match = re.search(r'<Temperature>(.*)</Temperature>', response.read())
if temp_match:
    print temp_match.group(1)
else:
    sys.exit(1)

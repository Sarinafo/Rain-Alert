import requests
import os
from twilio.rest import Client


OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")

account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

weather_params = {
    "lat": 21.3069,
    "lon": -157.8583,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}
response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
data = response.json()
weather_slice = data['hourly'][:12]

will_rain = False
for hour_data in weather_slice:
    cond_code = hour_data["weather"][0]["id"]
    if int(cond_code) < 700:
        will_rain = True

if will_rain:
    account_sid = account_sid
    auth_token = auth_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It will rain today. Remember to bring an umbrella☔️",
        from_="+16812515301",
        to="+12164048099"
    ).fetch()

    print(message.status)



import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 39.082104 # Your latitude
MY_LONG = -77.151218 # Your longitude

MY_EMAIL = "battlecrabtest@gmail.com"
MY_PASSWORD ="cphf oanc zbvf azid"

def is_iss_overhead():

    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    data = iss_response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LONG-5 <= iss_longitude <= MY_LONG+5 and MY_LAT-5 <= iss_latitude <= MY_LAT+5:
        return True
    return None


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    day_night_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    day_night_response.raise_for_status()
    data = day_night_response.json()


    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if sunset < time_now.hour < sunrise:
        return True
    return None

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs="cem2010.vt@gmail.com",
                                msg="Subject:Look up!\n\nThe ISS is right above you!")

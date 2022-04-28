import requests
import time

from date import convert_date
from hook import HOOK

BRANCHES = "branches/"
MY_STATION = "a7d1ce445762e13d9634fe8263262fd2faf362877741916a67ee82e26abd121b/"
DATES = "dates"
MY_SERVICE = ";servicePublicId=8e859bd4c1752249665bf2363ea231e1678dbb7fc4decff862d9d41975a9a95a;"
SLOT_LENGTH = "customSlotLength=10"

FULL_DATE = BRANCHES + MY_STATION + DATES + MY_SERVICE + SLOT_LENGTH

LAST_POSSIBLE_DATE = "YYYY-MM-DD"

def get_full_hour(date):
    return BRANCHES + MY_STATION + DATES + "/" + date + "/times" + MY_SERVICE + SLOT_LENGTH

def notify(date, time):
    message = f"Det er en ledig time {convert_date(date)} kl. {time}"
    requests.post(HOOK, f'{{"text":"{message}"}}')

def poll():
    url = "https://pass-og-id.politiet.no/qmaticwebbooking/rest/schedule/"
    service = ApiService(url)

    response = service.get_available_dates()
    first_day = response.json()[0]
    if not first_day["date"] <= LAST_POSSIBLE_DATE:
        return None, None
    
    hour_response = service.get_available_hours(first_day["date"])
    all_hours = [hour["time"] for hour in hour_response.json()]

    return first_day["date"], all_hours[0]

class ApiService:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_branches(self):
        return requests.get(self.base_url + BRANCHES)

    def get_available_dates(self):
        return requests.get(self.base_url + FULL_DATE)
    
    def get_available_hours(self, date):
        return requests.get(self.base_url + get_full_hour(date))

def main():
    date, timestamp = None, None
    while not date:
        date, timestamp = poll()
        if not date:
            time.sleep(10)
    notify(date, timestamp)

if __name__ == "__main__":
    main()




import json
from urllib.request import urlopen
from urllib.error import HTTPError
import os

api_key = os.environ.get('API_KEY')


def events(city, start_date, end_date, page=0):
    try:
        with urlopen(
                f"https://app.ticketmaster.com/discovery/v2/events.json?size=20&sort=date,asc&page={page}&localStartEndDateTime={start_date}T00:00:00,{end_date}T00:00:00&city={city}&apikey={api_key}"
        ) as response:
            source = response.read()

        data = json.loads(source)
        # total_pages = data["page"]["totalPages"]

        for item in data["_embedded"]["events"]:
            event_date = item["dates"]["start"]["localDate"]
            event_time = item["dates"]["start"]["localTime"]
            event_name = item["name"]
            event_url = item["url"]
            print(event_name)
            for x in item["_embedded"]["venues"]:
                venue_name = x["name"]
                city_venue = x["city"]["name"]
                state_venue = x["state"]["name"]
                venue_address = x["address"]["line1"]
                venue_country = x["country"]["name"]
                print(venue_name)
                print(venue_address + ' ' + city_venue + ', ' + state_venue)
                print(venue_country)
                print(event_date, event_time)
                for j in item["classifications"]:
                    event_classification = j["segment"]["name"]
                    print(event_classification)
                    print(event_url)
                    print("\n")
        events(city, start_date, end_date, page + 1)
    except(KeyError, HTTPError):
        return


print(events('Houston', '2021-09-14', '2021-09-28'))

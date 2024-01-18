import json
from datetime import datetime, timedelta
import requests

class FreeTimeSlotsFinder:
    def __init__(self, input_link):
        self.input_link = input_link

    # Function to parse datetime from string
    def parse_datetime(self, datetime_str):
        return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z')

    # Function to find available time slots
    def find_available_slots(self, events):
        events.sort(key = lambda x: x['start']['dateTime'])

        # Set the initial start and end time
        start_time = self.parse_datetime(events[0]['start']['dateTime'])
        end_time = self.parse_datetime(events[-1]['end']['dateTime'])

        # Assume each day available time starts at 07:00:00 and ends at 00:00:00
        day_start_time = '07:00:00'
        day_end_time = '00:00:00'

        available_slots = []

        # Add first time slot before the event starts on the first date if there is an event
        if end_time > start_time:
            available_slots.append({
                "start_time": day_start_time,
                "end_time": start_time.strftime('%H:%M:%S'),
                "date": start_time.strftime('%Y-%m-%d')
            })

        # Find next available time slots
        for event in events:
            event_start_time = self.parse_datetime(event['start']['dateTime'])
            event_end_time = self.parse_datetime(event['end']['dateTime'])

            if event_start_time > start_time:
                end = min(event_start_time, end_time)
                start_time_str = start_time.strftime('%H:%M:%S')
                end_time_str = end.strftime('%H:%M:%S')
                date_str = start_time.strftime('%Y-%m-%d')

                if end.date() > start_time.date():
                    available_slots.append({
                        "start_time": day_start_time,
                        "end_time": end.strftime('%H:%M:%S'),
                        "date": end.strftime('%Y-%m-%d')
                    })

                # If end_time is on the next day, set it to 00:00:00
                if end.date() > start_time.date():
                    end_time_str = day_end_time

                available_slots.append({
                    "start_time": start_time_str,
                    "end_time": end_time_str,
                    "date": date_str
                })

            start_time = max(start_time, event_end_time)

        # Add a final time slot for the last day
        available_slots.append({
                "start_time": end_time.strftime('%H:%M:%S'),
                "end_time": day_end_time,
                "date": end_time.strftime('%Y-%m-%d')
            })

        # Find days without events and add them to the available slots
        all_dates = {slot['date'] for slot in available_slots}
        min_date = self.parse_datetime(events[0]['start']['dateTime']).date()
        max_date = self.parse_datetime(events[-1]['end']['dateTime']).date()

        for single_date in (min_date + timedelta(n) for n in range(int((max_date - min_date).days) + 1)):
            date_str = single_date.strftime('%Y-%m-%d')
            if date_str not in all_dates:
                available_slots.append({
                    "start_time": day_start_time,
                    "end_time": day_end_time,
                    "date": date_str
                })

        return available_slots

    # Function to load events data from the provided input link
    def load_events_data(self):
        response = requests.get(self.input_link)
        events_data = response.json()
        return events_data

    # Function to process free time slots based on the loaded events data
    def calculate_free_time_slots(self):
        events_data = self.load_events_data()
        available_slots = self.find_available_slots(events_data)

        grouped_slots = {}
        for slot in available_slots:
            date = slot["date"]
            if date not in grouped_slots:
                grouped_slots[date] = []
            grouped_slots[date].append({
                "start_time": slot['start_time'],
                "end_time": slot['end_time']
            })

        sorted_grouped_slots = dict(sorted(grouped_slots.items()))
        return sorted_grouped_slots


if __name__ == "__main__":

    input_link = "https://file.notion.so/f/f/ee0c3f7e-9612-446c-bbc7-dff07ad41e91/19e15141-7b4e-413f-be88-f32719690e9c/events.json?id=5d6fbc7e-cf7d-4b28-a8dd-9e426a513c96&table=block&spaceId=ee0c3f7e-9612-446c-bbc7-dff07ad41e91&expirationTimestamp=1705615200000&signature=u7PLy6r4ELqZzUQbGlxYZXbmwMrXibjjOLCYPKZGJ_E&downloadName=events.json"

    free_time_handler = FreeTimeSlotsFinder(input_link)
    free_time_slots = free_time_handler.calculate_free_time_slots()
    output = json.dumps(free_time_slots, indent=2)

    print(output)


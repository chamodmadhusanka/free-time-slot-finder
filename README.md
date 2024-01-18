# Find free times in a Calendar

### Task:
Given a set of events from a calendar, the task is to find the available time slots for scheduling new events.

### Input:
The input will be provided in JSON format and will consist of the following fields:

- `calendar`: A list of events in the calendar, each event containing the following fields:
    - `start_time`: The start time of the event.
    - `end_time`: The end time of the event.
 
### Output:
The output should be provided in JSON format and will consist of a list of available time slots for scheduling new events. Each time slot will contain the following fields:

- `start_time`: The start time of the free time slot.
- `end_time`: The end time of the free time slot.

### Prerequisites:
- `requests` library.
You can install the package using 
```
pip install requests
```


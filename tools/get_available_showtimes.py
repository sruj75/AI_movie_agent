import csv
from datetime import datetime, timedelta

def get_available_showtimes(movie_name: str, location: str, seats_needed: int, desired_time: str) -> str:
    with open("data/showtimes.csv", "r") as file:
        reader = csv.DictReader(file)
        showtimes = list(reader)

    input_time = datetime.strptime(desired_time, "%H:%M")
    time_range_start = input_time - timedelta(hours=1)
    time_range_end = input_time + timedelta(hours=1)

    available = []
    for show in showtimes:
        if show["movie_name"].lower() == movie_name.lower() and show["theater_location"].lower() == location.lower():
            show_time = datetime.strptime(show["time"], "%H:%M")
            if time_range_start <= show_time <= time_range_end:
                if int(show["available_seats"]) >= seats_needed:
                    available.append(f"🕒 {show['time']} at {show['theater_location']} for {show['movie_name']}")

    if not available:
        return "No available showtimes found."
    
    return str(available)

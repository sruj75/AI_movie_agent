import csv
from datetime import datetime

def book_tickets(movie_name: str, location: str, time: str, seats_to_book: int, reservation_name: str) -> str:
    with open("data/showtimes.csv", "r") as file:
        reader = csv.DictReader(file)
        showtimes = list(reader)

    # Find the showtime and check availability
    for show in showtimes:
        if (show["movie_name"].lower() == movie_name.lower() and 
            show["theater_location"].lower() == location.lower() and
            show["time"] == time):

            available = int(show["available_seats"])
            if available >= seats_to_book:
                # Book it
                show["available_seats"] = str(available - seats_to_book)

                # Write back
                fieldnames = reader.fieldnames
                with open("data/showtimes.csv", "w", newline="") as wfile:
                    writer = csv.DictWriter(wfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(showtimes)

                return f"✅ Booking Success: {seats_to_book} seats for {movie_name} at {time} in {location} under {reservation_name}"
            else:
                return f"❌ Not enough seats available. Only {available} seats left."
    
    return f"❌ Showtime not found for {movie_name} at {time} in {location}."

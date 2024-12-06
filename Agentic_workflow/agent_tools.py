from Agentic_workflow.database import SupabaseClient

supabase_client = SupabaseClient()

def check_showtimes_tool(movie_name: str) -> str:
    movie = supabase_client.client.table('movies').select('*').eq('title', movie_name).single().execute().data
    if not movie:
        return f"No movie found with the name '{movie_name}'."
    
    showtimes = supabase_client.client.table('showtimes').select('*').eq('movie_id', movie['id']).execute().data
    if not showtimes:
        return f"No showtimes available for '{movie_name}'."
    
    formatted_showtimes = []
    for show in showtimes:
        formatted_showtimes.append(
            f"Name: {show['name']}, Time: {show['show_time']}, Balcony Seats: {show['balcony_seats']}, First Class Seats: {show['first_class_seats']}"
        )
    return "\n".join(formatted_showtimes)

def book_tickets_tool(movie_name: str, showtime_name: str, num_seats: int) -> str:
    movie = supabase_client.client.table('movies').select('*').eq('title', movie_name).single().execute().data
    if not movie:
        return f"No movie found with the name '{movie_name}'."
    
    showtime = supabase_client.client.table('showtimes').select('*').eq('movie_id', movie['id']).eq('name', showtime_name).single().execute().data
    if not showtime:
        return f"No showtime named '{showtime_name}' found for '{movie_name}'."
    
    available_seats = showtime['balcony_seats'] + showtime['first_class_seats']
    if num_seats > available_seats:
        return f"Only {available_seats} seats are available for '{movie_name}' at '{showtime_name}'."
    
    if num_seats <= showtime['balcony_seats']:
        supabase_client.client.table('showtimes').update({
            'balcony_seats': showtime['balcony_seats'] - num_seats
        }).eq('id', showtime['id']).execute()
        seat_type = 'balcony'
    else:
        seats_left = num_seats - showtime['balcony_seats']
        supabase_client.client.table('showtimes').update({
            'balcony_seats': 0,
            'first_class_seats': showtime['first_class_seats'] - seats_left
        }).eq('id', showtime['id']).execute()
        seat_type = 'first_class'
    
    booking = {
        'showtime_id': showtime['id'],
        'customer_name': 'Anonymous',
        'seats_booked': num_seats,
        'seat_type': seat_type,
        'status': 'confirmed'
    }
    supabase_client.client.table('bookings').insert(booking).execute()
    
    return f"Successfully booked {num_seats} {seat_type} seats for '{movie_name}' at '{showtime_name}'. Enjoy your movie!" 
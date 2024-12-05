from supabase import create_client
from .config import SUPABASE_URL, SUPABASE_KEY

class SupabaseClient:
    def __init__(self):
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)

    async def get_movies(self):
        response = self.client.table('movies').select("*").execute()
        return response.data

    async def get_showtimes(self, movie_id=None):
        query = self.client.table('showtimes').select("*")
        if movie_id:
            query = query.eq('movie_id', movie_id)
        response = query.execute()
        return response.data

    async def create_booking(self, booking_data):
        response = self.client.table('bookings').insert(booking_data).execute()
        return response.data 
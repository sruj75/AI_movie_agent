import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

# Additional configurations
VECTOR_STORE_TABLE = 'movie_data'
SUPABASE_SCHEMA = 'public' 
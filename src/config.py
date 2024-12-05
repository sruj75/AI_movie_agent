import os
from dotenv import load_dotenv
from llama_index import VectorStoreIndex, StorageContext
from llama_index.core.vector_stores import SupabaseVectorStore

# Load environment variables
load_dotenv()

# Use environment variables for Supabase connection
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')  # Using anon key instead of service key

# Add vector store configuration
vector_store = SupabaseVectorStore(
    supabase_url=SUPABASE_URL,
    supabase_key=SUPABASE_ANON_KEY,
    supabase_schema='public',
    table_name='movie_data'  # You need to create this table
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex([], storage_context=storage_context)

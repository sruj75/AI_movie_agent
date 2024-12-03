To configure the APIs in Python, it's essential to align with the official documentation of each service. Below are the configurations for OpenAI, Supabase, TMDB, and WhatsApp Business APIs, tailored for Python implementations.

**1. OpenAI API Configuration**

Utilize the official OpenAI Python library to interact with the API. Ensure you have your API key stored securely, for instance, using environment variables.

```python
import openai
import os

# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Example function to generate a completion
def generate_completion(prompt):
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Usage
completion = generate_completion("Once upon a time")
print(completion)
```

*Note: Replace `"text-davinci-004"` with the appropriate model name as per your requirements.*

**2. Supabase API Configuration**

Leverage the `supabase-py` library to interact with Supabase services. Initialize the client using your Supabase URL and API key.

```python
from supabase import create_client, Client
import os

# Retrieve Supabase credentials from environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Initialize the Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

# Example function to fetch data from a table
def fetch_table_data(table_name):
    response = supabase.table(table_name).select("*").execute()
    return response.data

# Usage
data = fetch_table_data("your_table_name")
print(data)
```

*Ensure that the `supabase` package is installed and up-to-date.*

**3. TMDB API Configuration**

Use the `tmdbv3api` Python library to interact with The Movie Database (TMDB) API. First, install the library using pip:

```bash
pip install tmdbv3api
```

Then, configure it as follows:

```python
from tmdbv3api import TMDb, Movie
import os

# Initialize TMDb with your API key
tmdb = TMDb()
tmdb.api_key = os.getenv("TMDB_API_KEY")

# Example function to search for a movie
def search_movie(title):
    movie = Movie()
    search_results = movie.search(title)
    return search_results

# Usage
results = search_movie("Inception")
for result in results:
    print(result.title, result.release_date)
```

*Ensure you have obtained an API key from TMDB and set it in your environment variables.*

**4. WhatsApp Business API Configuration**

To interact with the WhatsApp Business API, you can use the `whatsapp-python-sdk`. Install the SDK using pip:

```bash
pip install whatsapp-python-sdk
```

Configure the API as follows:

```python
from whatsapp import Client
import os

# Initialize the WhatsApp client with your credentials
whatsapp_client = Client(
    phone_number=os.getenv("WHATSAPP_PHONE_NUMBER"),
    api_key=os.getenv("WHATSAPP_API_KEY"),
    api_secret=os.getenv("WHATSAPP_API_SECRET")
)

# Example function to send a message
def send_whatsapp_message(recipient_number, message):
    response = whatsapp_client.send_message(recipient_number, message)
    return response

# Usage
response = send_whatsapp_message("recipient_number", "Hello, World!")
print(response)
```

*Ensure you have the necessary credentials and have set up your WhatsApp Business API account as per the official documentation.*

**Environment Variables Setup**

It's recommended to store sensitive information like API keys in environment variables. You can create a `.env` file in your project directory and use the `python-dotenv` package to load them:

1. Install `python-dotenv`:

   ```bash
   pip install python-dotenv
   ```

2. Create a `.env` file:

   ```
   OPENAI_API_KEY=your_openai_api_key
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   TMDB_API_KEY=your_tmdb_api_key
   WHATSAPP_PHONE_NUMBER=your_whatsapp_phone_number
   WHATSAPP_API_KEY=your_whatsapp_api_key
   WHATSAPP_API_SECRET=your_whatsapp_api_secret
   ```

3. Load environment variables in your script:

   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()

   # Now you can access the environment variables
   openai_api_key = os.getenv("OPENAI_API_KEY")
   ```

By following these configurations and referring to the official documentation, you can ensure that your API integrations are set up correctly and securely. 
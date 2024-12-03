## App Flow Document

When a user first interacts with the app, they are greeted with a simple and intuitive signup or login page. Upon successful login, they are directed to the dashboard, which acts as the central hub for managing their activities. The dashboard is divided into four main sections: the Metrics section, the Analytics section, the Movie Management section, and the Bookings section.

The Metrics section provides a quick overview of the theater's performance, including the total number of tickets sold, revenue generated, and current occupancy rates for various shows. The Analytics section offers deeper insights into user behavior, such as peak booking times, popular movie genres, and other trends to help managers optimize their schedules and promotions.

The Movie Management section allows theater managers to search for movies using the integrated TMDB API. They can select a movie, view its details like runtime, poster, and language, and add it to the schedule. The scheduling interface is straightforward, enabling the manager to assign showtimes and specify the number of seats available for each class. Once saved, the updated schedule appears instantly on the dashboard.

The Bookings section displays a real-time view of all ongoing and completed bookings. Managers can view details such as customer name, number of tickets, payment status, and QR codes for entry verification. There’s also an option to resend QR codes or update booking statuses if needed. The user journey is seamless, whether they are booking tickets through WhatsApp or managing operations via the dashboard.

For customers, the app experience starts on WhatsApp. They initiate a conversation and fill out a simple form specifying the theater, movie, showtime, and number of tickets. The system responds with available options, including payment instructions via UPI. Once payment is confirmed, the customer receives a QR code for entry. The system also provides movie recommendations and alternative options if their preferred showtime is unavailable. Overall, the app ensures simplicity and efficiency for both theater managers and customers.

## Tech Stack and Packages Document

The frontend is built using React, designed with a mobile-first approach to cater to both desktop and mobile users. For the backend, Supabase serves as the primary database and authentication layer, ensuring secure and efficient data management. Supabase's integration with RAG and vector databases facilitates advanced query handling. LangChain is used for natural language processing workflows and multi-modal interaction support.

The TMDB API is integrated into the backend to fetch movie details, including posters, runtime, and genres. Payments are handled through a UPI-compatible gateway, ensuring secure transactions. For QR code generation and storage, the app uses a dedicated storage bucket within Supabase. The AI layer relies on LlamaIndex for indexing and query resolution, while OpenAI’s GPT-4 model provides conversational and recommendation logic. The messaging interface is powered by WhatsApp Business API, which supports multi-language and natural language interactions.

## API Documentation

OpenAI API: The OpenAI GPT-4 API is used for processing natural language queries and generating movie recommendations. It connects directly to the LangChain workflows and works seamlessly with the private database to provide context-aware responses. For example, when a user asks for evening showtimes, the API fetches data from LlamaIndex and presents an accurate answer.

Supabase API: Supabase APIs manage authentication, user data, and database interactions. It handles CRUD operations for tables like users, movies, showtimes, and bookings. The APIs also manage secure file storage for QR codes and movie posters. For example, when a movie is added via the dashboard, the API stores its details in the movies table and links it to the relevant showtimes.

TMDB API: This API retrieves movie information such as title, year, poster URL, runtime, and language. It is accessed whenever a theater manager searches for a movie to add to the schedule. The API responds with a structured JSON object containing all relevant details, which are then saved in the Supabase database.

Payment Gateway API: The payment gateway API facilitates secure UPI transactions. It provides endpoints for initiating payments, verifying status, and generating payment confirmations. Upon successful payment, the API triggers the generation of a unique QR code stored in the Supabase bucket.

WhatsApp Business API: This API powers the conversational interface for ticket booking. It enables text and voice interactions in multiple languages, offering features like query resolution, booking confirmations, and QR code sharing. The API is tightly integrated with the LangChain workflows and LlamaIndex for handling user queries.


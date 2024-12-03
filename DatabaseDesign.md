Database Design

-- Blueprint for Backend using Supabase

-- User Authentication Table
CREATE TABLE users (
    user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone_number VARCHAR(15),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Theater Managers Table
CREATE TABLE theater_managers (
    manager_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    theater_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Movies Table
CREATE TABLE movies (
    movie_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    year VARCHAR(4),
    imdb_id VARCHAR(20),
    poster_url TEXT,
    runtime INTEGER,
    language VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Showtimes Table
CREATE TABLE showtimes (
    showtime_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    theater_id UUID REFERENCES theater_managers(manager_id) ON DELETE CASCADE,
    movie_id UUID REFERENCES movies(movie_id) ON DELETE CASCADE,
    show_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    balcony_seats INTEGER DEFAULT 50,
    first_class_seats INTEGER DEFAULT 50,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Bookings Table
CREATE TABLE bookings (
    booking_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    showtime_id UUID REFERENCES showtimes(showtime_id) ON DELETE CASCADE,
    seats_booked INTEGER NOT NULL,
    seat_class VARCHAR(50) CHECK (seat_class IN ('balcony', 'first_class')),
    payment_status VARCHAR(50) CHECK (payment_status IN ('pending', 'completed', 'failed')),
    payment_reference VARCHAR(100),
    qr_code_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Logs Table for User Queries
CREATE TABLE user_queries (
    query_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    query_text TEXT NOT NULL,
    response_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Storage Buckets (Supabase Specific)
-- For QR Codes and Movie Posters
-- Storage Bucket: qr_codes
-- Storage Bucket: movie_posters

-- Relationships:
-- users -> theater_managers: One-to-Many (One user can manage multiple theaters)
-- theater_managers -> showtimes: One-to-Many (One theater manager can manage multiple showtimes)
-- movies -> showtimes: One-to-Many (One movie can have multiple showtimes in different theaters)
-- users -> bookings: One-to-Many (One user can make multiple bookings)
-- showtimes -> bookings: One-to-Many (One showtime can have multiple bookings)

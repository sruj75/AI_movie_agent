-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Movies table
CREATE TABLE movies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    year VARCHAR(4) NOT NULL,
    poster_url TEXT,
    imdb_id VARCHAR(20) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    additional_info JSONB DEFAULT '{}'::jsonb
);

-- Showtimes table
CREATE TABLE showtimes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    movie_id UUID REFERENCES movies(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    show_time TIMESTAMP WITH TIME ZONE NOT NULL,
    balcony_seats INTEGER NOT NULL CHECK (balcony_seats >= 0),
    first_class_seats INTEGER NOT NULL CHECK (first_class_seats >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Bookings table
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    showtime_id UUID REFERENCES showtimes(id) ON DELETE CASCADE,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255),
    customer_phone VARCHAR(20),
    seats_booked INTEGER NOT NULL CHECK (seats_booked > 0),
    seat_type VARCHAR(20) CHECK (seat_type IN ('balcony', 'first_class')),
    booking_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled'))
);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_showtimes_updated_at
    BEFORE UPDATE ON showtimes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column(); 
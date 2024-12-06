require('dotenv').config();
import { supabase } from './supabaseClient';
const API_KEY = process.env.API_KEY;

let selectedMovie = null;
let showtimes = [];

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const searchResults = document.getElementById('searchResults');
    const movieDetails = document.getElementById('movieDetails');
    const movieInfo = document.getElementById('movieInfo');
    const showtimeManager = document.getElementById('showtimeManager');
    const addShowtimeForm = document.getElementById('addShowtimeForm');
    const showtimeList = document.getElementById('showtimeList');

    // Event Listeners
    searchButton.addEventListener('click', handleSearch);
    addShowtimeForm.addEventListener('submit', handleAddShowtime);

    function handleSearch() {
        const searchTerm = searchInput.value.trim();
        if (searchTerm) {
            // Fetch data from the OMDB API instead of using mock data
            fetchMovies(searchTerm);
        }
    }

    // New function to fetch movies from the OMDB API
    function fetchMovies(searchTerm) {
        const url = `http://www.omdbapi.com/?s=${encodeURIComponent(searchTerm)}&apikey=${API_KEY}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.Response === "True") {
                    displaySearchResults(data.Search);
                } else {
                    alert('No movies found.');
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                alert('Failed to fetch data. Please try again later.');
            });
    }

    function displaySearchResults(movies) {
        searchResults.innerHTML = '';
        movies.forEach(movie => {
            const movieCard = document.createElement('div');
            movieCard.className = 'movie-card';
            movieCard.innerHTML = `
                <div class="poster-container">
                    <img src="${movie.Poster}" alt="${movie.Title}" class="movie-poster">
                </div>
                <h3>${movie.Title}</h3>
                <p>${movie.Year}</p>
            `;
            movieCard.addEventListener('click', () => selectMovie(movie));
            searchResults.appendChild(movieCard);
        });
    }

    async function selectMovie(movie) {
        try {
            // First, check if movie exists in database
            const { data, error } = await supabase
                .from('movies')
                .select('*')
                .eq('imdb_id', movie.imdbID)
                .single();

            if (error && error.code !== 'PGRST116') throw error;

            if (!data) {
                // Movie doesn't exist, insert it
                const { error: insertError } = await supabase
                    .from('movies')
                    .insert([{
                        title: movie.Title,
                        year: movie.Year,
                        poster_url: movie.Poster,
                        imdb_id: movie.imdbID,
                        additional_info: movie
                    }]);

                if (insertError) throw insertError;
            }

            selectedMovie = movie;
            searchInput.value = '';
            searchResults.innerHTML = '';
            searchResults.classList.add('hidden');
            
            displayMovieDetails();
            showSection(movieDetails);
            showSection(showtimeManager);
            displayShowtimes();
        } catch (error) {
            console.error('Error selecting movie:', error);
            alert('Failed to select movie. Please try again.');
        }
    }

    // Add a function to show search section again (optional)
    function showSearchSection() {
        searchResults.classList.remove('hidden');
        // You could add a "Back to Search" button that calls this function
    }

    function displayMovieDetails() {
        movieInfo.innerHTML = `
            <img src="${selectedMovie.Poster}" alt="${selectedMovie.Title}">
            <div>
                <h2>${selectedMovie.Title}</h2>
                <p>Year: ${selectedMovie.Year}</p>
            </div>
        `;
    }

    async function handleAddShowtime(e) {
        e.preventDefault();
        const newShowtime = {
            movie_id: selectedMovie.imdb_id, // Using IMDB ID as reference
            name: document.getElementById('showtimeName').value,
            show_time: document.getElementById('showtimeTime').value,
            balcony_seats: parseInt(document.getElementById('balconySeats').value),
            first_class_seats: parseInt(document.getElementById('firstClassSeats').value)
        };

        try {
            const { data, error } = await supabase
                .from('showtimes')
                .insert([newShowtime]);

            if (error) throw error;
            
            showtimes.push(data[0]);
            displayShowtimes();
            addShowtimeForm.reset();
        } catch (error) {
            console.error('Error adding showtime:', error);
            alert('Failed to add showtime. Please try again.');
        }
    }

    async function displayShowtimes() {
        try {
            const { data, error } = await supabase
                .from('showtimes')
                .select('*')
                .eq('movie_id', selectedMovie.imdb_id);

            if (error) throw error;

            showtimeList.innerHTML = '';
            data.forEach(showtime => {
                const showtimeItem = document.createElement('div');
                showtimeItem.className = 'showtime-item';
                showtimeItem.innerHTML = `
                    <div>
                        <strong>${showtime.name}</strong> - ${new Date(showtime.show_time).toLocaleTimeString()}
                        <br>
                        Balcony: ${showtime.balcony_seats}, First Class: ${showtime.first_class_seats}
                    </div>
                    <button class="delete-showtime" data-id="${showtime.id}">Delete</button>
                `;
                showtimeList.appendChild(showtimeItem);
            });

            // Add event listeners for delete buttons
            document.querySelectorAll('.delete-showtime').forEach(button => {
                button.addEventListener('click', function() {
                    deleteShowtime(this.getAttribute('data-id'));
                });
            });
        } catch (error) {
            console.error('Error fetching showtimes:', error);
            alert('Failed to load showtimes. Please try again.');
        }
    }

    async function deleteShowtime(id) {
        try {
            const { error } = await supabase
                .from('showtimes')
                .delete()
                .eq('id', id);

            if (error) throw error;

            displayShowtimes();
        } catch (error) {
            console.error('Error deleting showtime:', error);
            alert('Failed to delete showtime. Please try again.');
        }
    }

    function showSection(section) {
        section.classList.remove('hidden');
    }

    // Initial setup
    showSection(document.getElementById('movieSearch'));
});


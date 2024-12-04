require('dotenv').config();
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
                <img src="${movie.Poster}" alt="${movie.Title}">
                <h3>${movie.Title}</h3>
                <p>${movie.Year}</p>
            `;
            movieCard.addEventListener('click', () => selectMovie(movie));
            searchResults.appendChild(movieCard);
        });
    }

    function selectMovie(movie) {
        selectedMovie = movie;
        
        // Clear and hide search input and results
        searchInput.value = ''; // Clear the search input
        searchResults.innerHTML = ''; // Clear the search results
        searchResults.classList.add('hidden'); // Hide the search results section
        
        // Show movie details and showtime manager
        displayMovieDetails();
        showSection(movieDetails);
        showSection(showtimeManager);
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

    function handleAddShowtime(e) {
        e.preventDefault();
        const newShowtime = {
            id: Date.now().toString(),
            name: document.getElementById('showtimeName').value,
            time: document.getElementById('showtimeTime').value,
            balconySeats: parseInt(document.getElementById('balconySeats').value),
            firstClassSeats: parseInt(document.getElementById('firstClassSeats').value)
        };
        showtimes.push(newShowtime);
        displayShowtimes();
        addShowtimeForm.reset();
    }

    function displayShowtimes() {
        showtimeList.innerHTML = '';
        showtimes.forEach(showtime => {
            const showtimeItem = document.createElement('div');
            showtimeItem.className = 'showtime-item';
            showtimeItem.innerHTML = `
                <div>
                    <strong>${showtime.name}</strong> - ${showtime.time}
                    <br>
                    Balcony: ${showtime.balconySeats}, First Class: ${showtime.firstClassSeats}
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
    }

    function deleteShowtime(id) {
        showtimes = showtimes.filter(showtime => showtime.id !== id);
        displayShowtimes();
    }

    function showSection(section) {
        section.classList.remove('hidden');
    }

    // Initial setup
    showSection(document.getElementById('movieSearch'));
});


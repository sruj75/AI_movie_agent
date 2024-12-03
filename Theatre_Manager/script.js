// Mock data for movie search results
const mockMovies = [
    {
        imdbID: "tt1375666",
        Title: "Inception",
        Year: "2010",
        Poster: "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg",
        Runtime: "148 min",
        Language: "English, Japanese, French"
    },
    {
        imdbID: "tt0816692",
        Title: "Interstellar",
        Year: "2014",
        Poster: "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
        Runtime: "169 min",
        Language: "English"
    }
];

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
            // In a real application, you would make an API call here
            displaySearchResults(mockMovies);
        }
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
        displayMovieDetails();
        showSection(movieDetails);
        showSection(showtimeManager);
        // Hide the search results (movie cards) after selecting a movie
        searchResults.classList.add('hidden'); // This line ensures the search results are hidden

    }

    function displayMovieDetails() {
        movieInfo.innerHTML = `
            <img src="${selectedMovie.Poster}" alt="${selectedMovie.Title}">
            <div>
                <h2>${selectedMovie.Title}</h2>
                <p>Year: ${selectedMovie.Year}</p>
                <p>Runtime: ${selectedMovie.Runtime}</p>
                <p>Language: ${selectedMovie.Language}</p>
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


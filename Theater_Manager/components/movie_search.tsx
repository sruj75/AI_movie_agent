"use client"

import { useState } from "react"
import { Search } from 'lucide-react'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Movie } from "@/types"

interface MovieSearchProps {
  onSelectMovie: (movie: Movie) => void
}

export function MovieSearch({ onSelectMovie }: MovieSearchProps) {
  const [searchTerm, setSearchTerm] = useState("")
  const [searchResults, setSearchResults] = useState<Movie[]>([])

  const handleSearch = async () => {
    // This is a mock API call. In a real application, you would call your actual API here.
    const mockResults: Movie[] = [
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
    ]
    setSearchResults(mockResults)
  }

  return (
    <div className="space-y-4">
      <div className="flex space-x-2">
        <Input
          type="text"
          placeholder="Search for a movie..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-grow"
        />
        <Button onClick={handleSearch}>
          <Search className="w-4 h-4 mr-2" />
          Search
        </Button>
      </div>
      {searchResults.length > 0 && (
        <div className="grid grid-cols-2 gap-4">
          {searchResults.map((movie) => (
            <div
              key={movie.imdbID}
              className="flex items-center space-x-4 p-4 rounded-lg border border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors"
              onClick={() => onSelectMovie(movie)}
            >
              <img src={movie.Poster} alt={movie.Title} className="w-16 h-24 object-cover rounded" />
              <div>
                <h3 className="font-semibold">{movie.Title}</h3>
                <p className="text-sm text-gray-500">{movie.Year}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}


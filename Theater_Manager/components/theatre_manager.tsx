"use client"

import { useState } from "react"
import { MovieSearch } from "./movie-search"
import { MovieDetails } from "./movie-details"
import { ShowtimeManager } from "./showtime-manager"
import { Movie } from "@/types"

export function TheatreManager() {
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null)

  return (
    <div className="space-y-8">
      <MovieSearch onSelectMovie={setSelectedMovie} />
      {selectedMovie && (
        <>
          <MovieDetails movie={selectedMovie} />
          <ShowtimeManager />
        </>
      )}
    </div>
  )
}


import { Movie } from "@/types"

interface MovieDetailsProps {
  movie: Movie
}

export function MovieDetails({ movie }: MovieDetailsProps) {
  return (
    <div className="flex space-x-6 p-6 bg-gray-50 rounded-lg">
      <img src={movie.Poster} alt={movie.Title} className="w-32 h-48 object-cover rounded-md shadow-md" />
      <div className="space-y-2">
        <h2 className="text-2xl font-semibold">{movie.Title}</h2>
        <p className="text-gray-600">{movie.Year}</p>
        <p className="text-gray-600">Runtime: {movie.Runtime}</p>
        <p className="text-gray-600">Language: {movie.Language}</p>
      </div>
    </div>
  )
}


"use client"

import { useState } from "react"
import { Plus, Trash2, Clock, Users } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Showtime } from "@/types"

export function ShowtimeManager() {
  const [showtimes, setShowtimes] = useState<Showtime[]>([])
  const [newShowtime, setNewShowtime] = useState<Showtime>({
    id: "",
    name: "",
    time: "",
    balconySeats: 0,
    firstClassSeats: 0,
  })

  const handleAddShowtime = (e: React.FormEvent) => {
    e.preventDefault()
    setShowtimes([...showtimes, { ...newShowtime, id: Date.now().toString() }])
    setNewShowtime({
      id: "",
      name: "",
      time: "",
      balconySeats: 0,
      firstClassSeats: 0,
    })
  }

  const handleUpdateShowtime = (id: string, field: keyof Showtime, value: string | number) => {
    setShowtimes(
      showtimes.map((showtime) =>
        showtime.id === id ? { ...showtime, [field]: value } : showtime
      )
    )
  }

  const handleDeleteShowtime = (id: string) => {
    setShowtimes(showtimes.filter((showtime) => showtime.id !== id))
  }

  return (
    <div className="space-y-8 bg-gray-50 p-6 rounded-lg">
      <div>
        <h2 className="text-2xl font-semibold mb-4">Manage Showtimes</h2>
        <p className="text-gray-600">Add and manage showtimes for the selected movie.</p>
      </div>
      
      <Separator />
      
      <div>
        <h3 className="text-lg font-medium mb-4">Add New Showtime</h3>
        <form onSubmit={handleAddShowtime} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="showtime-name">Showtime Name</Label>
              <Input
                id="showtime-name"
                placeholder="e.g., Evening Show"
                value={newShowtime.name}
                onChange={(e) => setNewShowtime({ ...newShowtime, name: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="showtime-time">Time</Label>
              <Input
                id="showtime-time"
                type="time"
                value={newShowtime.time}
                onChange={(e) => setNewShowtime({ ...newShowtime, time: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="balcony-seats">Balcony Seats</Label>
              <Input
                id="balcony-seats"
                type="number"
                placeholder="Number of balcony seats"
                value={newShowtime.balconySeats}
                onChange={(e) =>
                  setNewShowtime({ ...newShowtime, balconySeats: parseInt(e.target.value) })
                }
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="first-class-seats">First Class Seats</Label>
              <Input
                id="first-class-seats"
                type="number"
                placeholder="Number of first class seats"
                value={newShowtime.firstClassSeats}
                onChange={(e) =>
                  setNewShowtime({ ...newShowtime, firstClassSeats: parseInt(e.target.value) })
                }
                required
              />
            </div>
          </div>
          <Button type="submit" className="w-full md:w-auto">
            <Plus className="w-4 h-4 mr-2" />
            Add Showtime
          </Button>
        </form>
      </div>
      
      <Separator />
      
      <div>
        <h3 className="text-lg font-medium mb-4">Current Showtimes</h3>
        <div className="space-y-4">
          {showtimes.length === 0 ? (
            <p className="text-gray-500 italic">No showtimes added yet.</p>
          ) : (
            showtimes.map((showtime) => (
              <div key={showtime.id} className="flex flex-col md:flex-row items-start md:items-center gap-4 p-4 bg-white rounded-lg shadow">
                <div className="flex-grow space-y-2 w-full md:w-auto">
                  <Label>Showtime Name</Label>
                  <Input
                    value={showtime.name}
                    onChange={(e) => handleUpdateShowtime(showtime.id, "name", e.target.value)}
                  />
                </div>
                <div className="flex items-center gap-2 w-full md:w-auto">
                  <Clock className="w-4 h-4 text-gray-500" />
                  <Input
                    type="time"
                    value={showtime.time}
                    onChange={(e) => handleUpdateShowtime(showtime.id, "time", e.target.value)}
                    className="w-32"
                  />
                </div>
                <div className="flex items-center gap-2 w-full md:w-auto">
                  <Users className="w-4 h-4 text-gray-500" />
                  <Input
                    type="number"
                    value={showtime.balconySeats}
                    onChange={(e) =>
                      handleUpdateShowtime(showtime.id, "balconySeats", parseInt(e.target.value))
                    }
                    className="w-20"
                  />
                  <span className="text-sm text-gray-500">Balcony</span>
                </div>
                <div className="flex items-center gap-2 w-full md:w-auto">
                  <Users className="w-4 h-4 text-gray-500" />
                  <Input
                    type="number"
                    value={showtime.firstClassSeats}
                    onChange={(e) =>
                      handleUpdateShowtime(showtime.id, "firstClassSeats", parseInt(e.target.value))
                    }
                    className="w-20"
                  />
                  <span className="text-sm text-gray-500">First Class</span>
                </div>
                <Button variant="destructive" onClick={() => handleDeleteShowtime(showtime.id)} className="w-full md:w-auto">
                  <Trash2 className="w-4 h-4 mr-2" />
                  Delete
                </Button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}


'use client'
import Link from 'next/link'
import { useEffect, useState } from 'react'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import api from '@/services/api'

export default function EventsPage() {
  const [events, setEvents] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    api.get('/events/').then((res) => setEvents(res.data.results || res.data || [])).catch(() => setEvents([])).finally(() => setLoading(false))
  }, [])
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-primary mb-4">Events</h1>
        <p className="text-gray-600 dark:text-gray-400 mb-8">Workshops, trainings, and activities.</p>
        {loading && <div className="py-12">Loading...</div>}
        {!loading && events.length === 0 && <div className="card py-12 text-center"><p className="text-gray-600">No events yet.</p></div>}
        {!loading && events.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {events.map((e: any) => (
              <div key={e.id} className="card">
                <span className="px-3 py-1 bg-accent/10 text-accent rounded-full text-sm">{e.event_type}</span>
                <h2 className="text-xl font-bold mt-2 mb-2">{e.title}</h2>
                <p className="text-gray-600 dark:text-gray-400 line-clamp-2 mb-2">{e.description}</p>
                <p className="text-sm text-gray-500 mb-4">Venue: {e.venue}</p>
                <Link href={'/events/' + e.slug} className="text-primary font-semibold">View details</Link>
              </div>
            ))}
          </div>
        )}
      </main>
      <Footer />
    </div>
  )
}

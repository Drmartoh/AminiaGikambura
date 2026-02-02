'use client'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { format } from 'date-fns'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import api from '@/services/api'

export default function EventDetailPage() {
  const params = useParams()
  const slug = params?.slug as string
  const [event, setEvent] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [notFound, setNotFound] = useState(false)
  useEffect(() => {
    if (!slug) return
    api.get('/events/?slug=' + slug)
      .then((res) => {
        const data = res.data.results || res.data
        const found = Array.isArray(data) ? data.find((e: any) => e.slug === slug) : data
        if (found) setEvent(found)
        else setNotFound(true)
      })
      .catch(() => setNotFound(true))
      .finally(() => setLoading(false))
  }, [slug])
  if (loading) return <div className="min-h-screen flex flex-col"><Header /><main className="flex-grow container mx-auto px-4 py-12">Loading...</main><Footer /></div>
  if (notFound || !event) return <div className="min-h-screen flex flex-col"><Header /><main className="flex-grow container mx-auto px-4 py-12"><h1 className="text-2xl font-bold mb-4">Event not found</h1><Link href="/events" className="text-primary font-semibold">Back to Events</Link></main><Footer /></div>
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <Link href="/events" className="text-primary font-semibold mb-6 inline-block">← Back to Events</Link>
        {event.featured_image && <div className="w-full h-64 md:h-96 bg-gray-200 dark:bg-slate-700 rounded-xl mb-8 overflow-hidden"><img src={event.featured_image} alt={event.title} className="w-full h-full object-cover" /></div>}
        <span className="px-3 py-1 bg-accent/10 text-accent rounded-full text-sm">{event.event_type}</span>
        <h1 className="text-4xl font-bold text-primary mt-4 mb-4">{event.title}</h1>
        <p className="text-gray-600 dark:text-gray-400 mb-2">Start: {format(new Date(event.start_date), 'PPpp')}</p>
        {event.end_date && <p className="text-gray-600 dark:text-gray-400 mb-4">End: {format(new Date(event.end_date), 'PPpp')}</p>}
        <p className="text-gray-600 dark:text-gray-400 mb-6">Venue: {event.venue}</p>
        <div className="prose dark:prose-invert max-w-none"><p className="text-gray-600 dark:text-gray-400 whitespace-pre-wrap">{event.description}</p></div>
      </main>
      <Footer />
    </div>
  )
}

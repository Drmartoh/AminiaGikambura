'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { format } from 'date-fns'
import api from '@/services/api'
import { useEffect, useState } from 'react'

interface Event {
  id: number
  title: string
  slug: string
  description: string
  start_date: string
  venue: string
  event_type: string
}

export default function LatestEvents() {
  const [events, setEvents] = useState<Event[]>([])

  useEffect(() => {
    api.get('/events/?is_published=true')
      .then((response) => {
        const sorted = response.data.results?.sort(
          (a: Event, b: Event) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime()
        ) || []
        setEvents(sorted.slice(0, 3))
      })
      .catch(() => {
        // Handle error
      })
  }, [])

  return (
    <section className="py-20 bg-gray-50 dark:bg-slate-800">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl font-bold text-center mb-4">Upcoming Events</h2>
          <p className="text-center text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto">
            Join us for exciting events, workshops, and community activities.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {events.length > 0 ? (
              events.map((event, index) => (
                <motion.div
                  key={event.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="card"
                >
                  <div className="flex items-center justify-between mb-4">
                    <span className="px-3 py-1 bg-accent/10 text-accent rounded-full text-sm">
                      {event.event_type}
                    </span>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {format(new Date(event.start_date), 'MMM dd, yyyy')}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold mb-2">{event.title}</h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
                    {event.description}
                  </p>
                  <div className="flex items-center text-sm text-gray-500 mb-4">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    {event.venue}
                  </div>
                  <Link
                    href={`/events/${event.slug}`}
                    className="text-primary hover:text-primary-light font-semibold inline-flex items-center"
                  >
                    Learn More →
                  </Link>
                </motion.div>
              ))
            ) : (
              <div className="col-span-3 text-center text-gray-500">
                No upcoming events at the moment.
              </div>
            )}
          </div>
          
          <div className="text-center mt-12">
            <Link href="/events" className="btn-primary">
              View All Events
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

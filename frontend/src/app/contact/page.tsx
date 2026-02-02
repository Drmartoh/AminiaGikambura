'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import api from '@/services/api'

export default function ContactPage() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: '',
  })
  const [status, setStatus] = useState<'idle' | 'sending' | 'success' | 'error'>('idle')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus('sending')
    try {
      await api.post('/reports/contact/', form)
      setStatus('success')
      setForm({ name: '', email: '', phone: '', subject: '', message: '' })
    } catch {
      setStatus('error')
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-2xl mx-auto"
        >
          <h1 className="text-4xl font-bold text-primary mb-4">Contact Us</h1>
          <p className="text-gray-600 dark:text-gray-400 mb-8">
            Have a question or want to get involved? Send us a message and we will get back to you.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
            <div>
              <h3 className="font-bold mb-2">Email</h3>
              <p className="text-gray-600 dark:text-gray-400">info@agcbo.org</p>
            </div>
            <div>
              <h3 className="font-bold mb-2">Phone</h3>
              <p className="text-gray-600 dark:text-gray-400">+254 XXX XXX XXX</p>
            </div>
            <div>
              <h3 className="font-bold mb-2">Location</h3>
              <p className="text-gray-600 dark:text-gray-400">Kiambu County, Kenya</p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="card space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Name *</label>
              <input
                type="text"
                required
                className="input-field"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Email *</label>
              <input
                type="email"
                required
                className="input-field"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Phone</label>
              <input
                type="tel"
                className="input-field"
                value={form.phone}
                onChange={(e) => setForm({ ...form, phone: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Subject *</label>
              <input
                type="text"
                required
                className="input-field"
                value={form.subject}
                onChange={(e) => setForm({ ...form, subject: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Message *</label>
              <textarea
                required
                rows={5}
                className="input-field"
                value={form.message}
                onChange={(e) => setForm({ ...form, message: e.target.value })}
              />
            </div>
            {status === 'success' && (
              <p className="text-green-600 dark:text-green-400">Thank you! Your message has been sent.</p>
            )}
            {status === 'error' && (
              <p className="text-red-600 dark:text-red-400">Something went wrong. Please try again.</p>
            )}
            <button
              type="submit"
              disabled={status === 'sending'}
              className="btn-primary disabled:opacity-50"
            >
              {status === 'sending' ? 'Sending...' : 'Send message'}
            </button>
          </form>
        </motion.div>
      </main>
      <Footer />
    </div>
  )
}

'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import { authService, User } from '@/services/auth'
import api from '@/services/api'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login')
      return
    }

    authService.getCurrentUser()
      .then(setUser)
      .catch(() => router.push('/login'))
      .finally(() => setLoading(false))
  }, [router])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow py-12 bg-gray-50 dark:bg-slate-800">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="text-4xl font-bold mb-8">Welcome, {user.first_name || user.username}!</h1>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="card">
                <h3 className="text-lg font-semibold mb-2">My Projects</h3>
                <p className="text-3xl font-bold text-primary">0</p>
              </div>
              <div className="card">
                <h3 className="text-lg font-semibold mb-2">My Events</h3>
                <p className="text-3xl font-bold text-accent">0</p>
              </div>
              <div className="card">
                <h3 className="text-lg font-semibold mb-2">My Points</h3>
                <p className="text-3xl font-bold text-teal">0</p>
              </div>
            </div>

            {!user.is_approved && (
              <div className="card bg-yellow-50 border-yellow-200 border-2">
                <h3 className="text-lg font-semibold mb-2 text-yellow-800">Account Pending Approval</h3>
                <p className="text-yellow-700">
                  Your account is pending admin approval. You'll be able to access all features once approved.
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </main>
      <Footer />
    </div>
  )
}

'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { authService } from '@/services/auth'

export default function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const router = useRouter()

  useEffect(() => {
    setIsAuthenticated(authService.isAuthenticated())
  }, [])

  const handleLogout = () => {
    authService.logout()
    setIsAuthenticated(false)
    router.push('/')
  }

  return (
    <header className="bg-white dark:bg-slate-900 shadow-md sticky top-0 z-50">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
              <span className="text-white font-bold text-xl">A</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-primary">AGCBO</h1>
              <p className="text-xs text-gray-600 dark:text-gray-400">Aminia Gikambura CBO</p>
            </div>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-6">
            <Link href="/projects" className="text-gray-700 dark:text-gray-300 hover:text-primary transition-colors">
              Projects
            </Link>
            <Link href="/events" className="text-gray-700 dark:text-gray-300 hover:text-primary transition-colors">
              Events
            </Link>
            <Link href="/gallery" className="text-gray-700 dark:text-gray-300 hover:text-primary transition-colors">
              Gallery
            </Link>
            <Link href="/sports" className="text-gray-700 dark:text-gray-300 hover:text-primary transition-colors">
              Sports
            </Link>
            <Link href="/about" className="text-gray-700 dark:text-gray-300 hover:text-primary transition-colors">
              About
            </Link>
            {isAuthenticated ? (
              <>
                <Link href="/dashboard" className="btn-primary text-sm py-2 px-4">
                  Dashboard
                </Link>
                <button onClick={handleLogout} className="btn-outline text-sm py-2 px-4">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="text-gray-700 dark:text-gray-300 hover:text-primary transition-colors">
                  Login
                </Link>
                <Link href="/register" className="btn-primary text-sm py-2 px-4">
                  Join Us
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden text-gray-700 dark:text-gray-300"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {isOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden mt-4 space-y-4"
          >
            <Link href="/projects" className="block text-gray-700 dark:text-gray-300 hover:text-primary">
              Projects
            </Link>
            <Link href="/events" className="block text-gray-700 dark:text-gray-300 hover:text-primary">
              Events
            </Link>
            <Link href="/gallery" className="block text-gray-700 dark:text-gray-300 hover:text-primary">
              Gallery
            </Link>
            <Link href="/sports" className="block text-gray-700 dark:text-gray-300 hover:text-primary">
              Sports
            </Link>
            <Link href="/about" className="block text-gray-700 dark:text-gray-300 hover:text-primary">
              About
            </Link>
            {isAuthenticated ? (
              <>
                <Link href="/dashboard" className="block btn-primary text-center">
                  Dashboard
                </Link>
                <button onClick={handleLogout} className="block w-full btn-outline">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="block text-gray-700 dark:text-gray-300 hover:text-primary">
                  Login
                </Link>
                <Link href="/register" className="block btn-primary text-center">
                  Join Us
                </Link>
              </>
            )}
          </motion.div>
        )}
      </nav>
    </header>
  )
}

'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { format } from 'date-fns'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import api from '@/services/api'

interface Report {
  id: number
  title: string
  report_type: string
  report_date: string
  report_file?: string
  report_url?: string
  project?: { title: string }
}

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/reports/')
      .then((res) => setReports(res.data.results || res.data || []))
      .catch(() => setReports([]))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-12">
          <h1 className="text-4xl font-bold text-primary mb-4">Reports</h1>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl">
            Public reports on projects and funding.
          </p>
        </motion.div>
        {loading ? (
          <div className="text-center py-12">Loading reports...</div>
        ) : reports.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">No public reports yet.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {reports.map((report, i) => (
              <motion.div
                key={report.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="card flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
              >
                <div>
                  <h2 className="text-xl font-bold mb-1">{report.title}</h2>
                  <p className="text-sm text-gray-500">
                    {report.report_type} • {format(new Date(report.report_date), 'MMM dd, yyyy')}
                  </p>
                </div>
                {(report.report_url || report.report_file) && (
                  <a
                    href={report.report_url || report.report_file}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-primary text-sm py-2 px-4"
                  >
                    View / Download
                  </a>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </main>
      <Footer />
    </div>
  )
}

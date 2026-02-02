'use client'
import Link from 'next/link'
import { useEffect, useState } from 'react'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import api from '@/services/api'

export default function ProjectsPage() {
  const [projects, setProjects] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    api.get('/projects/').then((res) => setProjects(res.data.results || res.data || [])).catch(() => setProjects([])).finally(() => setLoading(false))
  }, [])
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-primary mb-4">Our Projects</h1>
        <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-2xl">Discover our initiatives.</p>
        {loading ? <div className="py-12">Loading...</div> : projects.length === 0 ? <div className="card py-12 text-center"><p className="text-gray-600">No projects yet.</p></div> : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {projects.map((p: any) => (
              <div key={p.id} className="card">
                {p.category && <span className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm">{p.category.name}</span>}
                <h2 className="text-xl font-bold mt-2 mb-2">{p.title}</h2>
                <p className="text-gray-600 dark:text-gray-400 line-clamp-3 mb-4">{p.description}</p>
                <Link href={`/projects/${p.slug}`} className="text-primary font-semibold">Learn more →</Link>
              </div>
            ))}
          </div>
        )}
      </main>
      <Footer />
    </div>
  )
}

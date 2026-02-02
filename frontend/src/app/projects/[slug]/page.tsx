'use client'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import api from '@/services/api'

export default function ProjectDetailPage() {
  const params = useParams()
  const slug = params?.slug as string
  const [project, setProject] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [notFound, setNotFound] = useState(false)
  useEffect(() => {
    if (!slug) return
    api.get('/projects/?slug=' + slug)
      .then((res) => {
        const data = res.data.results || res.data
        const found = Array.isArray(data) ? data.find((p: any) => p.slug === slug) : data
        if (found) setProject(found)
        else setNotFound(true)
      })
      .catch(() => setNotFound(true))
      .finally(() => setLoading(false))
  }, [slug])
  if (loading) return <div className="min-h-screen flex flex-col"><Header /><main className="flex-grow container mx-auto px-4 py-12">Loading...</main><Footer /></div>
  if (notFound || !project) return <div className="min-h-screen flex flex-col"><Header /><main className="flex-grow container mx-auto px-4 py-12"><h1 className="text-2xl font-bold mb-4">Project not found</h1><Link href="/projects" className="text-primary font-semibold">Back to Projects</Link></main><Footer /></div>
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <Link href="/projects" className="text-primary font-semibold mb-6 inline-block">Back to Projects</Link>
        {project.featured_image && <div className="w-full h-64 md:h-96 bg-gray-200 dark:bg-slate-700 rounded-xl mb-8 overflow-hidden"><img src={project.featured_image} alt={project.title} className="w-full h-full object-cover" /></div>}
        {project.category && <span className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm">{project.category.name}</span>}
        <h1 className="text-4xl font-bold text-primary mt-4 mb-4">{project.title}</h1>
        <span className="inline-block px-3 py-1 rounded-full text-sm bg-gray-100 text-gray-800 mb-6">{project.status}</span>
        <div className="prose dark:prose-invert max-w-none mb-8"><p className="text-gray-600 dark:text-gray-400 whitespace-pre-wrap">{project.description}</p></div>
        {project.objectives && <section className="mb-8"><h2 className="text-2xl font-bold mb-4">Objectives</h2><p className="text-gray-600 dark:text-gray-400 whitespace-pre-wrap">{project.objectives}</p></section>}
        {(project.budget_amount > 0 || project.budget_amount) && <section className="mb-8"><h2 className="text-2xl font-bold mb-4">Budget</h2><p className="text-gray-600 dark:text-gray-400">{project.budget_currency} {String(project.budget_amount)}</p></section>}
      </main>
      <Footer />
    </div>
  )
}

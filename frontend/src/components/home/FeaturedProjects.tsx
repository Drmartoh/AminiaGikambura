'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import api from '@/services/api'
import { useEffect, useState } from 'react'

interface Project {
  id: number
  title: string
  slug: string
  description: string
  status: string
  featured_image?: string
  category?: { name: string }
}

export default function FeaturedProjects() {
  const [projects, setProjects] = useState<Project[]>([])

  useEffect(() => {
    api.get('/projects/?is_featured=true&status=ongoing')
      .then((response) => {
        setProjects(response.data.results?.slice(0, 3) || [])
      })
      .catch(() => {
        // Handle error - could show placeholder projects
      })
  }, [])

  return (
    <section className="py-20 bg-white dark:bg-slate-900">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl font-bold text-center mb-4">Featured Projects</h2>
          <p className="text-center text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto">
            Discover our ongoing initiatives that are making a real impact in our communities.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {projects.length > 0 ? (
              projects.map((project, index) => (
                <motion.div
                  key={project.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  className="card group cursor-pointer"
                >
                  {project.featured_image && (
                    <div className="w-full h-48 bg-gray-200 dark:bg-slate-700 rounded-xl mb-4 overflow-hidden">
                      <img
                        src={project.featured_image}
                        alt={project.title}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                      />
                    </div>
                  )}
                  {project.category && (
                    <span className="inline-block px-3 py-1 bg-primary/10 text-primary rounded-full text-sm mb-3">
                      {project.category.name}
                    </span>
                  )}
                  <h3 className="text-xl font-bold mb-2">{project.title}</h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-3">
                    {project.description}
                  </p>
                  <Link
                    href={`/projects/${project.slug}`}
                    className="text-primary hover:text-primary-light font-semibold inline-flex items-center"
                  >
                    Learn More →
                  </Link>
                </motion.div>
              ))
            ) : (
              <div className="col-span-3 text-center text-gray-500">
                Loading projects...
              </div>
            )}
          </div>
          
          <div className="text-center mt-12">
            <Link href="/projects" className="btn-primary">
              View All Projects
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

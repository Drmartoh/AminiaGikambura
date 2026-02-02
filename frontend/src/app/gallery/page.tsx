'use client'
import { useEffect, useState } from 'react'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import api from '@/services/api'

export default function GalleryPage() {
  const [items, setItems] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    api.get('/gallery/').then((res) => setItems(res.data.results || res.data || [])).catch(() => setItems([])).finally(() => setLoading(false))
  }, [])
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-primary mb-4">Gallery</h1>
        <p className="text-gray-600 dark:text-gray-400 mb-8">Photos and videos.</p>
        {loading && <div className="py-12">Loading...</div>}
        {!loading && items.length === 0 && <div className="card py-12 text-center"><p className="text-gray-600">No gallery items yet.</p></div>}
        {!loading && items.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {items.map((item: any) => (
              <div key={item.id} className="card overflow-hidden p-0">
                {item.file && <div className="aspect-square bg-gray-200"><img src={item.file} alt={item.title} className="w-full h-full object-cover" /></div>}
                <div className="p-4"><h3 className="font-bold">{item.title}</h3><p className="text-sm text-gray-500">{item.year}</p></div>
              </div>
            ))}
          </div>
        )}
      </main>
      <Footer />
    </div>
  )
}

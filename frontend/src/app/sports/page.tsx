'use client'
import { useEffect, useState } from 'react'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import api from '@/services/api'

export default function SportsPage() {
  const [programs, setPrograms] = useState<any[]>([])
  const [teams, setTeams] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    Promise.all([
      api.get('/sports/programs/').then((r) => r.data.results || r.data || []),
      api.get('/sports/teams/').then((r) => r.data.results || r.data || []),
    ]).then(([p, t]) => { setPrograms(p); setTeams(t) }).catch(() => {}).finally(() => setLoading(false))
  }, [])
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-primary mb-4">Sports and Talent</h1>
        <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-2xl">Programs and teams.</p>
        {loading ? <div className="py-12">Loading...</div> : (
          <>
            {programs.length > 0 && <section className="mb-12"><h2 className="text-2xl font-bold mb-6">Programs</h2><div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">{programs.map((p: any) => <div key={p.id} className="card"><h3 className="text-xl font-bold text-primary">{p.name}</h3><p className="text-sm text-gray-500">{p.sport_type}</p></div>)}</div></section>}
            {teams.length > 0 && <section><h2 className="text-2xl font-bold mb-6">Teams</h2><div className="grid grid-cols-1 md:grid-cols-2 gap-6">{teams.map((t: any) => <div key={t.id} className="card"><h3 className="text-xl font-bold">{t.name}</h3><p className="text-sm text-primary">{t.sport_program?.name}</p></div>)}</div></section>}
            {!loading && programs.length === 0 && teams.length === 0 && <div className="card py-12 text-center"><p className="text-gray-600">No sports data yet.</p></div>}
          </>
        )}
      </main>
      <Footer />
    </div>
  )
}

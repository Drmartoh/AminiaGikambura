import Link from 'next/link'
import { motion } from 'framer-motion'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import Hero from '@/components/home/Hero'
import Stats from '@/components/home/Stats'
import FeaturedProjects from '@/components/home/FeaturedProjects'
import LatestEvents from '@/components/home/LatestEvents'
import Partners from '@/components/home/Partners'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">
        <Hero />
        <Stats />
        <FeaturedProjects />
        <LatestEvents />
        <Partners />
      </main>
      <Footer />
    </div>
  )
}

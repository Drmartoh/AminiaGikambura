'use client'

import { motion } from 'framer-motion'

const partners = [
  { name: 'Ministry of Youth', logo: '/partners/youth-ministry.png' },
  { name: 'Kiambu County', logo: '/partners/kiambu.png' },
  { name: 'Ministry of Agriculture', logo: '/partners/agriculture.png' },
  { name: 'Ministry of Sports', logo: '/partners/sports.png' },
]

export default function Partners() {
  return (
    <section className="py-20 bg-white dark:bg-slate-900">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-4xl font-bold text-center mb-4">Our Partners</h2>
          <p className="text-center text-gray-600 dark:text-gray-400 mb-12 max-w-2xl mx-auto">
            We work with government ministries, county governments, and organizations to create lasting impact.
          </p>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 items-center">
            {partners.map((partner, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.5 }}
                className="flex items-center justify-center p-6 bg-gray-50 dark:bg-slate-800 rounded-xl hover:shadow-lg transition-shadow"
              >
                <span className="text-gray-400 text-sm">{partner.name}</span>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}

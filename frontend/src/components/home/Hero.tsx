'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'

export default function Hero() {
  return (
    <section className="relative bg-gradient-to-br from-primary via-primary-light to-teal min-h-[700px] flex items-center overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-10 w-72 h-72 bg-accent/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-sky/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="container mx-auto px-4 py-20 relative z-10">
        {/* Organization Name Badge with Buttons */}
        <motion.div
          initial={{ opacity: 0, y: -30, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 1, type: "spring", bounce: 0.4 }}
          className="mb-10 flex flex-col md:flex-row items-center justify-center gap-6 md:gap-8"
        >
          {/* Organization Name Badge */}
          <div className="relative inline-block">
            {/* Multiple glowing effects for depth */}
            <div className="absolute inset-0 bg-accent/20 blur-3xl rounded-3xl animate-pulse"></div>
            <div className="absolute inset-0 bg-primary/20 blur-2xl rounded-3xl animate-pulse" style={{ animationDelay: '0.5s' }}></div>
            
            {/* Main badge with enhanced styling */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="relative bg-white/98 dark:bg-slate-900/98 backdrop-blur-md px-8 py-6 md:px-14 md:py-10 rounded-3xl shadow-2xl transition-all duration-300"
            >
              <div className="text-center relative z-10">
                {/* Main Organization Name - Large and Eye-catching with gradient */}
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.4, duration: 0.8 }}
                  className="text-4xl md:text-6xl lg:text-7xl font-black mb-3 leading-tight"
                  style={{ 
                    fontFamily: "'Playfair Display', serif",
                    background: 'linear-gradient(135deg, #0d4f3c 0%, #fbbf24 50%, #0d4f3c 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                    letterSpacing: '-0.02em',
                  }}
                >
                  Aminia Gikambura
                </motion.div>
                
                {/* Subtitle - Community Based Organisation */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6, duration: 0.8 }}
                  className="text-xl md:text-3xl lg:text-4xl font-bold text-accent mb-3 tracking-wide org-name-glow"
                >
                  Community Based Organisation
                </motion.div>
                
                {/* CBO Badge with animation */}
                <motion.div
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.8, type: "spring", bounce: 0.6 }}
                  whileHover={{ scale: 1.1 }}
                  className="inline-block px-6 py-2 bg-gradient-to-r from-primary to-primary-light text-white rounded-full text-base md:text-lg font-bold mt-2 shadow-lg"
                >
                  (CBO)
                </motion.div>
              </div>
            </motion.div>
          </div>

          {/* Action Buttons - Small but visible */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.8, duration: 0.8 }}
            className="flex flex-col gap-3 md:gap-4"
          >
            <Link 
              href="/register" 
              className="bg-accent hover:bg-accent-light text-white font-semibold py-2 px-4 md:py-2.5 md:px-5 rounded-lg text-sm md:text-base transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl whitespace-nowrap"
            >
              Join the CBO
            </Link>
            <Link 
              href="/projects" 
              className="bg-white/95 hover:bg-white text-primary font-semibold py-2 px-4 md:py-2.5 md:px-5 rounded-lg text-sm md:text-base transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl whitespace-nowrap"
            >
              Support a Project
            </Link>
            <Link 
              href="/about" 
              className="border-2 border-white/80 hover:border-white hover:bg-white/10 text-white font-semibold py-2 px-4 md:py-2.5 md:px-5 rounded-lg text-sm md:text-base transition-all duration-300 transform hover:scale-105 whitespace-nowrap"
            >
              View Our Impact
            </Link>
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="max-w-3xl text-white"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Empowering Youth Through
            <span className="block text-accent">Community Action</span>
          </h1>
          <p className="text-xl mb-8 text-gray-100">
            Building a better future for our youth through innovative projects, events, and community engagement in Kenya.
          </p>
        </motion.div>
      </div>
      
      {/* Decorative elements */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M0 120L60 105C120 90 240 60 360 45C480 30 600 30 720 37.5C840 45 960 60 1080 67.5C1200 75 1320 75 1380 75L1440 75V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z" fill="white"/>
        </svg>
      </div>
    </section>
  )
}

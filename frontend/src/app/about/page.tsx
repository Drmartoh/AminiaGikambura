'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import api from '@/services/api'

export default function AboutPage() {
  const [stats, setStats] = useState({ projects: 0, members: 0, events: 0, communities: 0 })

  useEffect(() => {
    Promise.all([
      api.get('/projects/').then((r) => ({ count: (r.data.results || r.data || []).length })),
      api.get('/events/').then((r) => ({ count: (r.data.results || r.data || []).length })),
    ]).then(([projects, events]) => {
      setStats({
        projects: projects.count || 45,
        members: 250,
        events: events.count || 120,
        communities: 15,
      })
    }).catch(() => {})
  }, [])

  const values = [
    {
      icon: '✓',
      title: 'Integrity',
      description: 'We maintain the highest standards of transparency, accountability, and ethical conduct in all our operations and relationships.',
    },
    {
      icon: '👥',
      title: 'Inclusion',
      description: 'We believe every young person deserves a voice and opportunity, regardless of background, gender, or circumstance.',
    },
    {
      icon: '💡',
      title: 'Innovation',
      description: 'We embrace new ideas, technologies, and approaches to solve community challenges and maximize our impact.',
    },
    {
      icon: '🤝',
      title: 'Partnership',
      description: 'We collaborate with County Government, Ministries, donors, and communities to achieve shared development goals.',
    },
    {
      icon: '🌱',
      title: 'Sustainability',
      description: 'We design programs that create lasting change and empower communities to continue development independently.',
    },
    {
      icon: '❤️',
      title: 'Service',
      description: 'We are driven by a genuine commitment to serve our communities and improve the lives of young people.',
    },
  ]

  const focusAreas = [
    {
      title: 'Youth Empowerment',
      description: 'Skills training, mentorship, leadership development, and creating opportunities for young people to thrive.',
      icon: '🎓',
    },
    {
      title: 'Community Development',
      description: 'Infrastructure projects, economic development, and initiatives that improve quality of life in our communities.',
      icon: '🏘️',
    },
    {
      title: 'Agriculture & Food Security',
      description: 'Supporting local farmers, promoting sustainable agriculture, and ensuring food security for our communities.',
      icon: '🌾',
    },
    {
      title: 'Environment & Conservation',
      description: 'Environmental protection, tree planting, waste management, and climate action initiatives.',
      icon: '🌳',
    },
    {
      title: 'Sports & Talent Development',
      description: 'Nurturing athletic talent, promoting physical fitness, and using sports as a tool for youth engagement.',
      icon: '⚽',
    },
    {
      title: 'Education & Training',
      description: 'Scholarships, training programs, workshops, and educational support for youth and community members.',
      icon: '📚',
    },
  ]

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="bg-gradient-to-br from-primary via-primary-light to-teal text-white py-20">
          <div className="container mx-auto px-4">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="max-w-4xl mx-auto text-center"
            >
              <h1 className="text-5xl md:text-6xl font-bold mb-6">About AGCBO</h1>
              <p className="text-xl md:text-2xl text-gray-100 mb-4">
                Aminia Gikambura Community Based Organisation
              </p>
              <p className="text-lg text-gray-200 max-w-2xl mx-auto">
                Empowering youth, transforming communities, and building a better future for Kenya
              </p>
            </motion.div>
          </div>
        </section>

        {/* Impact Stats */}
        <section className="py-12 bg-gray-50 dark:bg-slate-800">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {[
                { label: 'Active Members', value: stats.members, suffix: '+' },
                { label: 'Projects Completed', value: stats.projects, suffix: '+' },
                { label: 'Events Hosted', value: stats.events, suffix: '+' },
                { label: 'Communities Reached', value: stats.communities, suffix: '+' },
              ].map((stat, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: i * 0.1 }}
                  className="text-center"
                >
                  <div className="text-4xl md:text-5xl font-bold text-primary mb-2">
                    {stat.value}{stat.suffix}
                  </div>
                  <div className="text-gray-600 dark:text-gray-400">{stat.label}</div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        <div className="container mx-auto px-4 py-12 max-w-6xl">
          {/* Vision */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <div className="card bg-primary/5 border-l-4 border-primary p-8">
              <h2 className="text-3xl font-bold text-primary mb-4">Our Vision</h2>
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed">
                To be a leading youth-led community-based organisation that empowers young people and transforms communities through sustainable projects, strategic partnerships, and active civic engagement. We envision a future where every young person in Kenya has the skills, opportunities, and support they need to thrive, and where communities are self-reliant, prosperous, and actively contributing to national development goals.
              </p>
            </div>
          </motion.section>

          {/* Mission */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <div className="card bg-accent/5 border-l-4 border-accent p-8">
              <h2 className="text-3xl font-bold text-accent mb-4">Our Mission</h2>
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                To mobilise, equip, and empower youth with the skills, knowledge, and opportunities they need to participate meaningfully in community development, advocate for their rights and interests, and contribute to achieving national goals in alignment with County Government and Ministry priorities.
              </p>
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed">
                We achieve this by implementing innovative projects, fostering partnerships with government and development partners, providing training and mentorship, and creating platforms for youth voice and leadership.
              </p>
            </div>
          </motion.section>

          {/* Core Values */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <h2 className="text-3xl font-bold text-primary mb-8 text-center">Our Core Values</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {values.map((value, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="card hover:shadow-xl transition-shadow"
                >
                  <div className="text-4xl mb-3">{value.icon}</div>
                  <h3 className="text-xl font-bold text-primary mb-2">{value.title}</h3>
                  <p className="text-gray-600 dark:text-gray-400">{value.description}</p>
                </motion.div>
              ))}
            </div>
          </motion.section>

          {/* Our Story */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <h2 className="text-3xl font-bold text-primary mb-6">Our Story</h2>
            <div className="prose dark:prose-invert max-w-none">
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                <strong>Aminia Gikambura Community Based Organisation (AGCBO)</strong> was founded by a group of passionate young leaders who recognized the immense potential of youth in driving community transformation. Registered and operating in Kenya, with a primary focus on <strong>Kiambu County</strong>, AGCBO has grown from a small grassroots initiative to a recognized partner in community development.
              </p>
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-4">
                Our journey began with a simple belief: that young people, when given the right tools, opportunities, and support, can be powerful agents of change in their communities. Over the years, we have worked tirelessly to bridge the gap between youth aspirations and community needs, creating programs that address real challenges while building the capacity of young people.
              </p>
              <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed">
                Today, AGCBO stands as a testament to what is possible when youth leadership, community engagement, and strategic partnerships come together. We continue to expand our reach, deepen our impact, and inspire the next generation of community leaders.
              </p>
            </div>
          </motion.section>

          {/* What We Do */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <h2 className="text-3xl font-bold text-primary mb-8 text-center">What We Do</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {focusAreas.map((area, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, scale: 0.95 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.05 }}
                  className="card hover:shadow-xl transition-all hover:-translate-y-1"
                >
                  <div className="text-4xl mb-3">{area.icon}</div>
                  <h3 className="text-xl font-bold text-primary mb-2">{area.title}</h3>
                  <p className="text-gray-600 dark:text-gray-400">{area.description}</p>
                </motion.div>
              ))}
            </div>
          </motion.section>

          {/* Our Approach */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <h2 className="text-3xl font-bold text-primary mb-6">Our Approach</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="card">
                <h3 className="text-xl font-bold text-primary mb-3">Community-Centered</h3>
                <p className="text-gray-600 dark:text-gray-400">
                  All our programs are designed in consultation with community members, ensuring they address real needs and have local ownership.
                </p>
              </div>
              <div className="card">
                <h3 className="text-xl font-bold text-primary mb-3">Evidence-Based</h3>
                <p className="text-gray-600 dark:text-gray-400">
                  We use data and research to inform our decisions, measure our impact, and continuously improve our programs.
                </p>
              </div>
              <div className="card">
                <h3 className="text-xl font-bold text-primary mb-3">Youth-Led</h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Young people are at the center of everything we do - from planning to implementation to evaluation.
                </p>
              </div>
              <div className="card">
                <h3 className="text-xl font-bold text-primary mb-3">Partnership-Driven</h3>
                <p className="text-gray-600 dark:text-gray-400">
                  We work closely with County Government, Ministries, donors, and other stakeholders to maximize resources and impact.
                </p>
              </div>
            </div>
          </motion.section>

          {/* Registration & Legal */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <div className="card bg-slate-50 dark:bg-slate-800/50 p-8">
              <h2 className="text-3xl font-bold text-primary mb-4">Registration & Legal Status</h2>
              <div className="space-y-3 text-gray-700 dark:text-gray-300">
                <p><strong>Organization Name:</strong> Aminia Gikambura Community Based Organisation (AGCBO)</p>
                <p><strong>Legal Status:</strong> Registered Community Based Organisation</p>
                <p><strong>Registration Number:</strong> [To be updated with actual registration number]</p>
                <p><strong>Primary Operating Area:</strong> Kiambu County, Kenya</p>
                <p><strong>Scope:</strong> National (with focus on Kiambu County)</p>
                <p><strong>Compliance:</strong> We operate in full compliance with Kenyan law and county regulations, and align our reporting with County Government and Ministry standards to ensure transparency and accountability to our funders and beneficiaries.</p>
              </div>
            </div>
          </motion.section>

          {/* Partners & Funders */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <h2 className="text-3xl font-bold text-primary mb-6 text-center">Our Partners & Funders</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="card">
                <h3 className="text-xl font-bold text-primary mb-3">Government Partners</h3>
                <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                  <li>• Kiambu County Government</li>
                  <li>• Ministry of Youth Affairs</li>
                  <li>• Ministry of Agriculture</li>
                  <li>• Ministry of Sports</li>
                  <li>• Ministry of Environment</li>
                </ul>
              </div>
              <div className="card">
                <h3 className="text-xl font-bold text-primary mb-3">Development Partners</h3>
                <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                  <li>• International Donors</li>
                  <li>• Local Business Partners</li>
                  <li>• Community Foundations</li>
                  <li>• NGOs and CSOs</li>
                </ul>
              </div>
            </div>
          </motion.section>

          {/* Get Involved */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <div className="card bg-gradient-to-r from-primary to-teal text-white p-12 text-center">
              <h2 className="text-3xl font-bold mb-4">Join Us in Making a Difference</h2>
              <p className="text-lg mb-8 text-gray-100 max-w-2xl mx-auto">
                Whether you are a young person wanting to join our movement, a donor wishing to support a project, a partner interested in collaboration, or a community member seeking assistance – we would like to hear from you.
              </p>
              <div className="flex flex-wrap justify-center gap-4">
                <Link href="/register" className="btn-accent bg-white text-primary hover:bg-gray-100">
                  Join as a Member
                </Link>
                <Link href="/projects" className="bg-white/20 text-white hover:bg-white/30 border-2 border-white font-semibold py-3 px-6 rounded-xl transition-all">
                  Support a Project
                </Link>
                <Link href="/contact" className="bg-white/20 text-white hover:bg-white/30 border-2 border-white font-semibold py-3 px-6 rounded-xl transition-all">
                  Contact Us
                </Link>
              </div>
            </div>
          </motion.section>

          {/* Contact Information */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <h2 className="text-3xl font-bold text-primary mb-6 text-center">Get in Touch</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="card text-center">
                <div className="text-4xl mb-3">📧</div>
                <h3 className="font-bold text-primary mb-2">Email</h3>
                <p className="text-gray-600 dark:text-gray-400">info@agcbo.org</p>
              </div>
              <div className="card text-center">
                <div className="text-4xl mb-3">📱</div>
                <h3 className="font-bold text-primary mb-2">Phone</h3>
                <p className="text-gray-600 dark:text-gray-400">+254 XXX XXX XXX</p>
              </div>
              <div className="card text-center">
                <div className="text-4xl mb-3">📍</div>
                <h3 className="font-bold text-primary mb-2">Location</h3>
                <p className="text-gray-600 dark:text-gray-400">Kiambu County, Kenya</p>
              </div>
            </div>
          </motion.section>
        </div>
      </main>
      <Footer />
    </div>
  )
}

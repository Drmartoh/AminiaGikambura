import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="bg-primary text-white mt-20">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">AGCBO</h3>
            <p className="text-gray-300 text-sm">
              Empowering youth through community-based projects and engagement in Kenya.
            </p>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/about" className="text-gray-300 hover:text-white transition-colors">About Us</Link></li>
              <li><Link href="/projects" className="text-gray-300 hover:text-white transition-colors">Projects</Link></li>
              <li><Link href="/events" className="text-gray-300 hover:text-white transition-colors">Events</Link></li>
              <li><Link href="/gallery" className="text-gray-300 hover:text-white transition-colors">Gallery</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Resources</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/reports" className="text-gray-300 hover:text-white transition-colors">Reports</Link></li>
              <li><Link href="/sports" className="text-gray-300 hover:text-white transition-colors">Sports</Link></li>
              <li><Link href="/contact" className="text-gray-300 hover:text-white transition-colors">Contact</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Contact</h4>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>Email: info@agcbo.org</li>
              <li>Phone: +254 XXX XXX XXX</li>
              <li>Kiambu County, Kenya</li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-primary-light mt-8 pt-8 text-center text-sm text-gray-300">
          <p>&copy; {new Date().getFullYear()} AGCBO Digital Hub. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

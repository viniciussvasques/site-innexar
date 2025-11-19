import Header from '@/components/Header'
import Contact from '@/components/Contact'
import Footer from '@/components/Footer'
import ContactHero from '@/components/contact/ContactHero'

export default function ContactPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <ContactHero />
      <div className="bg-white">
        <Contact />
      </div>
      <Footer />
    </main>
  )
}
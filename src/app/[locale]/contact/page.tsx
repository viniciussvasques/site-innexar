import Header from '@/components/Header'
import Contact from '@/components/Contact'
import Footer from '@/components/Footer'

export default function ContactPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <div className="pt-16">
        <Contact />
      </div>
      <Footer />
    </main>
  )
}
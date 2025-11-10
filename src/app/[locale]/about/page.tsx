import Header from '@/components/Header'
import About from '@/components/About'
import Footer from '@/components/Footer'

export default function AboutPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <div className="pt-16">
        <About />
      </div>
      <Footer />
    </main>
  )
}
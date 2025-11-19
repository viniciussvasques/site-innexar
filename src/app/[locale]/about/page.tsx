import Header from '@/components/Header'
import About from '@/components/About'
import Footer from '@/components/Footer'
import AboutHero from '@/components/about/AboutHero'
import AboutContent from '@/components/about/AboutContent'

export default function AboutPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <AboutHero />
      <About />
      <AboutContent />
      <Footer />
    </main>
  )
}
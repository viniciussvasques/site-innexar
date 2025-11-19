import Header from '@/components/Header'
import Portfolio from '@/components/Portfolio'
import Footer from '@/components/Footer'
import PortfolioHero from '@/components/portfolio/PortfolioHero'

export default function PortfolioPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <PortfolioHero />
      <Portfolio />
      <Footer />
    </main>
  )
}
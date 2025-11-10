import Header from '@/components/Header'
import Portfolio from '@/components/Portfolio'
import Footer from '@/components/Footer'

export default function PortfolioPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <div className="pt-16">
        <Portfolio />
      </div>
      <Footer />
    </main>
  )
}
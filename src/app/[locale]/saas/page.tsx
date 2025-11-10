import Header from '@/components/Header'
import Footer from '@/components/Footer'
import SaasHero from '@/components/saas/SaasHero'
import SaasFeatures from '@/components/saas/SaasFeatures'
import SaasPricing from '@/components/saas/SaasPricing'
import SaasOverview from '@/components/saas/SaasOverview'
import SaasTestimonials from '@/components/saas/SaasTestimonials'

export default function SaasPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <SaasHero />
      <SaasFeatures />
      <SaasOverview />
      <SaasPricing />
      <SaasTestimonials />
      <Footer />
    </main>
  )
}

import Header from '@/components/Header'
import Footer from '@/components/Footer'
import SaasHero from '@/components/saas/SaasHero'
import SaasFeatures from '@/components/saas/SaasFeatures'
import SaasOverview from '@/components/saas/SaasOverview'
import SaasPricing from '@/components/saas/SaasPricing'
import SaasTestimonials from '@/components/saas/SaasTestimonials'

export default function InnexarSaasPage() {
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



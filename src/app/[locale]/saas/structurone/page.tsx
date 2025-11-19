import Header from '@/components/Header'
import Footer from '@/components/Footer'
import StructurOneHero from '@/components/saas/StructurOneHero'
import StructurOneSection from '@/components/saas/StructurOneSection'

export default function StructurOneSaasPage() {
  return (
    <main className="min-h-screen">
      <Header />
      <StructurOneHero />
      <StructurOneSection />
      <Footer />
    </main>
  )
}



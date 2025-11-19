import Header from '@/components/Header'
import Hero from '@/components/Hero'
import Services from '@/components/Services'
import SuccessStories from '@/components/SuccessStories'
import ProcessSection from '@/components/ProcessSection'
import Technologies from '@/components/Technologies'
import EngagementModels from '@/components/EngagementModels'
import Testimonials from '@/components/Testimonials'
import LeadMagnet from '@/components/LeadMagnet'
import About from '@/components/About'
import Contact from '@/components/Contact'
import Footer from '@/components/Footer'

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <Header />
      <Hero />
      <Services />
      <SuccessStories />
      <ProcessSection />
      <Technologies />
      <EngagementModels />
      <Testimonials />
      <LeadMagnet />
      <About />
      <Contact />
      <Footer />
    </main>
  )
}
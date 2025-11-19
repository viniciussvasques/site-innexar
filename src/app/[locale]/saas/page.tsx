import Header from '@/components/Header'
import Footer from '@/components/Footer'
import SaasSelectorHero from '@/components/saas/SaasSelectorHero'
import { Link } from '@/i18n/navigation'
import { useTranslations } from 'next-intl'
import { ArrowRightIcon } from '@heroicons/react/24/outline'

export default function SaasPage() {
  const t = useTranslations('saas.saasSelector')
  const innexarPointsRaw = t.raw('innexar.points')
  const structuronePointsRaw = t.raw('structurone.points')
  const innexarPoints = Array.isArray(innexarPointsRaw) ? innexarPointsRaw : []
  const structuronePoints = Array.isArray(structuronePointsRaw) ? structuronePointsRaw : []

  return (
    <main className="min-h-screen">
      <Header />
      <SaasSelectorHero />
      <section className="py-24 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              {t('title')}
            </h2>
            <p className="text-lg text-gray-600">
              {t('subtitle')}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Innexar ERP */}
            <div className="group bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 text-left flex flex-col justify-between border border-gray-100 hover:border-blue-200 transform hover:-translate-y-1">
              <div>
                <div className="inline-flex items-center gap-2 rounded-full bg-blue-100 text-blue-700 px-3 py-1 text-xs font-semibold mb-4">
                  ERP Platform
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-3">
                  {t('innexar.title')}
                </h2>
                <p className="text-gray-600 mb-6 leading-relaxed">
                  {t('innexar.description')}
                </p>
                <ul className="space-y-2 mb-6">
                  {innexarPoints.map((p) => (
                    <li key={p} className="flex items-start gap-2 text-gray-600">
                      <span className="text-blue-600 mt-1">✓</span>
                      <span>{p}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <Link
                  href="/saas/innexar"
                  className="inline-flex items-center justify-center gap-2 w-full px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold hover:from-blue-700 hover:to-blue-800 transition-all duration-300 shadow-md hover:shadow-lg"
                >
                  {t('innexar.cta')}
                  <ArrowRightIcon className="h-4 w-4" />
                </Link>
              </div>
            </div>

            {/* StructurOne */}
            <div className="group bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 text-left flex flex-col justify-between border border-gray-100 hover:border-slate-300 transform hover:-translate-y-1">
              <div>
                <div className="inline-flex items-center gap-2 rounded-full bg-slate-100 text-slate-700 px-3 py-1 text-xs font-semibold mb-4">
                  Construction SaaS
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-3">
                  {t('structurone.title')}
                </h2>
                <p className="text-gray-600 mb-6 leading-relaxed">
                  {t('structurone.description')}
                </p>
                <ul className="space-y-2 mb-6">
                  {structuronePoints.map((p) => (
                    <li key={p} className="flex items-start gap-2 text-gray-600">
                      <span className="text-slate-600 mt-1">✓</span>
                      <span>{p}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <Link
                  href="/saas/structurone"
                  className="inline-flex items-center justify-center gap-2 w-full px-6 py-3 rounded-xl bg-gradient-to-r from-slate-900 to-slate-800 text-white font-semibold hover:from-slate-800 hover:to-slate-700 transition-all duration-300 shadow-md hover:shadow-lg"
                >
                  {t('structurone.cta')}
                  <ArrowRightIcon className="h-4 w-4" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </main>
  )
}


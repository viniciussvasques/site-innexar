import { NextIntlClientProvider } from 'next-intl'
import { getMessages } from 'next-intl/server'
import { notFound } from 'next/navigation'
import { Inter } from 'next/font/google'
import { Suspense } from 'react'
import { generateMetadata as genMeta } from '@/lib/seo'
import GoogleAnalytics from '@/components/GoogleAnalytics'
import '../globals.css'

const inter = Inter({ subsets: ['latin'] })

const locales = ['en', 'pt', 'es']

type Props = {
  readonly children: React.ReactNode
  readonly params: Promise<{ locale: string }>
}

export async function generateMetadata({ params }: Props) {
  const { locale } = await params
  return genMeta(locale, 'home')
}

export default async function RootLayout({
  children,
  params
}: Props) {
  const { locale } = await params
  
  // Validate locale
  if (!locales.includes(locale)) {
    notFound()
  }

  const messages = await getMessages({ locale })
  const { generateStructuredData } = await import('@/lib/seo')
  const structuredData = generateStructuredData(locale, 'home')

  // Serializar structured data de forma segura
  const organizationJson = JSON.stringify(structuredData.organization)
  const websiteJson = JSON.stringify(structuredData.website)

  return (
    <html lang={locale} suppressHydrationWarning>
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: organizationJson }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: websiteJson }}
        />
      </head>
      <body className={inter.className}>
        <Suspense fallback={null}>
          <GoogleAnalytics />
        </Suspense>
        <NextIntlClientProvider messages={messages} locale={locale}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  )
}

export function generateStaticParams() {
  return [{ locale: 'en' }, { locale: 'pt' }, { locale: 'es' }]
}

import { NextIntlClientProvider } from 'next-intl'
import { getMessages } from 'next-intl/server'
import { notFound } from 'next/navigation'
import { Inter } from 'next/font/google'
import '../globals.css'

const inter = Inter({ subsets: ['latin'] })

const locales = ['en', 'pt', 'es']

type Props = {
  readonly children: React.ReactNode
  readonly params: Promise<{ locale: string }>
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

  return (
    <html lang={locale} suppressHydrationWarning>
      <body className={inter.className}>
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
import { defineRouting } from 'next-intl/routing'

export const routing = defineRouting({
  locales: ['en', 'pt', 'es'],
  defaultLocale: 'en',
  pathnames: {
    '/': '/',
    '/services': {
      en: '/services',
      pt: '/servicos',
      es: '/servicios'
    },
    '/about': {
      en: '/about',
      pt: '/sobre',
      es: '/acerca'
    },
    '/portfolio': {
      en: '/portfolio',
      pt: '/portfolio',
      es: '/portafolio'
    },
    '/contact': {
      en: '/contact',
      pt: '/contato',
      es: '/contacto'
    }
  }
})

export type Pathnames = keyof typeof routing.pathnames
export type Locale = (typeof routing.locales)[number]
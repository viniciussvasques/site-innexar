'use client';

import { useState } from 'react';
import { Link } from '@/i18n/navigation';
import Image from 'next/image';
import { useTranslations, useLocale } from 'next-intl';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Bars3Icon,
  XMarkIcon,
  ChevronDownIcon,
  GlobeAltIcon,
  EnvelopeIcon,
  PhoneIcon,
} from '@heroicons/react/24/outline';

const languages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'pt', name: 'Português', flag: '🇧🇷' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
];

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [languageMenuOpen, setLanguageMenuOpen] = useState(false);
  const [saasMenuOpen, setSaasMenuOpen] = useState(false);
  const t = useTranslations('navigation');
  const headerT = useTranslations('header');
  const locale = useLocale();

  const navigation: { key: string; name: string; href: string }[] = [
    { key: 'home', name: t('home'), href: '/' },
    { key: 'services', name: t('services'), href: '/services' },
    { key: 'about', name: t('about'), href: '/about' },
    { key: 'portfolio', name: t('portfolio'), href: '/portfolio' },
    { key: 'saas', name: t('saas'), href: '/saas' },
    { key: 'contact', name: t('contact'), href: '/contact' },
  ];

  const currentLanguage = languages.find(lang => lang.code === locale) || languages[0];

  const topEmailValue = headerT('top.emailValue');
  const topPhones = (headerT.raw('top.phones') as { label: string; display: string; href: string }[]) ?? [];
  const topCta = headerT('top.cta');

  const changeLanguage = (newLocale: string) => {
    setLanguageMenuOpen(false);
    setMobileMenuOpen(false);
    
    // Pega o caminho atual sem o locale
    const currentPath = globalThis.location?.pathname || '/';
    // Remove o locale atual do path
    const pathWithoutLocale = currentPath.replace(`/${locale}`, '') || '/';
    
    // Navega para o novo locale
    const newPath = `/${newLocale}${pathWithoutLocale}`;
    globalThis.location?.assign(newPath);
  };

  return (
    <header className="fixed w-full z-50">
      <div className="hidden lg:block bg-slate-900 text-slate-100 text-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <a
              href={`mailto:${topEmailValue}`}
              className="flex items-center gap-2 hover:text-cyan-300 transition-colors"
            >
              <EnvelopeIcon className="h-4 w-4" />
              <span>{topEmailValue}</span>
            </a>
            {topPhones.map((phone) => (
              <a
                key={phone.display}
                href={`tel:${phone.href}`}
                className="flex items-center gap-2 hover:text-cyan-300 transition-colors"
              >
                <PhoneIcon className="h-4 w-4" />
                <span className="hidden xl:inline">
                  {phone.label} • {phone.display}
                </span>
                <span className="xl:hidden">{phone.display}</span>
              </a>
            ))}
          </div>
          <Link
            href="/contact"
            className="px-4 py-1.5 rounded-full text-xs font-semibold bg-white text-slate-900 hover:bg-cyan-200 transition-colors"
          >
            {topCta}
          </Link>
        </div>
      </div>
      <div className="bg-white/95 backdrop-blur-md shadow-sm">
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-20 items-center justify-between">
          {/* Logo */}
          <div className="flex lg:flex-1">
            <Link href="/" className="flex items-center group">
              <Image
                src="/logo-header.svg"
                alt="Innexar"
                width={180}
                height={45}
                className="h-10 w-auto transition-transform duration-300 group-hover:scale-105"
                priority
              />
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex lg:gap-x-2 lg:items-center">
            {navigation.map((item) => {
              const isSaas = item.key === 'saas';

              if (isSaas) {
                // Dropdown para SaaS: Innexar ERP e StructurOne
                return (
                  <div
                    key={item.key}
                    className="relative"
                    onMouseEnter={() => setSaasMenuOpen(true)}
                    onMouseLeave={() => setSaasMenuOpen(false)}
                  >
                    <button
                      className="flex items-center gap-x-1 px-5 py-2.5 text-sm font-medium rounded-lg bg-blue-600 text-white hover:bg-blue-700 shadow-md hover:shadow-lg transition-all duration-200"
                    >
                      <span>{item.name}</span>
                      <ChevronDownIcon className="h-4 w-4" />
                    </button>
                    <AnimatePresence>
                      {saasMenuOpen && (
                        <motion.div
                          initial={{ opacity: 0, y: 4 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: 4 }}
                          transition={{ duration: 0.15 }}
                          className="absolute left-0 mt-2 w-56 bg-white rounded-lg shadow-xl border border-gray-100 py-2 z-50"
                        >
                          <Link
                            href="/saas#innexar-erp"
                            className="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600"
                          >
                            {t('saasInnexar')}
                          </Link>
                          <Link
                            href="/saas#structurone"
                            className="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600"
                          >
                            {t('saasStructurone')}
                          </Link>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                );
              }

              return (
                <Link
                  key={item.key}
                  href={item.href}
                  className="relative px-5 py-2.5 text-sm font-medium rounded-lg text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200"
                >
                  {item.name}
                </Link>
              );
            })}
          </div>

          {/* Language Selector & CTA */}
          <div className="hidden lg:flex lg:flex-1 lg:justify-end lg:gap-x-4 lg:items-center">
            {/* Language Selector */}
            <div className="relative">
              <button
                onClick={() => setLanguageMenuOpen(!languageMenuOpen)}
                className="flex items-center gap-x-2 px-3 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 rounded-lg hover:bg-gray-50 transition-all duration-200"
              >
                <GlobeAltIcon className="h-5 w-5" />
                <span>{currentLanguage.flag}</span>
                <span className="uppercase">{currentLanguage.code}</span>
                <ChevronDownIcon className="h-4 w-4" />
              </button>

              <AnimatePresence>
                {languageMenuOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-100 py-2"
                  >
                    {languages.map((lang) => (
                      <button
                        key={lang.code}
                        onClick={() => changeLanguage(lang.code)}
                        className="flex items-center gap-x-3 w-full px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors"
                      >
                        <span>{lang.flag}</span>
                        <span>{lang.name}</span>
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Get Started Button */}
            <Link
              href="/contact"
              className="px-6 py-2.5 text-sm font-semibold text-white bg-linear-to-r from-blue-600 to-blue-700 rounded-lg hover:from-blue-700 hover:to-blue-800 shadow-md hover:shadow-lg transition-all duration-200"
            >
              {t('getStarted')}
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="flex lg:hidden">
            <button
              type="button"
              className="inline-flex items-center justify-center rounded-lg p-2.5 text-gray-700 hover:bg-gray-100"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <span className="sr-only">Toggle menu</span>
              {mobileMenuOpen ? (
                <XMarkIcon className="h-6 w-6" aria-hidden="true" />
              ) : (
                <Bars3Icon className="h-6 w-6" aria-hidden="true" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="lg:hidden overflow-hidden"
            >
              <div className="space-y-2 pb-4 pt-2">
                {navigation.map((item) => {
                  const isSaas = item.key === 'saas';

                  if (isSaas) {
                    return (
                      <div key={item.key} className="space-y-1 px-2">
                        <div className="px-2 py-2 text-sm font-semibold text-gray-500 uppercase">
                          {item.name}
                        </div>
                        <Link
                          href="/saas#innexar-erp"
                          className="block px-4 py-3 text-base font-medium rounded-lg text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200"
                          onClick={() => setMobileMenuOpen(false)}
                        >
                          {t('saasInnexar')}
                        </Link>
                        <Link
                          href="/saas#structurone"
                          className="block px-4 py-3 text-base font-medium rounded-lg text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200"
                          onClick={() => setMobileMenuOpen(false)}
                        >
                          {t('saasStructurone')}
                        </Link>
                      </div>
                    );
                  }

                  return (
                    <Link
                      key={item.key}
                      href={item.href}
                      className="block px-4 py-3 text-base font-medium rounded-lg text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      {item.name}
                    </Link>
                  );
                })}

                {/* Mobile Language Selector */}
                <div className="pt-4 border-t border-gray-200 space-y-2">
                  {languages.map((lang) => (
                    <button
                      key={lang.code}
                      onClick={() => changeLanguage(lang.code)}
                      className={`flex items-center gap-x-3 w-full px-4 py-3 text-base font-medium rounded-lg transition-all duration-200 ${
                        lang.code === locale
                          ? 'bg-blue-50 text-blue-600'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <span>{lang.flag}</span>
                      <span>{lang.name}</span>
                    </button>
                  ))}
                </div>

                {/* Mobile Get Started Button */}
                <Link
                  href="/contact"
                  className="block mt-4 px-4 py-3 text-center text-base font-semibold text-white bg-linear-to-r from-blue-600 to-blue-700 rounded-lg hover:from-blue-700 hover:to-blue-800 shadow-md"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {t('getStarted')}
                </Link>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>
      </div>
    </header>
  );
}

import type { SupportedLanguage } from '../types';

/**
 * Get default language from browser or user preference
 */
export function getDefaultLanguage(): SupportedLanguage {
  if (typeof window !== 'undefined') {
    const browserLang = navigator.language;
    if (browserLang.startsWith('pt')) return 'pt-BR';
    if (browserLang.startsWith('es')) return 'es-ES';
  }
  return 'en-US';
}

/**
 * Validate if language is supported
 */
export function isSupportedLanguage(lang: string): lang is SupportedLanguage {
  return ['pt-BR', 'en-US', 'es-ES'].includes(lang);
}


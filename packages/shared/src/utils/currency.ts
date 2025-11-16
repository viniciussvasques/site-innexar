import type { SupportedLanguage } from '../types';

/**
 * Format currency value to display format
 * @param amount Amount in cents
 * @param currency Currency code (default: USD)
 * @param locale Locale for formatting (default: en-US)
 * @returns Formatted currency string
 */
export function formatCurrency(
  amount: number,
  currency: string = 'USD',
  locale: SupportedLanguage = 'en-US'
): string {
  const localeMap: Record<SupportedLanguage, string> = {
    'pt-BR': 'pt-BR',
    'en-US': 'en-US',
    'es-ES': 'es-ES',
  };

  const amountInDollars = amount / 100;
  return new Intl.NumberFormat(localeMap[locale], {
    style: 'currency',
    currency: currency,
  }).format(amountInDollars);
}

/**
 * Parse currency string to cents
 * @param value Currency string
 * @returns Amount in cents
 */
export function parseCurrency(value: string): number {
  const numericValue = value.replace(/[^\d.-]/g, '');
  return Math.round(parseFloat(numericValue) * 100);
}


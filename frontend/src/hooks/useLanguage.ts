'use client';

import { useMemo } from 'react';
import { useTranslations } from 'next-intl';
import { authService } from '@/services/auth';

export function useLanguage() {
  const t = useTranslations();
  const user = authService.getCurrentUser();
  
  // Obter idioma do tenant do usuário ou padrão
  const currentLanguage = useMemo(() => {
    if (user?.tenant?.language) {
      return user.tenant.language;
    }
    // Detectar do navegador
    if (typeof window !== 'undefined') {
      const browserLang = navigator.language.toLowerCase();
      if (browserLang.startsWith('pt')) return 'pt-br';
      if (browserLang.startsWith('en')) return 'en-us';
      if (browserLang.startsWith('es')) return 'es-es';
    }
    return 'pt-br';
  }, [user]);

  return {
    t,
    currentLanguage,
    locale: currentLanguage,
  };
}


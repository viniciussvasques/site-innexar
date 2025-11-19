'use client';

import { createContext, useContext, useEffect, useState, useRef, ReactNode } from 'react';
import { authService } from '@/services/auth';
// Importar mensagens padrão de forma estática para evitar flash
import ptBrMessages from '../messages/pt-br.json';

type Language = 'pt-br' | 'en-us' | 'es-es';

type TranslationFunction = (key: string, values?: Record<string, any>) => string;

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: TranslationFunction;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: ReactNode }) {
  // Sempre começar com pt-br para consistência servidor/cliente
  // Começar com mensagens pt-br carregadas para evitar flash de chaves
  const [language, setLanguageState] = useState<Language>('pt-br');
  const [messages, setMessages] = useState<any>(ptBrMessages);
  const [loading, setLoading] = useState(false);
  const [mounted, setMounted] = useState(false);
  const hasCheckedTenantLanguage = useRef(false);
  const initialLoadDone = useRef(false);

  // Detectar idioma apenas no cliente após montagem e carregar mensagens imediatamente
  useEffect(() => {
    setMounted(true);
    
    // Detectar idioma inicial do cliente
    // PRIORIDADE: 1. localStorage (preferência do usuário) > 2. Tenant > 3. Navegador
    const detectLanguage = (): Language => {
      // 1. Verificar localStorage primeiro (preferência do usuário tem prioridade)
      const savedLang = localStorage.getItem('preferred_language');
      if (savedLang && ['pt-br', 'en-us', 'es-es'].includes(savedLang)) {
        return savedLang as Language;
      }
      
      // 2. Se não há preferência salva, usar idioma do tenant
      const user = authService.getCurrentUser();
      if (user?.tenant?.language) {
        const tenantLang = user.tenant.language as Language;
        // Salvar o idioma do tenant como preferência inicial
        localStorage.setItem('preferred_language', tenantLang);
        return tenantLang;
      }
      
      // 3. Detectar do navegador como último recurso
      const browserLang = navigator.language.toLowerCase();
      if (browserLang.startsWith('pt')) return 'pt-br';
      if (browserLang.startsWith('en')) return 'en-us';
      if (browserLang.startsWith('es')) return 'es-es';
      return 'pt-br';
    };

    const detectedLang = detectLanguage();
    
    // Carregar mensagens ANTES de atualizar o idioma para evitar flash de chaves
    const loadMessagesSync = async () => {
      try {
        const mod = await import(`../messages/${detectedLang}.json`);
        setMessages(mod.default);
        setLanguageState(detectedLang); // Atualizar idioma após carregar mensagens
        setLoading(false);
        initialLoadDone.current = true;
      } catch {
        // Fallback para pt-br se houver erro
        const mod = await import('../messages/pt-br.json');
        setMessages(mod.default);
        setLanguageState('pt-br');
        setLoading(false);
        initialLoadDone.current = true;
      }
    };
    
    loadMessagesSync();
  }, []);

  useEffect(() => {
    // Carregar mensagens quando o idioma mudar (apenas após o carregamento inicial)
    if (!mounted || !initialLoadDone.current) return;
    
    const loadMessages = async () => {
      setLoading(true);
      try {
        const mod = await import(`../messages/${language}.json`);
        setMessages(mod.default);
      } catch {
        // Fallback para pt-br se houver erro
        const mod = await import('../messages/pt-br.json');
        setMessages(mod.default);
      } finally {
        setLoading(false);
      }
    };

    loadMessages();
  }, [language, mounted]);

  // Atualizar idioma quando o usuário fizer login (apenas uma vez, se não houver preferência salva)
  useEffect(() => {
    if (!mounted || hasCheckedTenantLanguage.current) return;
    
    // Se o usuário já escolheu um idioma manualmente, respeitar essa escolha
    const savedLang = localStorage.getItem('preferred_language');
    if (savedLang && ['pt-br', 'en-us', 'es-es'].includes(savedLang)) {
      // Usuário já escolheu um idioma, não sobrescrever
      hasCheckedTenantLanguage.current = true;
      return;
    }
    
    // Se não há preferência salva, usar o idioma do tenant (apenas uma vez)
    const user = authService.getCurrentUser();
    if (user?.tenant?.language) {
      const tenantLang = user.tenant.language as Language;
      // Sempre atualizar se não há preferência salva (não comparar com language atual)
      setLanguageState(tenantLang);
      // Salvar o idioma do tenant como preferência inicial
      localStorage.setItem('preferred_language', tenantLang);
    }
    
    hasCheckedTenantLanguage.current = true;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mounted]);

  const setLanguage = async (lang: Language) => {
    setLanguageState(lang);
    // Salvar preferência no localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('preferred_language', lang);
    }
    try {
      const mod = await import(`../messages/${lang}.json`);
      setMessages(mod.default);
    } catch {
      const mod = await import('../messages/pt-br.json');
      setMessages(mod.default);
    }
  };

  // Usar traduções dinâmicas
  const t = (key: string, values?: any) => {
    if (!messages) return key;
    const keys = key.split('.');
    let value: any = messages;
    for (const k of keys) {
      value = value?.[k];
      if (value === undefined) return key;
    }
    if (typeof value === 'string' && values) {
      return value.replace(/\{(\w+)\}/g, (match, key) => values[key] || match);
    }
    return value || key;
  };

  // Sempre fornecer o Context, mesmo durante o carregamento
  // Usar traduções vazias ou fallback durante o carregamento
  const contextValue: LanguageContextType = {
    language,
    setLanguage,
    t: messages ? t : ((key: string) => key), // Retornar a chave durante carregamento
  };

  return (
    <LanguageContext.Provider value={contextValue}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguageContext() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguageContext must be used within LanguageProvider');
  }
  return context;
}


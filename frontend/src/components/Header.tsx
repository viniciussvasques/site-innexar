'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth';
import { useLanguageContext } from './LanguageProvider';
import './Header.css';

interface HeaderProps {
  onMenuClick: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  const router = useRouter();
  const { t, language, setLanguage } = useLanguageContext();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showLangMenu, setShowLangMenu] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [user, setUser] = useState<any>(null);
  const userMenuRef = useRef<HTMLDivElement>(null);
  const langMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMounted(true);
    // Buscar usuário apenas no cliente
    const currentUser = authService.getCurrentUser();
    setUser(currentUser);
  }, []);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setShowUserMenu(false);
      }
      if (langMenuRef.current && !langMenuRef.current.contains(event.target as Node)) {
        setShowLangMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = async () => {
    await authService.logout();
    router.push('/login');
  };

  const languages = [
    { code: 'pt-br', label: '🇧🇷 Português' },
    { code: 'en-us', label: '🇺🇸 English' },
    { code: 'es-es', label: '🇪🇸 Español' },
  ];

  return (
    <header className="dashboard-header">
      <div className="header-left">
        <button className="header-menu-btn" onClick={onMenuClick}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </button>
        <h1 className="header-title">{t('dashboard.header.title')}</h1>
      </div>

      <div className="header-right">
        {/* Language Selector */}
        <div className="header-dropdown" ref={langMenuRef}>
          <button
            className="header-btn"
            onClick={() => setShowLangMenu(!showLangMenu)}
          >
            <span>
              {mounted ? (languages.find(l => l.code === language)?.label || '🌐') : '🌐'}
            </span>
          </button>
          {showLangMenu && (
            <div className="header-dropdown-menu">
              {languages.map((lang) => (
                <button
                  key={lang.code}
                  className={`header-dropdown-item ${language === lang.code ? 'active' : ''}`}
                  onClick={async () => {
                    await setLanguage(lang.code as 'pt-br' | 'en-us' | 'es-es');
                    setShowLangMenu(false);
                  }}
                >
                  {lang.label}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Notifications */}
        <button className="header-btn header-notifications">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path
              d="M10 2C8.34315 2 7 3.34315 7 5V7.58579C6.41751 8.05886 6 8.79524 6 9.5V13.5C6 14.3284 6.67157 15 7.5 15H12.5C13.3284 15 14 14.3284 14 13.5V9.5C14 8.79524 13.5825 8.05886 13 7.58579V5C13 3.34315 11.6569 2 10 2Z"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M8 15V16C8 17.6569 9.34315 19 11 19H9C10.6569 19 12 17.6569 12 16V15"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="header-notification-badge">3</span>
        </button>

        {/* User Menu */}
        <div className="header-dropdown" ref={userMenuRef}>
          <button
            className="header-user-btn"
            onClick={() => setShowUserMenu(!showUserMenu)}
          >
            <div className="header-user-avatar">
              {mounted && user?.first_name?.[0] ? user.first_name[0] : 'U'}
            </div>
            {mounted && user && (
              <div className="header-user-info">
                <span className="header-user-name">
                  {user.first_name} {user.last_name}
                </span>
                <span className="header-user-role">{user.role || 'User'}</span>
              </div>
            )}
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
          {showUserMenu && (
            <div className="header-dropdown-menu">
              <button className="header-dropdown-item">
                <span>👤</span> {t('dashboard.header.profile')}
              </button>
              <button className="header-dropdown-item">
                <span>⚙️</span> {t('dashboard.header.settings')}
              </button>
              <div className="header-dropdown-divider" />
              <button className="header-dropdown-item" onClick={handleLogout}>
                <span>🚪</span> {t('dashboard.header.logout')}
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}


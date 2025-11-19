'use client';

import { useRouter, usePathname } from 'next/navigation';
import { useLanguageContext } from './LanguageProvider';
import './Sidebar.css';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const router = useRouter();
  const pathname = usePathname();
  const { t } = useLanguageContext();

  const menuItems = [
    { path: '/dashboard', icon: '📊', label: t('dashboard.sidebar.dashboard') },
    { path: '/dashboard/projects', icon: '🏗️', label: t('dashboard.sidebar.projects') },
    { path: '/dashboard/investors', icon: '👥', label: t('dashboard.sidebar.investors') },
    { path: '/dashboard/financial', icon: '💰', label: t('dashboard.sidebar.financial') },
    { path: '/dashboard/reports', icon: '📈', label: t('dashboard.sidebar.reports') },
    { path: '/dashboard/settings', icon: '⚙️', label: t('dashboard.sidebar.settings') },
    { path: '/dashboard/billing', icon: '💳', label: t('dashboard.sidebar.billing') },
  ];

  const handleNavigation = (path: string) => {
    router.push(path);
    onClose();
  };

  return (
    <>
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}
      <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="32" height="32" rx="8" fill="url(#logoGradient)"/>
              <path d="M16 8L22 14H19V18H13V14H10L16 8Z" fill="white"/>
              <path d="M8 20L14 26H11V24H21V26H18L24 20L16 12L8 20Z" fill="white" fillOpacity="0.9"/>
              <defs>
                <linearGradient id="logoGradient" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#6366f1"/>
                  <stop offset="1" stopColor="#8b5cf6"/>
                </linearGradient>
              </defs>
            </svg>
            <span className="sidebar-logo-text">StructurOne</span>
          </div>
          <button className="sidebar-close" onClick={onClose}>
            ✕
          </button>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <button
              key={item.path}
              className={`sidebar-item ${pathname === item.path ? 'sidebar-item-active' : ''}`}
              onClick={() => handleNavigation(item.path)}
            >
              <span className="sidebar-item-icon">{item.icon}</span>
              <span className="sidebar-item-label">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-version">
            <span>{t('dashboard.sidebar.version')} 1.0.0</span>
          </div>
        </div>
      </aside>
    </>
  );
}


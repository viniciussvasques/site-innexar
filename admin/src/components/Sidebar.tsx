'use client';

import { usePathname, useRouter } from 'next/navigation';
import Link from 'next/link';
import { useState } from 'react';

interface MenuItem {
  name: string;
  href: string;
  icon: React.ReactNode;
  badge?: number;
}

const menuItems: MenuItem[] = [
  {
    name: 'Dashboard',
    href: '/',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path
          d="M3 4C3 3.44772 3.44772 3 4 3H7C7.55228 3 8 3.44772 8 4V7C8 7.55228 7.55228 8 7 8H4C3.44772 8 3 7.55228 3 7V4Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M12 4C12 3.44772 12.4477 3 13 3H16C16.5523 3 17 3.44772 17 4V7C17 7.55228 16.5523 8 16 8H13C12.4477 8 12 7.55228 12 7V4Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M3 13C3 12.4477 3.44772 12 4 12H7C7.55228 12 8 12.4477 8 13V16C8 16.5523 7.55228 17 7 17H4C3.44772 17 3 16.5523 3 16V13Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M12 13C12 12.4477 12.4477 12 13 12H16C16.5523 12 17 12.4477 17 13V16C17 16.5523 16.5523 17 16 17H13C12.4477 17 12 16.5523 12 16V13Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    name: 'Tenants',
    href: '/tenants',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path
          d="M13 6C13 7.65685 11.6569 9 10 9C8.34315 9 7 7.65685 7 6C7 4.34315 8.34315 3 10 3C11.6569 3 13 4.34315 13 6Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M10 11C7.23858 11 5 13.2386 5 16V17H15V16C15 13.2386 12.7614 11 10 11Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M16 8C16.5523 8 17 7.55228 17 7C17 6.44772 16.5523 6 16 6C15.4477 6 15 6.44772 15 7C15 7.55228 15.4477 8 16 8Z"
          fill="currentColor"
        />
        <path
          d="M17 12C17 12.5523 16.5523 13 16 13C15.4477 13 15 12.5523 15 12C15 11.4477 15.4477 11 16 11C16.5523 11 17 11.4477 17 12Z"
          fill="currentColor"
        />
      </svg>
    ),
  },
  {
    name: 'Projetos',
    href: '/projects',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path
          d="M3 4C3 3.44772 3.44772 3 4 3H16C16.5523 3 17 3.44772 17 4V16C17 16.5523 16.5523 17 16 17H4C3.44772 17 3 16.5523 3 16V4Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M3 8H17"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M7 12H13"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    name: 'Investidores',
    href: '/investors',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path
          d="M10 2L12.09 7.26L18 8.27L14 12.14L14.18 18.02L10 15.77L5.82 18.02L6 12.14L2 8.27L7.91 7.26L10 2Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    name: 'Financeiro',
    href: '/financial',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path
          d="M3 4C3 3.44772 3.44772 3 4 3H16C16.5523 3 17 3.44772 17 4V16C17 16.5523 16.5523 17 16 17H4C3.44772 17 3 16.5523 3 16V4Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M5 7H15"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M5 10H15"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M5 13H12"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    name: 'Billing',
    href: '/billing',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <rect
          x="3"
          y="3"
          width="14"
          height="14"
          rx="2"
          stroke="currentColor"
          strokeWidth="2"
        />
        <path
          d="M7 8H13"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M7 12H11"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </svg>
    ),
  },
  {
    name: 'Documentos',
    href: '/documents',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path
          d="M4 3C4 2.44772 4.44772 2 5 2H11.5858C11.851 2 12.1054 2.10536 12.2929 2.29289L16.7071 6.70711C16.8946 6.89464 17 7.149 17 7.41421V17C17 17.5523 16.5523 18 16 18H5C4.44772 18 4 17.5523 4 17V3Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M11 2V7H16"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    name: 'Atualizações',
    href: '/updates',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path
          d="M10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M10 6V10L13 13"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    name: 'Configurações',
    href: '/settings',
    icon: (
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path
          d="M10 12C11.1046 12 12 11.1046 12 10C12 8.89543 11.1046 8 10 8C8.89543 8 8 8.89543 8 10C8 11.1046 8.89543 12 10 12Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M16.6569 12.3431C16.8444 12.5306 16.9897 12.7576 17.0816 13.0076C17.1735 13.2576 17.2098 13.5247 17.1877 13.7897C17.1656 14.0547 17.0855 14.3115 16.9531 14.5431C16.8207 14.7747 16.6393 14.9756 16.4216 15.1316L16.3431 15.1877C16.1254 15.3437 15.8764 15.4506 15.6131 15.5016C15.3498 15.5526 15.0786 15.5463 14.8181 15.4831L14.1569 15.3123C13.8964 15.2491 13.6252 15.2428 13.3619 15.2938C13.0986 15.3448 12.8496 15.4517 12.6319 15.6077L12.5534 15.6638C12.3357 15.8198 12.1543 16.0207 12.0219 16.2523C11.8895 16.4839 11.8094 16.7407 11.7873 17.0057C11.7652 17.2707 11.8015 17.5378 11.8934 17.7878C11.9853 18.0378 12.1306 18.2648 12.3181 18.4523L12.3431 18.4773C12.5306 18.6648 12.7576 18.8101 13.0076 18.902C13.2576 18.9939 13.5247 19.0302 13.7897 19.0081C14.0547 18.986 14.3115 18.9059 14.5431 18.7735C14.7747 18.6411 14.9756 18.4597 15.1316 18.242L15.1877 18.1635C15.3437 17.9458 15.4506 17.6968 15.5016 17.4335C15.5526 17.1702 15.5463 16.899 15.4831 16.6385L15.3123 15.9773C15.2491 15.7168 15.2428 15.4456 15.2938 15.1823C15.3448 14.919 15.4517 14.67 15.6077 14.4523L15.6638 14.3738C15.8198 14.1561 15.9756 13.9747 16.1316 13.742L16.1877 13.6635C16.3437 13.4458 16.4506 13.1968 16.5016 12.9335C16.5526 12.6702 16.5463 12.399 16.4831 12.1385L16.3123 11.4773C16.2491 11.2168 16.2428 10.9456 16.2938 10.6823C16.3448 10.419 16.4517 10.17 16.6077 9.95234L16.6638 9.87384C16.8198 9.65615 16.9756 9.47473 17.1316 9.24203L17.1877 9.16353C17.3437 8.94584 17.4506 8.69684 17.5016 8.43353C17.5526 8.17022 17.5463 7.899 17.4831 7.63853L17.3123 6.97734C17.2491 6.71684 17.2428 6.44562 17.2938 6.18231C17.3448 5.919 17.4517 5.67 17.6077 5.45234L17.6638 5.37384C17.8198 5.15615 17.9756 4.97473 18.1316 4.74203L18.1877 4.66353C18.3437 4.44584 18.4506 4.19684 18.5016 3.93353C18.5526 3.67022 18.5463 3.399 18.4831 3.13853L18.3123 2.47734C18.2491 2.21684 18.2428 1.94562 18.2938 1.68231C18.3448 1.419 18.4517 1.17 18.6077 0.952344L18.6638 0.873844C18.8198 0.656152 18.9756 0.47473 19.1316 0.242031L19.1877 0.163531"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
];

export default function Sidebar({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const pathname = usePathname();
  const router = useRouter();

  return (
    <>
      {/* Overlay para mobile */}
      {isOpen && (
        <div
          className="sidebar-overlay"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <svg width="32" height="32" viewBox="0 0 48 48" fill="none">
              <rect width="48" height="48" rx="12" fill="url(#gradient)"/>
              <path d="M24 12L32 20H28V28H20V20H16L24 12Z" fill="white"/>
              <path d="M12 32L20 40H16V36H32V40H28L36 32L24 20L12 32Z" fill="white" fillOpacity="0.8"/>
              <defs>
                <linearGradient id="gradient" x1="0" y1="0" x2="48" y2="48" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#6366f1"/>
                  <stop offset="1" stopColor="#8b5cf6"/>
                </linearGradient>
              </defs>
            </svg>
            <div>
              <h2>StructurOne</h2>
              <p>Admin Panel</p>
            </div>
          </div>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => {
            const isActive = pathname === item.href || (item.href !== '/' && pathname?.startsWith(item.href));
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`sidebar-nav-item ${isActive ? 'active' : ''}`}
                onClick={() => {
                  if (window.innerWidth < 768) {
                    onClose();
                  }
                }}
              >
                <span className="sidebar-nav-icon">{item.icon}</span>
                <span className="sidebar-nav-text">{item.name}</span>
                {item.badge && (
                  <span className="sidebar-nav-badge">{item.badge}</span>
                )}
              </Link>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="sidebar-user-avatar">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path
                  d="M12 12C14.7614 12 17 9.76142 17 7C17 4.23858 14.7614 2 12 2C9.23858 2 7 4.23858 7 7C7 9.76142 9.23858 12 12 12Z"
                  fill="currentColor"
                />
                <path
                  d="M12 14C7.58172 14 4 17.5817 4 22H20C20 17.5817 16.4183 14 12 14Z"
                  fill="currentColor"
                />
              </svg>
            </div>
            <div className="sidebar-user-info">
              <p className="sidebar-user-name">Admin</p>
              <p className="sidebar-user-role">Administrador</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}


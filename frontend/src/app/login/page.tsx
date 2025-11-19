'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth';
import { billingService } from '@/services/billing';
import { useLanguageContext } from '@/components/LanguageProvider';
import './login.css';

export default function LoginPage() {
  const router = useRouter();
  const { t } = useLanguageContext();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await authService.login({ email, password });

      console.log('Login result:', result);
      console.log('User data:', result.user);
      console.log('Onboarding completed:', result.user?.onboarding_completed);

      setLoading(false);

      // BLOQUEIO: Verificar assinatura ativa ANTES de liberar acesso
      const hasActiveSub = await billingService.hasActiveSubscription();

      setTimeout(() => {
        if (!hasActiveSub) {
          console.log('❌ SEM ASSINATURA ATIVA → Redirecionando para checkout...');
          window.location.href = '/billing/checkout';
          return;
        }

        if (result.user?.onboarding_completed) {
          console.log('✅ Onboarding completo + assinatura ativa → Dashboard');
          window.location.href = '/dashboard';
        } else {
          console.log('⏭️ Onboarding pendente → Onboarding');
          window.location.href = '/onboarding';
        }
      }, 300);
    } catch (err: any) {
      console.error('Login error:', err);
      setError(err.response?.data?.detail || t('auth.login.error'));
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-background">
        <div className="login-gradient"></div>
        <div className="login-pattern"></div>
      </div>
      
      <div className="login-card">
        <div className="login-header">
          <div className="login-logo">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="64" height="64" rx="16" fill="url(#logoGradient)"/>
              <path d="M32 16L44 28H38V36H26V28H20L32 16Z" fill="white"/>
              <path d="M16 42L28 54H22V50H42V54H36L48 42L32 26L16 42Z" fill="white" fillOpacity="0.9"/>
              <defs>
                <linearGradient id="logoGradient" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
                  <stop stopColor="#6366f1"/>
                  <stop offset="1" stopColor="#8b5cf6"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 className="login-title">StructurOne</h1>
          <p className="login-subtitle">{t('auth.login.subtitle')}</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {error && (
            <div className="login-error">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path
                  d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M10 6V10"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M10 14H10.01"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <span>{error}</span>
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email" className="form-label">
              {t('auth.login.email')}
            </label>
            <div className="form-input-wrapper">
              <svg className="form-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path
                  d="M2.5 6.66667L9.0755 11.0504C9.63533 11.4236 10.3647 11.4236 10.9245 11.0504L17.5 6.66667M3.33333 15H16.6667C17.5871 15 18.3333 14.2538 18.3333 13.3333V6.66667C18.3333 5.74619 17.5871 5 16.6667 5H3.33333C2.41286 5 1.66667 5.74619 1.66667 6.66667V13.3333C1.66667 14.2538 2.41286 15 3.33333 15Z"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seu@email.com"
                required
                autoComplete="email"
                className="form-input"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">
              {t('auth.login.password')}
            </label>
            <div className="form-input-wrapper">
              <svg className="form-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path
                  d="M15.8333 9.16667H4.16667C3.24619 9.16667 2.5 9.91286 2.5 10.8333V15.8333C2.5 16.7538 3.24619 17.5 4.16667 17.5H15.8333C16.7538 17.5 17.5 16.7538 17.5 15.8333V10.8333C17.5 9.91286 16.7538 9.16667 15.8333 9.16667Z"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M5.83333 9.16667V5.83333C5.83333 4.72876 6.27281 3.66895 7.05372 2.88805C7.83462 2.10714 8.89443 1.66667 9.99999 1.66667C11.1056 1.66667 12.1654 2.10714 12.9463 2.88805C13.7272 3.66895 14.1667 4.72876 14.1667 5.83333V9.16667"
                  stroke="currentColor"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                autoComplete="current-password"
                className="form-input"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="form-icon-button"
                tabIndex={-1}
              >
                {showPassword ? (
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path
                      d="M2.5 10C2.5 10 5.83333 5 10 5C14.1667 5 17.5 10 17.5 10C17.5 10 14.1667 15 10 15C5.83333 15 2.5 10 2.5 10Z"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <path
                      d="M10 12.5C11.3807 12.5 12.5 11.3807 12.5 10C12.5 8.61929 11.3807 7.5 10 7.5C8.61929 7.5 7.5 8.61929 7.5 10C7.5 11.3807 8.61929 12.5 10 12.5Z"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path
                      d="M2.5 2.5L17.5 17.5M11.7678 11.7678C11.4678 12.0127 11.1139 12.1923 10.7281 12.2934C10.3423 12.3945 9.93337 12.4144 9.53876 12.3513C9.14415 12.2882 8.77343 12.1439 8.45191 11.9287C8.13038 11.7135 7.86566 11.4325 7.67568 11.1067M2.5 10C2.5 10 5.83333 5 10 5C10.3408 5 10.6742 5.02947 11 5.08571M17.5 10C17.5 10 16.25 12.0833 14.5833 13.3333M12.5 7.91667C13.2934 8.35455 13.9811 8.93714 14.525 9.625"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                )}
              </button>
            </div>
          </div>

          <div className="form-options">
            <a href="/forgot-password" className="form-link">
              {t('auth.login.forgotPassword')}
            </a>
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? (
              <>
                <svg className="spinner" width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <circle
                    cx="10"
                    cy="10"
                    r="8"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeDasharray="31.416"
                    strokeDashoffset="31.416"
                  >
                    <animate
                      attributeName="stroke-dasharray"
                      dur="2s"
                      values="0 31.416;15.708 15.708;0 31.416;0 31.416"
                      repeatCount="indefinite"
                    />
                    <animate
                      attributeName="stroke-dashoffset"
                      dur="2s"
                      values="0;-15.708;-31.416;-31.416"
                      repeatCount="indefinite"
                    />
                  </circle>
                </svg>
                {t('auth.login.submitting')}
              </>
            ) : (
              t('auth.login.submit')
            )}
          </button>
        </form>

        <div className="login-footer">
          <p>
            {t('auth.login.noAccount')}{' '}
            <a href="/register" className="form-link">
              {t('auth.login.register')}
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth';
import { useLanguageContext } from '@/components/LanguageProvider';
import { DashboardLayout } from '@/components/DashboardLayout';
import { StatCard } from '@/components/StatCard';
import api from '@/lib/api';
import { billingService } from '@/services/billing';
import './dashboard.css';

export default function DashboardPage() {
  const router = useRouter();
  const { t } = useLanguageContext();
  const [user, setUser] = useState(authService.getCurrentUser());
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    projects: 0,
    investors: 0,
    revenue: 0,
    investments: 0,
  });

  useEffect(() => {
    let isMounted = true;

    const checkAuth = async () => {
      try {
        // Verificar autenticação
        if (!authService.isAuthenticated()) {
          if (isMounted) {
            router.push('/login');
          }
          return;
        }

        // Buscar dados atualizados do backend
        try {
          const response = await api.get('/auth/me/');
          if (isMounted && response.data) {
            localStorage.setItem('user', JSON.stringify(response.data));
            setUser(response.data);

            // Verificar onboarding
            if (!response.data.onboarding_completed) {
              router.push('/onboarding');
              return;
            }

            // BLOQUEIO: Verificar assinatura ativa ANTES de liberar dashboard
            const hasActiveSub = await billingService.hasActiveSubscription();
            if (!hasActiveSub) {
              console.log('❌ Dashboard bloqueado: sem assinatura ativa → Checkout');
              router.push('/billing/checkout');
              return;
            }
            console.log('✅ Assinatura ativa confirmada → Dashboard liberado');
          }

          // Buscar estatísticas (mock por enquanto)
          // TODO: Substituir por chamada real à API quando disponível
          if (isMounted) {
            setStats({
              projects: 12,
              investors: 45,
              revenue: 2500000,
              investments: 1800000,
            });
          }
        } catch (err: any) {
          if (!isMounted) return;
          
          console.error('Erro ao buscar dados do usuário:', err);
          
          // Se der erro 401, fazer logout
          if (err.response?.status === 401) {
            await authService.logout();
            router.push('/login');
            return;
          }
          
          // Se falhar, usar dados do localStorage
          const localUser = authService.getCurrentUser();
          if (localUser) {
            setUser(localUser);
            if (!localUser.onboarding_completed) {
              router.push('/onboarding');
              return;
            }
          } else {
            router.push('/login');
            return;
          }
        }
      } catch (err) {
        console.error('Erro inesperado:', err);
        if (isMounted) {
          router.push('/login');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    checkAuth();

    return () => {
      isMounted = false;
    };
  }, [router]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="dashboard-loading">
          <div className="dashboard-spinner"></div>
          <p>{t('common.loading')}</p>
        </div>
      </DashboardLayout>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <DashboardLayout>
      <div className="dashboard-page">
        {/* Welcome Section */}
        <div className="dashboard-welcome">
          <div>
            <h1 className="dashboard-welcome-title">
              {t('dashboard.welcome', { name: `${user.first_name} ${user.last_name}` })}
            </h1>
            <p className="dashboard-welcome-subtitle">
              {user.tenant?.name || 'StructurOne'} • {new Date().toLocaleDateString('pt-BR', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </p>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="dashboard-stats-grid">
          <StatCard
            title={t('dashboard.overview.projects')}
            value={stats.projects}
            icon="🏗️"
            color="blue"
            trend={{ value: 12, isPositive: true, label: t('dashboard.overview.vsLastMonth') }}
            subtitle={t('dashboard.overview.inConstruction', { count: 3 })}
          />
          <StatCard
            title={t('dashboard.overview.investors')}
            value={stats.investors}
            icon="👥"
            color="green"
            trend={{ value: 8, isPositive: true, label: t('dashboard.overview.vsLastMonth') }}
            subtitle={t('dashboard.overview.newThisMonth', { count: 5 })}
          />
          <StatCard
            title={t('dashboard.overview.revenue')}
            value={formatCurrency(stats.revenue)}
            icon="💰"
            color="purple"
            trend={{ value: 15, isPositive: true, label: t('dashboard.overview.vsLastMonth') }}
            subtitle={t('dashboard.overview.thisMonth')}
          />
          <StatCard
            title={t('dashboard.overview.investments')}
            value={formatCurrency(stats.investments)}
            icon="📊"
            color="orange"
            trend={{ value: 5, isPositive: true, label: t('dashboard.overview.vsLastMonth') }}
            subtitle={t('dashboard.overview.totalInvested')}
          />
        </div>

        {/* Content Grid */}
        <div className="dashboard-content-grid">
          {/* Recent Projects */}
          <div className="dashboard-card">
            <div className="dashboard-card-header">
              <h2 className="dashboard-card-title">{t('dashboard.overview.recentProjects')}</h2>
              <button className="dashboard-card-action">{t('dashboard.overview.viewAll')}</button>
            </div>
            <div className="dashboard-card-body">
              <div className="dashboard-empty-state">
                <div className="dashboard-empty-icon">🏗️</div>
                <p className="dashboard-empty-text">{t('dashboard.overview.noProjects')}</p>
                <button className="dashboard-empty-action">
                  {t('dashboard.overview.createFirstProject')}
                </button>
              </div>
            </div>
          </div>

          {/* Recent Investors */}
          <div className="dashboard-card">
            <div className="dashboard-card-header">
              <h2 className="dashboard-card-title">{t('dashboard.overview.recentInvestors')}</h2>
              <button className="dashboard-card-action">{t('dashboard.overview.viewAll')}</button>
            </div>
            <div className="dashboard-card-body">
              <div className="dashboard-empty-state">
                <div className="dashboard-empty-icon">👥</div>
                <p className="dashboard-empty-text">{t('dashboard.overview.noInvestors')}</p>
                <button className="dashboard-empty-action">
                  {t('dashboard.overview.addInvestor')}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

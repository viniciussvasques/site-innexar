'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';

interface Plan {
  id: number;
  name: string;
  slug: string;
  description: string;
  price_monthly_brl: string;
  price_monthly_usd: string;
  price_monthly_display?: string;
  is_active: boolean;
  is_featured: boolean;
  trial_days: number;
}

export default function AdminBillingPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadPlans = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.get('/billing/plans/');
        const data = response.data;
        setPlans(Array.isArray(data) ? data : data.results || []);
      } catch (err: any) {
        console.error('Erro ao carregar planos de billing:', err);
        setError(err.response?.data?.detail || 'Erro ao carregar planos de billing.');
      } finally {
        setLoading(false);
      }
    };

    loadPlans();
  }, []);

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h1
          style={{
            fontSize: '2rem',
            fontWeight: 700,
            color: '#1e293b',
            margin: 0,
          }}
        >
          Billing - Planos
        </h1>
        <p style={{ color: '#64748b', marginTop: '0.5rem' }}>
          Visão geral dos planos de assinatura configurados no backend.
        </p>
      </div>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
          <div className="admin-spinner"></div>
        </div>
      ) : error ? (
        <div
          style={{
            padding: '12px 16px',
            borderRadius: '8px',
            backgroundColor: '#fee2e2',
            color: '#b91c1c',
            marginBottom: '16px',
            fontSize: '14px',
          }}
        >
          {error}
        </div>
      ) : (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: '1.5rem',
          }}
        >
          {plans.map((plan) => (
            <div key={plan.id} className="admin-card">
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  marginBottom: '0.75rem',
                }}
              >
                <div>
                  <h2
                    style={{
                      fontSize: '1.125rem',
                      fontWeight: 600,
                      margin: 0,
                      color: '#111827',
                    }}
                  >
                    {plan.name}
                  </h2>
                  <p
                    style={{
                      fontSize: '0.875rem',
                      color: '#6b7280',
                      marginTop: '0.25rem',
                    }}
                  >
                    slug: <code>{plan.slug}</code>
                  </p>
                </div>
                {plan.is_featured && (
                  <span
                    style={{
                      fontSize: '0.75rem',
                      padding: '4px 8px',
                      borderRadius: '999px',
                      background:
                        'linear-gradient(135deg, rgba(129, 140, 248, 0.15), rgba(236, 72, 153, 0.15))',
                      color: '#4f46e5',
                      fontWeight: 600,
                    }}
                  >
                    Destaque
                  </span>
                )}
              </div>

              <p
                style={{
                  fontSize: '0.875rem',
                  color: '#4b5563',
                  marginBottom: '0.75rem',
                }}
              >
                {plan.description}
              </p>

              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: '0.5rem',
                  fontSize: '0.875rem',
                }}
              >
                <div>
                  <strong>BRL:</strong>{' '}
                  <span>R$ {plan.price_monthly_brl || '0,00'}/mês</span>
                </div>
                <div>
                  <strong>USD:</strong>{' '}
                  <span>${plan.price_monthly_usd || '0.00'}/month</span>
                </div>
              </div>

              <div style={{ fontSize: '0.8rem', color: '#6b7280' }}>
                <p style={{ marginBottom: '0.25rem' }}>
                  Status:{' '}
                  <strong style={{ color: plan.is_active ? '#16a34a' : '#9ca3af' }}>
                    {plan.is_active ? 'Ativo' : 'Inativo'}
                  </strong>
                </p>
                <p style={{ marginBottom: '0.25rem' }}>
                  Trial: <strong>{plan.trial_days} dias</strong>
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}



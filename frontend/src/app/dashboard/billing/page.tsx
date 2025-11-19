'use client';

import { useEffect, useState } from 'react';
import { DashboardLayout } from '@/components/DashboardLayout';
import api from '@/lib/api';
import { useLanguageContext } from '@/components/LanguageProvider';
import '../dashboard.css';

interface Plan {
  id: number;
  name: string;
  slug: string;
  description: string;
  price_monthly_display?: string;
  price_yearly_display?: string;
  features?: string[];
}

interface Subscription {
  id: number;
  status: string;
  is_trial: boolean;
  current_period_start: string | null;
  current_period_end: string | null;
  gateway: string | null;
  plan: Plan | null;
}

interface Invoice {
  id: number;
  invoice_number: string;
  total_amount: string;
  amount: string;
  currency: string;
  status: string;
  status_display: string;
  issue_date: string;
  due_date: string;
  paid_at: string | null;
}

interface PaymentMethod {
  id: number;
  type: string;
  gateway: string;
  is_default: boolean;
  is_active: boolean;
  card_display?: string | null;
  card_brand?: string | null;
  card_last4?: string | null;
  card_exp_month?: number | null;
  card_exp_year?: number | null;
}

export default function BillingPage() {
  const { t, language } = useLanguageContext();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);
  const [payingInvoiceId, setPayingInvoiceId] = useState<number | null>(null);
  const [updatingMethodId, setUpdatingMethodId] = useState<number | null>(null);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);

      try {
        const [subscriptionRes, invoicesRes, methodsRes] = await Promise.all([
          api.get('/billing/subscriptions/me/').catch((err) => {
            if (err.response?.status === 404) {
              return null;
            }
            throw err;
          }),
          api.get('/billing/invoices/?page_size=5'),
          api.get('/billing/payment-methods/'),
        ]);

        if (subscriptionRes && subscriptionRes.data) {
          setSubscription(subscriptionRes.data as Subscription);
        }

        const invoicesData = invoicesRes.data.results || invoicesRes.data || [];
        setInvoices(invoicesData as Invoice[]);

        const methodsData = methodsRes.data.results || methodsRes.data || [];
        setPaymentMethods(methodsData as PaymentMethod[]);
      } catch (err: any) {
        console.error('Erro ao carregar billing:', err);
        setError(err.response?.data?.detail || t('common.error'));
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [t]);

  const formatDate = (value: string | null) => {
    if (!value) return '-';
    try {
      const date = new Date(value);
      return date.toLocaleDateString(language || 'pt-BR', {
        year: 'numeric',
        month: 'short',
        day: '2-digit',
      });
    } catch {
      return value;
    }
  };

  const handlePayInvoice = async (invoiceId: number) => {
    setPayingInvoiceId(invoiceId);
    setError(null);

    try {
      await api.post(`/billing/invoices/${invoiceId}/pay/`, {});
      // Recarregar a lista de faturas após o pagamento
      const invoicesRes = await api.get('/billing/invoices/?page_size=5');
      const invoicesData = invoicesRes.data.results || invoicesRes.data || [];
      setInvoices(invoicesData as Invoice[]);
    } catch (err: any) {
      console.error('Erro ao pagar fatura:', err);
      setError(err.response?.data?.detail || t('common.error'));
    } finally {
      setPayingInvoiceId(null);
    }
  };

  const handleSetDefaultMethod = async (methodId: number) => {
    setUpdatingMethodId(methodId);
    setError(null);

    try {
      await api.patch(`/billing/payment-methods/${methodId}/set-default/`, {});
      const methodsRes = await api.get('/billing/payment-methods/');
      const methodsData = methodsRes.data.results || methodsRes.data || [];
      setPaymentMethods(methodsData as PaymentMethod[]);
    } catch (err: any) {
      console.error('Erro ao atualizar método de pagamento:', err);
      setError(err.response?.data?.detail || t('common.error'));
    } finally {
      setUpdatingMethodId(null);
    }
  };

  return (
    <DashboardLayout>
      <div className="dashboard-page">
        <div className="dashboard-welcome">
          <div>
            <h1 className="dashboard-welcome-title">{t('billing.title')}</h1>
            <p className="dashboard-welcome-subtitle">{t('billing.subtitle')}</p>
          </div>
        </div>

        {loading ? (
          <div className="dashboard-loading">
            <div className="dashboard-spinner"></div>
            <p>{t('common.loading')}</p>
          </div>
        ) : (
          <>
            {error && (
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
            )}

            {/* Top grid: current plan + payment methods */}
            <div className="dashboard-stats-grid">
              {/* Current Plan */}
              <div className="dashboard-card">
                <div className="dashboard-card-header">
                  <h2 className="dashboard-card-title">
                    {t('billing.currentPlan.title')}
                  </h2>
                </div>
                <div className="dashboard-card-body">
                      {subscription && subscription.plan ? (
                    <div>
                      <p
                        style={{
                          fontSize: '16px',
                          fontWeight: 600,
                          marginBottom: '4px',
                        }}
                      >
                        {t('billing.currentPlan.plan')}: {subscription.plan.name}
                      </p>
                      {subscription.plan.price_monthly_display && (
                        <p
                          style={{
                            fontSize: '14px',
                            color: '#4b5563',
                            marginBottom: '4px',
                          }}
                        >
                          {subscription.plan.price_monthly_display}
                        </p>
                      )}
                      <p
                        style={{
                          fontSize: '14px',
                          color: '#4b5563',
                          marginBottom: '4px',
                        }}
                      >
                        {t('billing.currentPlan.status')}:{' '}
                        <strong>
                          {subscription.status === 'active'
                            ? t('billing.currentPlan.statusActive')
                            : subscription.is_trial
                            ? t('billing.currentPlan.statusTrial')
                            : t('billing.currentPlan.statusCanceled')}
                        </strong>
                      </p>
                      <p
                        style={{
                          fontSize: '14px',
                          color: '#4b5563',
                          marginBottom: '4px',
                        }}
                      >
                        {t('billing.currentPlan.currentPeriod')}:&nbsp;
                        {formatDate(subscription.current_period_start)} —{' '}
                        {formatDate(subscription.current_period_end)}
                      </p>
                      {subscription.gateway && (
                        <p
                          style={{
                            fontSize: '14px',
                            color: '#4b5563',
                            marginBottom: '4px',
                          }}
                        >
                          {t('billing.currentPlan.gateway')}:&nbsp;
                          <strong>{subscription.gateway.toUpperCase()}</strong>
                        </p>
                      )}
                    </div>
                  ) : (
                    <p
                      style={{
                        fontSize: '14px',
                        color: '#6b7280',
                      }}
                    >
                      {t('billing.currentPlan.noSubscription')}
                    </p>
                  )}
                </div>
              </div>

              {/* Payment Methods */}
              <div className="dashboard-card">
                <div className="dashboard-card-header">
                  <h2 className="dashboard-card-title">
                    {t('billing.paymentMethods.title')}
                  </h2>
                </div>
                <div className="dashboard-card-body">
                              {paymentMethods.length === 0 ? (
                    <p
                      style={{
                        fontSize: '14px',
                        color: '#6b7280',
                        marginBottom: '8px',
                      }}
                    >
                      {t('billing.paymentMethods.empty')}
                    </p>
                  ) : (
                    <ul
                      style={{
                        listStyle: 'none',
                        padding: 0,
                        margin: 0,
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '8px',
                      }}
                    >
                      {paymentMethods.map((method) => (
                        <li
                          key={method.id}
                          style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center',
                            padding: '8px 10px',
                            borderRadius: '8px',
                            border: '1px solid #e5e7eb',
                            backgroundColor: method.is_default
                              ? '#eef2ff'
                              : '#ffffff',
                          }}
                        >
                          <div>
                            <p
                              style={{
                                fontSize: '14px',
                                fontWeight: 500,
                                marginBottom: '2px',
                              }}
                            >
                              {method.card_display ||
                                `${method.gateway.toUpperCase()} - ${method.type}`}
                            </p>
                            <p
                              style={{
                                fontSize: '12px',
                                color: '#6b7280',
                              }}
                            >
                              {t('billing.paymentMethods.card')}{' '}
                              {method.card_last4
                                ? `•••• ${method.card_last4}`
                                : ''}
                            </p>
                          </div>
                          <div style={{ display: 'flex', gap: '8px' }}>
                            {method.is_default && (
                              <span
                                style={{
                                  fontSize: '12px',
                                  padding: '2px 8px',
                                  borderRadius: '999px',
                                  backgroundColor: '#22c55e1a',
                                  color: '#16a34a',
                                  border: '1px solid #bbf7d0',
                                }}
                              >
                                {t('billing.paymentMethods.default')}
                              </span>
                            )}
                            {!method.is_default && (
                              <button
                                type="button"
                                onClick={() => handleSetDefaultMethod(method.id)}
                                disabled={updatingMethodId === method.id}
                                style={{
                                  fontSize: '12px',
                                  padding: '4px 8px',
                                  borderRadius: '999px',
                                  border: '1px solid #e5e7eb',
                                  backgroundColor: '#ffffff',
                                  cursor:
                                    updatingMethodId === method.id
                                      ? 'not-allowed'
                                      : 'pointer',
                                }}
                              >
                                {t('billing.paymentMethods.setDefault')}
                              </button>
                            )}
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}

                  <p
                    style={{
                      fontSize: '12px',
                      color: '#9ca3af',
                      marginTop: '8px',
                    }}
                  >
                    {t('billing.paymentMethods.addingSoon')}
                  </p>
                  <button
                    type="button"
                    disabled
                    style={{
                      marginTop: '8px',
                      width: '100%',
                      padding: '8px 12px',
                      borderRadius: '8px',
                      border: '1px dashed #d1d5db',
                      backgroundColor: '#f9fafb',
                      color: '#9ca3af',
                      fontSize: '13px',
                      cursor: 'not-allowed',
                    }}
                  >
                    {t('billing.paymentMethods.addMethod')}
                  </button>
                </div>
              </div>
            </div>

            {/* Invoices table */}
            <div className="dashboard-card">
              <div className="dashboard-card-header">
                <h2 className="dashboard-card-title">{t('billing.invoices.title')}</h2>
              </div>
              <div className="dashboard-card-body">
                {invoices.length === 0 ? (
                  <p
                    style={{
                      fontSize: '14px',
                      color: '#6b7280',
                    }}
                  >
                    {t('billing.invoices.empty')}
                  </p>
                ) : (
                  <div className="dashboard-table-wrapper">
                    <table className="dashboard-table">
                      <thead>
                        <tr>
                          <th>{t('billing.invoices.invoice')}</th>
                          <th>{t('billing.invoices.status')}</th>
                          <th>{t('billing.invoices.total')}</th>
                          <th>{t('billing.invoices.issueDate')}</th>
                          <th>{t('billing.invoices.dueDate')}</th>
                          <th></th>
                        </tr>
                      </thead>
                      <tbody>
                        {invoices.map((invoice) => (
                          <tr key={invoice.id}>
                            <td>{invoice.invoice_number}</td>
                            <td>{invoice.status_display}</td>
                            <td>
                              {invoice.total_amount} {invoice.currency}
                            </td>
                            <td>{formatDate(invoice.issue_date)}</td>
                            <td>{formatDate(invoice.due_date)}</td>
                            <td>
                              {invoice.status !== 'paid' && (
                                <button
                                  type="button"
                                  onClick={() => handlePayInvoice(invoice.id)}
                                  disabled={payingInvoiceId === invoice.id}
                                  style={{
                                    padding: '6px 10px',
                                    borderRadius: '999px',
                                    border: 'none',
                                    backgroundColor: '#111827',
                                    color: '#ffffff',
                                    fontSize: '12px',
                                    cursor:
                                      payingInvoiceId === invoice.id
                                        ? 'not-allowed'
                                        : 'pointer',
                                  }}
                                >
                                  {payingInvoiceId === invoice.id
                                    ? t('common.loading')
                                    : t('billing.invoices.actions.pay')}
                                </button>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}



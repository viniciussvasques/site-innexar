'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  loadStripe,
  Stripe,
  StripeElements,
  StripeCardElementOptions,
  StripeElementsOptions,
  StripeElementLocale,
} from '@stripe/stripe-js';
import { Elements, ElementsConsumer, CardElement } from '@stripe/react-stripe-js';
import api from '@/lib/api';
import { authService } from '@/services/auth';
import { useLanguageContext } from '@/components/LanguageProvider';
import './checkout.css';

interface Plan {
  id: number;
  name: string;
  slug: string;
  description: string;
  price_monthly_display?: string;
}

interface Invoice {
  id: number;
  invoice_number: string;
  total_amount: string;
  currency: string;
  status: string;
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

type CreatingStep = 'idle' | 'savingCard' | 'generating' | 'paying';

const CARD_ELEMENT_OPTIONS: StripeCardElementOptions = {
  hidePostalCode: true,
  style: {
    base: {
      color: '#0f172a',
      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      fontSize: '16px',
      '::placeholder': {
        color: '#94a3b8',
      },
    },
    invalid: {
      color: '#ef4444',
    },
  },
};

export default function BillingCheckoutPage() {
  const router = useRouter();
  const { t, language } = useLanguageContext();

  const [stripePromise, setStripePromise] = useState<Promise<Stripe | null> | null>(null);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [creatingStep, setCreatingStep] = useState<CreatingStep>('idle');
  const [error, setError] = useState<string | null>(null);
  const [cardError, setCardError] = useState<string | null>(null);

  const [planSlug, setPlanSlug] = useState<string | null>(null);
  const [plan, setPlan] = useState<Plan | null>(null);
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);

  const [billingName, setBillingName] = useState('');
  const [billingEmail, setBillingEmail] = useState('');
  const [cardComplete, setCardComplete] = useState(false);
  const [showCardForm, setShowCardForm] = useState(false);

  const stripeLocale = useMemo<StripeElementLocale>(() => {
    if (!language) return 'auto';
    if (language.startsWith('pt')) return 'pt-BR';
    if (language.startsWith('es')) return 'es';
    return 'en';
  }, [language]);

  const stripeOptions = useMemo<StripeElementsOptions>(
    () => ({
      locale: stripeLocale,
      appearance: {
        theme: 'flat',
        variables: {
          colorPrimary: '#6366f1',
          colorText: '#0f172a',
          colorBackground: '#ffffff',
          colorDanger: '#ef4444',
          borderRadius: '12px',
          fontFamily: 'Inter, "Segoe UI", sans-serif',
          spacingUnit: '6px',
        },
        rules: {
          '.Label': {
            fontSize: '13px',
            fontWeight: '600',
            color: '#0f172a',
          },
          '.Input': {
            borderRadius: '12px',
            padding: '14px 16px',
            border: '1px solid #dfe3ff',
          },
        },
      },
    }),
    [stripeLocale],
  );

  const defaultPaymentMethod = useMemo(
    () => paymentMethods.find((method) => method.is_default) ?? paymentMethods[0] ?? null,
    [paymentMethods],
  );

  useEffect(() => {
    const publishableKey = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;
    if (publishableKey) {
      setStripePromise(loadStripe(publishableKey));
    } else {
      console.warn('NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY não configurada.');
    }
  }, []);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const currentUser = authService.getCurrentUser();
    if (!currentUser) return;

    const fullName = `${currentUser.first_name ?? ''} ${currentUser.last_name ?? ''}`.trim();
    if (fullName) setBillingName(fullName);
    if (currentUser.email) setBillingEmail(currentUser.email);
  }, []);

  useEffect(() => {
    if (!loading && !defaultPaymentMethod) {
      setShowCardForm(true);
    }
  }, [defaultPaymentMethod, loading]);

  const refreshOpenInvoice = useCallback(async () => {
    const response = await api.get('/billing/invoices/?status=open');
    const invoicesData: Invoice[] = response.data.results || response.data || [];
    if (invoicesData.length > 0) {
      setInvoice(invoicesData[0]);
      return invoicesData[0];
    }
    setInvoice(null);
    return null;
  }, []);

  const fetchPaymentMethods = useCallback(async () => {
    const response = await api.get('/billing/payment-methods/');
    const methodsData: PaymentMethod[] = response.data.results || response.data || [];
    setPaymentMethods(methodsData);
    return methodsData;
  }, []);

  useEffect(() => {
    const init = async () => {
      try {
        setError(null);

        if (!authService.isAuthenticated()) {
          router.push('/login');
          return;
        }

        let storedPlanSlug: string | null = null;
        if (typeof window !== 'undefined') {
          storedPlanSlug = localStorage.getItem('structurone_selected_plan');
        }
        setPlanSlug(storedPlanSlug);

        const [plansResponse, invoicesResponse, methodsResponse] = await Promise.all([
          api.get('/billing/plans/'),
          api.get('/billing/invoices/?status=open'),
          api.get('/billing/payment-methods/'),
        ]);

        const plansData: Plan[] = Array.isArray(plansResponse.data)
          ? plansResponse.data
          : plansResponse.data.results || [];

        let matchedPlan = storedPlanSlug
          ? plansData.find((p) => p.slug === storedPlanSlug)
          : undefined;
        if (!matchedPlan && plansData.length > 0) {
          matchedPlan = plansData[0];
        }

        if (!matchedPlan) {
          setError(t('billingCheckout.noPlans'));
          return;
        }
        setPlan(matchedPlan);

        const invoicesData: Invoice[] = invoicesResponse.data.results || invoicesResponse.data || [];
        if (invoicesData.length > 0) {
          setInvoice(invoicesData[0]);
        }

        const methodsData: PaymentMethod[] = methodsResponse.data.results || methodsResponse.data || [];
        setPaymentMethods(methodsData);
        if (methodsData.length === 0) {
          setShowCardForm(true);
        }
      } catch (err: any) {
        console.error('Erro ao carregar checkout:', err);
        setError(err.response?.data?.detail || t('common.error'));
      } finally {
        setLoading(false);
      }
    };

    init();
  }, [router, t]);

  const ctaLabel = useMemo(() => {
    if (creating) {
      if (creatingStep === 'savingCard') return t('billingCheckout.ctaSavingCard');
      if (creatingStep === 'generating') return t('billingCheckout.ctaGenerating');
      return t('billingCheckout.ctaProcessing');
    }

    if (showCardForm) {
      return cardComplete ? t('billingCheckout.ctaGenerate') : t('billingCheckout.ctaEnterCard');
    }

    return invoice ? t('billingCheckout.ctaTest') : t('billingCheckout.ctaGenerate');
  }, [creating, creatingStep, showCardForm, cardComplete, invoice, t]);

  const handleToggleCardForm = useCallback(() => {
    setShowCardForm((prev) => {
      const next = !prev;
      if (next) {
        setCardComplete(false);
        setCardError(null);
      }
      return next;
    });
  }, []);

  const handleCompleteCheckout = useCallback(
    async (stripe?: Stripe | null, elements?: StripeElements | null) => {
      if (!plan) {
        setError(t('billingCheckout.noPlans'));
        return;
      }

      setCreating(true);
      setError(null);
      setCardError(null);

      try {
        let methodsSnapshot = paymentMethods;
        let activeMethod = defaultPaymentMethod;
        let paymentMethodId = activeMethod?.id;

        if (showCardForm) {
          if (!stripe || !elements) {
            setError(t('billingCheckout.missingStripe'));
            return;
          }

          const cardElement = elements.getElement(CardElement);
          if (!cardElement) {
            setError(t('billingCheckout.cardElementMissing'));
            return;
          }

          setCreatingStep('savingCard');
          const { error: stripeError, paymentMethod } = await stripe.createPaymentMethod({
            type: 'card',
            card: cardElement,
            billing_details: {
              name: billingName || undefined,
              email: billingEmail || undefined,
            },
          });

          if (stripeError || !paymentMethod) {
            setCardError(stripeError?.message || t('billingCheckout.cardError'));
            return;
          }

          const methodResponse = await api.post('/billing/payment-methods/', {
            type: 'card',
            token: paymentMethod.id,
            is_default: true,
            billing_details: {
              name: billingName,
              email: billingEmail,
            },
          });

          const newMethod = methodResponse.data as PaymentMethod;
          const others = methodsSnapshot
            .filter((method) => method.id !== newMethod.id)
            .map((method) => ({ ...method, is_default: false }));

          methodsSnapshot = [newMethod, ...others];
          setPaymentMethods(methodsSnapshot);

          activeMethod = newMethod;
          paymentMethodId = newMethod.id;

          elements.getElement(CardElement)?.clear();
          setCardComplete(false);
          setShowCardForm(false);
        }

        let targetInvoice = invoice;

        if (!targetInvoice) {
          if (!paymentMethodId) {
            setError(t('billingCheckout.noPaymentMethod'));
            return;
          }

          setCreatingStep('generating');
          await api.post('/billing/subscriptions/create/', {
            plan_id: plan.id,
            payment_method_id: paymentMethodId,
            billing_cycle: 'monthly',
          });

          targetInvoice = await refreshOpenInvoice();

          if (!targetInvoice) {
            setError(t('billingCheckout.invoiceNotReady'));
            return;
          }
        }

        setCreatingStep('paying');
        await api.post(`/billing/invoices/${targetInvoice.id}/pay/`, {});
        const updatedInvoiceResponse = await api.get(`/billing/invoices/${targetInvoice.id}/`);
        const updatedInvoice = updatedInvoiceResponse.data as Invoice;
        setInvoice(updatedInvoice);

        if (updatedInvoice.status === 'paid') {
          await fetchPaymentMethods();
          setTimeout(() => {
            router.push('/dashboard');
          }, 1600);
        } else {
          await refreshOpenInvoice();
        }
      } catch (err: any) {
        console.error('❌ Erro ao processar pagamento:', err);
        setError(err.response?.data?.detail || t('common.error'));
      } finally {
        setCreating(false);
        setCreatingStep('idle');
      }
    },
    [
      billingEmail,
      billingName,
      cardComplete,
      defaultPaymentMethod,
      fetchPaymentMethods,
      invoice,
      paymentMethods,
      plan,
      refreshOpenInvoice,
      router,
      showCardForm,
      t,
    ],
  );

  const renderInvoiceCard = () => (
    <div className="checkout-invoice-card">
      <p className="checkout-invoice-title">{t('billingCheckout.invoiceTitle')}</p>
      {invoice ? (
        <>
          <p className="checkout-invoice-label">
            {t('billingCheckout.invoiceLabel', {
              number: invoice.invoice_number,
            })}
          </p>
          <p className="checkout-invoice-amount">
            {t('billingCheckout.invoiceAmount', {
              amount: invoice.total_amount,
              currency: invoice.currency,
            })}
            {' • '}
            {t('billingCheckout.invoiceStatus', {
              status: invoice.status,
            })}
          </p>
        </>
      ) : (
        <p className="checkout-invoice-empty">
          {creatingStep === 'generating'
            ? t('billingCheckout.invoiceGenerating')
            : t('billingCheckout.noInvoice')}
        </p>
      )}
    </div>
  );

  const renderActionButton = (stripe?: Stripe | null, elements?: StripeElements | null) => {
    const disabled =
      creating ||
      (showCardForm && (!stripe || !elements || !cardComplete));

    return (
      <button
        type="button"
        disabled={disabled}
        onClick={() => handleCompleteCheckout(stripe, elements)}
        className="checkout-cta-button"
      >
        {creating ? (
          <>
            <svg className="checkout-cta-spinner" width="20" height="20" viewBox="0 0 20 20" fill="none">
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
            {ctaLabel}
          </>
        ) : (
          ctaLabel
        )}
      </button>
    );
  };

  if (loading) {
    return (
      <div className="checkout-loading-container">
        <div className="checkout-loading-spinner" />
        <p>{t('common.loading')}</p>
      </div>
    );
  }

  if (!plan) {
    return (
      <div className="checkout-loading-container">
        <p>{error || t('billingCheckout.noPlans')}</p>
      </div>
    );
  }

  return (
    <div className="checkout-container">
      <div className="checkout-background">
        <div className="checkout-gradient" />
      </div>

      <div className="checkout-card">
        <div className="checkout-left-column">
          <div className="checkout-pill">
            <span className="checkout-pill-dot" />
            {t('billingCheckout.pill')}
          </div>

          <h1 className="checkout-title">{t('billingCheckout.title')}</h1>
          {planSlug && (
            <p className="checkout-subtitle">
              {t('billingCheckout.selectedPlan', { plan: planSlug })}
            </p>
          )}

          <div className="checkout-plan-highlight">
            <div className="checkout-plan-highlight-header">
              <span className="checkout-plan-name">{plan.name}</span>
              {plan.price_monthly_display && (
                <span className="checkout-plan-price">
                  {t('billingCheckout.planPerMonth', {
                    price: plan.price_monthly_display,
                  })}
                </span>
              )}
            </div>
            <p className="checkout-plan-description">{plan.description}</p>
          </div>

          <div className="checkout-before-after">
            <div className="checkout-before-after-header">
              <span className="checkout-before-after-badge">{t('billingCheckout.flowTitle')}</span>
            </div>
            <div className="checkout-before-after-body">
              <div className="checkout-before-card">
                <span className="checkout-emotion-icon">😣</span>
                <p>{t('billingCheckout.flowBefore')}</p>
              </div>
              <div className="checkout-before-after-arrow">⇢</div>
              <div className="checkout-after-card">
                <span className="checkout-emotion-icon">🚀</span>
                <p>{t('billingCheckout.flowAfter')}</p>
              </div>
            </div>
            <p className="checkout-flow-pain">{t('billingCheckout.flowPain')}</p>
          </div>

          <div className="checkout-test-mode-note">
            {t('billingCheckout.testModeNote')}
          </div>
        </div>

        <div className="checkout-right-column">
          <div className="checkout-hero">
            <h2 className="checkout-hero-title">{t('billingCheckout.heroTitle')}</h2>
            <p className="checkout-hero-subtitle">{t('billingCheckout.heroSubtitle')}</p>

            <p className="checkout-benefits-title">{t('billingCheckout.benefitsTitle')}</p>
            <ul className="checkout-benefits-list">
              {[1, 2, 3, 4].map((idx) => (
                <li key={idx} className="checkout-benefit-item">
                  <span className="checkout-benefit-dot" />
                  <span>{t(`billingCheckout.benefit${idx}`)}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="checkout-payment">
            <div className="checkout-payment-header">
              <h3 className="checkout-payment-title">{t('billingCheckout.paymentTitle')}</h3>
              <p className="checkout-payment-subtitle">{t('billingCheckout.paymentSubtitle')}</p>
            </div>

            {defaultPaymentMethod && (
              <div className="checkout-saved-card">
                <div>
                  <p className="checkout-saved-card-title">{t('billingCheckout.savedCardTitle')}</p>
                  <p className="checkout-saved-card-meta">
                    {defaultPaymentMethod.card_display ||
                      `${defaultPaymentMethod.card_brand?.toUpperCase() ?? 'CARD'} •••• ${
                        defaultPaymentMethod.card_last4 ?? '••••'
                      }`}
                  </p>
                </div>
                <button
                  type="button"
                  className="checkout-change-card"
                  onClick={handleToggleCardForm}
                >
                  {showCardForm
                    ? t('billingCheckout.cancelCardChange')
                    : t('billingCheckout.changeCard')}
                </button>
              </div>
            )}

            {showCardForm ? (
              stripePromise ? (
                <Elements stripe={stripePromise} options={stripeOptions}>
                  <ElementsConsumer>
                    {({ stripe, elements }) => (
                      <>
                        <div className="checkout-card-form">
                          <div className="checkout-field">
                            <label className="checkout-field-label" htmlFor="billingName">
                              {t('billingCheckout.cardNameLabel')}
                            </label>
                            <input
                              id="billingName"
                              className="checkout-input"
                              type="text"
                              value={billingName}
                              placeholder={t('billingCheckout.cardNamePlaceholder')}
                              onChange={(event) => setBillingName(event.target.value)}
                            />
                          </div>
                          <div className="checkout-field">
                            <label className="checkout-field-label" htmlFor="billingEmail">
                              {t('billingCheckout.cardEmailLabel')}
                            </label>
                            <input
                              id="billingEmail"
                              className="checkout-input"
                              type="email"
                              value={billingEmail}
                              placeholder={t('billingCheckout.cardEmailPlaceholder')}
                              onChange={(event) => setBillingEmail(event.target.value)}
                            />
                          </div>
                          <div className="checkout-field">
                            <label className="checkout-field-label">{t('billingCheckout.cardFieldLabel')}</label>
                            <div className="checkout-card-element">
                              <CardElement
                                options={CARD_ELEMENT_OPTIONS}
                                onChange={(event) => {
                                  setCardComplete(event.complete);
                                  setCardError(event.error?.message ?? null);
                                }}
                              />
                            </div>
                            <p className="checkout-card-hint">{t('billingCheckout.cardHint')}</p>
                          </div>
                        </div>

                        {cardError && <p className="checkout-card-error">{cardError}</p>}
                        {renderInvoiceCard()}
                        {error && (
                          <div className="checkout-error-box">
                            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                              <path
                                d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z"
                                stroke="currentColor"
                                strokeWidth="2"
                              />
                              <path
                                d="M10 6V10M10 14H10.01"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                              />
                            </svg>
                            <span>{error}</span>
                          </div>
                        )}
                        {renderActionButton(stripe, elements)}
                      </>
                    )}
                  </ElementsConsumer>
                </Elements>
              ) : (
                <div className="checkout-stripe-missing">
                  {t('billingCheckout.stripeKeyMissing')}
                </div>
              )
            ) : (
              <>
                {renderInvoiceCard()}
                {error && (
                  <div className="checkout-error-box">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <path
                        d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z"
                        stroke="currentColor"
                        strokeWidth="2"
                      />
                      <path
                        d="M10 6V10M10 14H10.01"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                    </svg>
                    <span>{error}</span>
                  </div>
                )}
                {renderActionButton()}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}


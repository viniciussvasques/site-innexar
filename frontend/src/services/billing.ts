import api from '@/lib/api';

export interface Subscription {
  id: number;
  status: 'trialing' | 'active' | 'past_due' | 'canceled' | 'unpaid';
  is_active: boolean;
  is_trial: boolean;
}

export const billingService = {
  async getCurrentSubscription(): Promise<Subscription | null> {
    try {
      const res = await api.get('/billing/subscriptions/me/');
      return res.data as Subscription;
    } catch (err: any) {
      if (err.response?.status === 404) {
        return null;
      }
      console.error('Erro ao buscar assinatura atual:', err);
      throw err;
    }
  },

  async hasActiveSubscription(): Promise<boolean> {
    try {
      const sub = await this.getCurrentSubscription();
      if (!sub) return false;
      // Considerar trialing e active como liberados
      return sub.status === 'active' || sub.status === 'trialing' || sub.is_active;
    } catch {
      return false;
    }
  },
};



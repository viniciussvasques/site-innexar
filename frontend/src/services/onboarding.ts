import api from '@/lib/api';

export interface OnboardingData {
  step: number;
  data: any;
}

export interface OnboardingProgress {
  step: number;
  completed: boolean;
  data: any;
}

export const onboardingService = {
  async getProgress(): Promise<OnboardingProgress> {
    const response = await api.get('/onboarding/');
    return response.data;
  },

  async updateStep(step: number, data: any): Promise<OnboardingProgress> {
    const response = await api.post('/onboarding/', { step, data });
    return response.data;
  },

  async complete(): Promise<{ message: string; onboarding_completed: boolean }> {
    const response = await api.post('/onboarding/complete/');
    return response.data;
  },
};


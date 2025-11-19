'use client';

import './StatCard.css';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: string;
  trend?: {
    value: number;
    isPositive: boolean;
    label?: string; // Label traduzido para a tendência
  };
  subtitle?: string;
  color?: 'blue' | 'green' | 'purple' | 'orange';
}

export function StatCard({ title, value, icon, trend, subtitle, color = 'blue' }: StatCardProps) {
  return (
    <div className={`stat-card stat-card-${color}`}>
      <div className="stat-card-header">
        <h3 className="stat-card-title">{title}</h3>
        <div className={`stat-card-icon stat-card-icon-${color}`}>
          {icon}
        </div>
      </div>
      <div className="stat-card-body">
        <div className="stat-card-value">{value}</div>
        {subtitle && <div className="stat-card-subtitle">{subtitle}</div>}
        {trend && (
          <div className={`stat-card-trend ${trend.isPositive ? 'positive' : 'negative'}`}>
            <span>{trend.isPositive ? '↑' : '↓'}</span>
            <span>{Math.abs(trend.value)}%</span>
            {trend.label && <span>{trend.label}</span>}
          </div>
        )}
      </div>
    </div>
  );
}


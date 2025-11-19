'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { tenantsService } from '@/lib/api';

interface Tenant {
  id: number;
  name: string;
  slug: string;
  domain: string;
  email: string;
  is_active: boolean;
  subscription_plan: string;
  is_subscription_active: boolean;
  created_at: string;
}

export default function TenantsPage() {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTenants();
  }, []);

  const fetchTenants = async () => {
    try {
      setLoading(true);
      const data = await tenantsService.list();
      // DRF pode retornar lista direta ou paginada
      let tenantsList = [];
      if (Array.isArray(data)) {
        tenantsList = data;
      } else if (data.results && Array.isArray(data.results)) {
        tenantsList = data.results;
      } else if (data && typeof data === 'object') {
        // Se for um objeto único, converter para array
        tenantsList = [data];
      }
      
      // Filtrar tenants sem ID válido e garantir que todos têm ID
      tenantsList = tenantsList.filter(tenant => {
        if (!tenant || tenant.id === undefined || tenant.id === null) {
          console.warn('Tenant sem ID válido:', tenant);
          return false;
        }
        return true;
      });
      
      console.log('Tenants carregados:', tenantsList.length, tenantsList);
      setTenants(tenantsList);
      setError(null);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.message || 
                          err.message || 
                          'Erro ao carregar tenants';
      setError(errorMessage);
      console.error('Error fetching tenants:', err);
      setTenants([]);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleActive = async (tenantId: number, isActive: boolean) => {
    try {
      // Atualizar o tenant com o novo status
      await tenantsService.update(tenantId, { is_active: !isActive });
      fetchTenants(); // Recarregar lista
    } catch (err: any) {
      console.error('Error toggling tenant status:', err);
      alert(err.response?.data?.detail || 'Erro ao alterar status do tenant');
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
        <div className="admin-spinner"></div>
      </div>
    );
  }

  return (
    <div>
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <div>
              <h1 style={{ fontSize: '2rem', fontWeight: 700, color: '#1e293b', margin: 0 }}>
                Gerenciamento de Tenants
              </h1>
              <p style={{ color: '#64748b', marginTop: '0.5rem' }}>
                Gerencie todos os tenants da plataforma
              </p>
            </div>
            <Link href="/tenants/new" className="admin-btn admin-btn-primary">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path
                  d="M10 4V16M4 10H16"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                />
              </svg>
              Novo Tenant
            </Link>
          </div>
        </div>

        {error && (
          <div className="admin-card" style={{
            backgroundColor: '#fee2e2',
            borderColor: '#fecaca',
            marginBottom: '1.5rem',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: '#991b1b' }}>
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
              <span style={{ fontWeight: 500 }}>{error}</span>
            </div>
          </div>
        )}

        <div className="admin-card">
          <table className="admin-table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>Slug</th>
                <th>Email</th>
                <th>Plano</th>
                <th>Status</th>
                <th>Ações</th>
              </tr>
            </thead>
          <tbody>
            {tenants.map((tenant) => {
              // Garantir que o tenant tem ID válido
              if (!tenant || tenant.id === undefined || tenant.id === null) {
                return null;
              }
              
              return (
                <tr key={tenant.id}>
                  <td>{tenant.name || 'Sem nome'}</td>
                  <td>
                    <code style={{ 
                      background: '#f1f5f9', 
                      padding: '0.25rem 0.5rem', 
                      borderRadius: '4px',
                      fontSize: '0.875rem'
                    }}>
                      {tenant.slug || 'N/A'}
                    </code>
                  </td>
                  <td>{tenant.email || 'N/A'}</td>
                  <td>
                    <span className={`admin-badge admin-badge-info`}>
                      {tenant.subscription_plan || 'N/A'}
                    </span>
                  </td>
                  <td>
                    <span className={`admin-badge ${tenant.is_active ? 'admin-badge-success' : 'admin-badge-danger'}`}>
                      {tenant.is_active ? 'Ativo' : 'Inativo'}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      <Link 
                        href={`/tenants/${String(tenant.id)}`} 
                        className="admin-btn admin-btn-secondary" 
                        style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
                      >
                        Ver
                      </Link>
                    <button
                      onClick={() => handleToggleActive(tenant.id, tenant.is_active)}
                      className={`admin-btn ${tenant.is_active ? 'admin-badge-danger' : 'admin-badge-success'}`}
                      style={{ 
                        padding: '0.5rem 1rem', 
                        fontSize: '0.875rem',
                        background: tenant.is_active ? '#ef4444' : '#10b981',
                        color: 'white',
                        border: 'none'
                      }}
                    >
                      {tenant.is_active ? 'Desativar' : 'Ativar'}
                    </button>
                  </div>
                </td>
              </tr>
              );
            })}
          </tbody>
          </table>
        </div>

        {tenants.length === 0 && !error && (
          <div className="admin-card" style={{ textAlign: 'center', padding: '3rem' }}>
            <svg width="64" height="64" viewBox="0 0 20 20" fill="none" style={{ margin: '0 auto 1rem', color: '#94a3b8' }}>
              <path
                d="M10 10C12.7614 10 15 7.76142 15 5C15 2.23858 12.7614 0 10 0C7.23858 0 5 2.23858 5 5C5 7.76142 7.23858 10 10 10Z"
                stroke="currentColor"
                strokeWidth="2"
              />
              <path
                d="M10 11C6.68629 11 4 13.6863 4 17V20H16V17C16 13.6863 13.3137 11 10 11Z"
                stroke="currentColor"
                strokeWidth="2"
              />
            </svg>
            <p style={{ color: '#64748b', fontSize: '1rem', margin: 0 }}>
              Nenhum tenant cadastrado ainda.
            </p>
            <Link href="/tenants/new" className="admin-btn admin-btn-primary" style={{ marginTop: '1rem' }}>
              Criar Primeiro Tenant
            </Link>
          </div>
        )}
    </div>
  );
}


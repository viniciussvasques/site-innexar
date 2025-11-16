'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8010/api';

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
      // TODO: Adicionar autenticação JWT
      const response = await axios.get(`${API_URL}/tenants/`);
      setTenants(response.data.results || response.data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao carregar tenants');
      console.error('Error fetching tenants:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleActive = async (tenantId: number, isActive: boolean) => {
    try {
      const endpoint = isActive ? 'deactivate' : 'activate';
      await axios.post(`${API_URL}/tenants/${tenantId}/${endpoint}/`);
      fetchTenants(); // Recarregar lista
    } catch (err) {
      console.error('Error toggling tenant status:', err);
      alert('Erro ao alterar status do tenant');
    }
  };

  if (loading) {
    return (
      <div className="admin-container">
        <header className="admin-header">
          <h1>StructurOne Admin</h1>
          <nav>
            <Link href="/tenants">Tenants</Link>
            <Link href="/dashboard">Dashboard</Link>
          </nav>
        </header>
        <main className="admin-main">
          <p>Carregando...</p>
        </main>
      </div>
    );
  }

  return (
    <div className="admin-container">
      <header className="admin-header">
        <h1>StructurOne Admin</h1>
        <nav>
          <Link href="/tenants">Tenants</Link>
          <Link href="/dashboard">Dashboard</Link>
        </nav>
      </header>
      <main className="admin-main">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <h2>Gerenciamento de Tenants</h2>
          <Link href="/tenants/new" style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#0070f3',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '4px',
          }}>
            Novo Tenant
          </Link>
        </div>

        {error && (
          <div style={{
            padding: '1rem',
            backgroundColor: '#fee',
            color: '#c00',
            borderRadius: '4px',
            marginBottom: '1rem',
          }}>
            {error}
          </div>
        )}

        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #ddd' }}>
              <th style={{ padding: '1rem', textAlign: 'left' }}>Nome</th>
              <th style={{ padding: '1rem', textAlign: 'left' }}>Slug</th>
              <th style={{ padding: '1rem', textAlign: 'left' }}>Email</th>
              <th style={{ padding: '1rem', textAlign: 'left' }}>Plano</th>
              <th style={{ padding: '1rem', textAlign: 'left' }}>Status</th>
              <th style={{ padding: '1rem', textAlign: 'left' }}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {tenants.map((tenant) => (
              <tr key={tenant.id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '1rem' }}>{tenant.name}</td>
                <td style={{ padding: '1rem' }}>{tenant.slug}</td>
                <td style={{ padding: '1rem' }}>{tenant.email}</td>
                <td style={{ padding: '1rem' }}>{tenant.subscription_plan}</td>
                <td style={{ padding: '1rem' }}>
                  <span style={{
                    padding: '0.25rem 0.75rem',
                    borderRadius: '12px',
                    fontSize: '0.875rem',
                    backgroundColor: tenant.is_active ? '#d4edda' : '#f8d7da',
                    color: tenant.is_active ? '#155724' : '#721c24',
                  }}>
                    {tenant.is_active ? 'Ativo' : 'Inativo'}
                  </span>
                </td>
                <td style={{ padding: '1rem' }}>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <Link href={`/tenants/${tenant.id}`} style={{
                      padding: '0.5rem 1rem',
                      backgroundColor: '#6c757d',
                      color: 'white',
                      textDecoration: 'none',
                      borderRadius: '4px',
                      fontSize: '0.875rem',
                    }}>
                      Ver
                    </Link>
                    <button
                      onClick={() => handleToggleActive(tenant.id, tenant.is_active)}
                      style={{
                        padding: '0.5rem 1rem',
                        backgroundColor: tenant.is_active ? '#dc3545' : '#28a745',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '0.875rem',
                      }}
                    >
                      {tenant.is_active ? 'Desativar' : 'Ativar'}
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {tenants.length === 0 && !error && (
          <p style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
            Nenhum tenant cadastrado ainda.
          </p>
        )}
      </main>
    </div>
  );
}


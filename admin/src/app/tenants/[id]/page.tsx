'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface Tenant {
  id: number;
  name: string;
  slug: string;
  domain: string;
  email: string;
  phone: string;
  is_active: boolean;
  subscription_plan: string;
  subscription_start_date: string;
  subscription_end_date: string | null;
  max_projects: number;
  max_users: number;
  notes: string;
  is_subscription_active: boolean;
  created_at: string;
  updated_at: string;
}

export default function TenantDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [tenant, setTenant] = useState<Tenant | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (params.id) {
      fetchTenant(Number(params.id));
    }
  }, [params.id]);

  const fetchTenant = async (id: number) => {
    try {
      setLoading(true);
      // TODO: Adicionar autenticação JWT
      const response = await axios.get(`${API_URL}/tenants/${id}/`);
      setTenant(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao carregar tenant');
      console.error('Error fetching tenant:', err);
    } finally {
      setLoading(false);
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

  if (error || !tenant) {
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
          <p>Erro: {error || 'Tenant não encontrado'}</p>
          <Link href="/tenants">Voltar para lista</Link>
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
        <div style={{ marginBottom: '2rem' }}>
          <Link href="/tenants" style={{ color: '#0070f3', textDecoration: 'none' }}>
            ← Voltar para lista
          </Link>
        </div>

        <h2>Detalhes do Tenant: {tenant.name}</h2>

        <div style={{
          backgroundColor: '#f8f9fa',
          padding: '2rem',
          borderRadius: '8px',
          marginTop: '1.5rem',
        }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            <div>
              <strong>Nome:</strong> {tenant.name}
            </div>
            <div>
              <strong>Slug:</strong> {tenant.slug}
            </div>
            <div>
              <strong>Domínio:</strong> {tenant.domain}
            </div>
            <div>
              <strong>Email:</strong> {tenant.email}
            </div>
            <div>
              <strong>Telefone:</strong> {tenant.phone || 'Não informado'}
            </div>
            <div>
              <strong>Status:</strong>{' '}
              <span style={{
                padding: '0.25rem 0.75rem',
                borderRadius: '12px',
                fontSize: '0.875rem',
                backgroundColor: tenant.is_active ? '#d4edda' : '#f8d7da',
                color: tenant.is_active ? '#155724' : '#721c24',
              }}>
                {tenant.is_active ? 'Ativo' : 'Inativo'}
              </span>
            </div>
            <div>
              <strong>Plano:</strong> {tenant.subscription_plan}
            </div>
            <div>
              <strong>Assinatura Ativa:</strong>{' '}
              <span style={{
                padding: '0.25rem 0.75rem',
                borderRadius: '12px',
                fontSize: '0.875rem',
                backgroundColor: tenant.is_subscription_active ? '#d4edda' : '#f8d7da',
                color: tenant.is_subscription_active ? '#155724' : '#721c24',
              }}>
                {tenant.is_subscription_active ? 'Sim' : 'Não'}
              </span>
            </div>
            <div>
              <strong>Máximo de Projetos:</strong> {tenant.max_projects}
            </div>
            <div>
              <strong>Máximo de Usuários:</strong> {tenant.max_users}
            </div>
            <div>
              <strong>Data de Criação:</strong> {new Date(tenant.created_at).toLocaleString('pt-BR')}
            </div>
            <div>
              <strong>Última Atualização:</strong> {new Date(tenant.updated_at).toLocaleString('pt-BR')}
            </div>
          </div>
          {tenant.notes && (
            <div style={{ marginTop: '1.5rem' }}>
              <strong>Observações:</strong>
              <p style={{ marginTop: '0.5rem', padding: '1rem', backgroundColor: 'white', borderRadius: '4px' }}>
                {tenant.notes}
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}


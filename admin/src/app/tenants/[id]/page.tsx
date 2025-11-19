'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { tenantsService } from '@/lib/api';

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
  const [showCredentials, setShowCredentials] = useState(false);
  const [credentials, setCredentials] = useState<{email: string, password?: string} | null>(null);
  const [loadingCredentials, setLoadingCredentials] = useState(false);

  useEffect(() => {
    if (params.id) {
      // params.id pode ser string ou array de strings
      const tenantId = Array.isArray(params.id) ? params.id[0] : params.id;
      
      // Se for "new", redirecionar para a página de criação
      if (tenantId === 'new') {
        router.push('/tenants/new');
        return;
      }
      
      const numericId = parseInt(tenantId, 10);
      if (!isNaN(numericId)) {
        fetchTenant(numericId);
      } else {
        setError('ID do tenant inválido');
        setLoading(false);
      }
    }
  }, [params.id, router]);

  const fetchTenant = async (id: number) => {
    try {
      setLoading(true);
      const data = await tenantsService.get(id);
      setTenant(data);
      setError(null);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.message || 
                          err.message || 
                          'Erro ao carregar tenant';
      setError(errorMessage);
      console.error('Error fetching tenant:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
        <div className="admin-spinner"></div>
      </div>
    );
  }

  if (error || !tenant) {
    return (
      <div>
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
            <span style={{ fontWeight: 500 }}>Erro: {error || 'Tenant não encontrado'}</span>
          </div>
        </div>
        <Link href="/tenants" className="admin-btn admin-btn-secondary">
          ← Voltar para lista
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <Link href="/tenants" className="admin-btn admin-btn-secondary" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path
              d="M7 17L2 12M2 12L7 7M2 12H18"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          Voltar para lista
        </Link>
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, color: '#1e293b', margin: 0 }}>
          Detalhes do Tenant
        </h1>
        <p style={{ color: '#64748b', marginTop: '0.5rem' }}>
          {tenant.name}
        </p>
      </div>

      <div className="admin-card">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Nome</p>
            <p style={{ fontSize: '1rem', fontWeight: 600, color: '#1e293b', margin: 0 }}>{tenant.name}</p>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Slug</p>
            <code style={{ 
              background: '#f1f5f9', 
              padding: '0.5rem 0.75rem', 
              borderRadius: '6px',
              fontSize: '0.875rem',
              display: 'block'
            }}>
              {tenant.slug}
            </code>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Domínio</p>
            <p style={{ fontSize: '1rem', color: '#1e293b', margin: 0 }}>{tenant.domain}</p>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Email</p>
            <p style={{ fontSize: '1rem', color: '#1e293b', margin: 0 }}>{tenant.email}</p>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Telefone</p>
            <p style={{ fontSize: '1rem', color: '#1e293b', margin: 0 }}>{tenant.phone || 'Não informado'}</p>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Status</p>
            <span className={`admin-badge ${tenant.is_active ? 'admin-badge-success' : 'admin-badge-danger'}`}>
              {tenant.is_active ? 'Ativo' : 'Inativo'}
            </span>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Plano</p>
            <span className="admin-badge admin-badge-info">
              {tenant.subscription_plan}
            </span>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Assinatura Ativa</p>
            <span className={`admin-badge ${tenant.is_subscription_active ? 'admin-badge-success' : 'admin-badge-danger'}`}>
              {tenant.is_subscription_active ? 'Sim' : 'Não'}
            </span>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Máximo de Projetos</p>
            <p style={{ fontSize: '1rem', fontWeight: 600, color: '#1e293b', margin: 0 }}>{tenant.max_projects}</p>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Máximo de Usuários</p>
            <p style={{ fontSize: '1rem', fontWeight: 600, color: '#1e293b', margin: 0 }}>{tenant.max_users}</p>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Data de Criação</p>
            <p style={{ fontSize: '1rem', color: '#1e293b', margin: 0 }}>
              {new Date(tenant.created_at).toLocaleString('pt-BR')}
            </p>
          </div>
          <div>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Última Atualização</p>
            <p style={{ fontSize: '1rem', color: '#1e293b', margin: 0 }}>
              {new Date(tenant.updated_at).toLocaleString('pt-BR')}
            </p>
          </div>
        </div>
        
        {tenant.notes && (
          <div style={{ marginTop: '2rem', paddingTop: '2rem', borderTop: '1px solid #e2e8f0' }}>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: '0 0 0.5rem 0' }}>Observações</p>
            <div style={{ 
              padding: '1rem', 
              backgroundColor: '#f8fafc', 
              borderRadius: '8px',
              border: '1px solid #e2e8f0'
            }}>
              <p style={{ margin: 0, color: '#1e293b', whiteSpace: 'pre-wrap' }}>
                {tenant.notes}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Seção de Credenciais do Administrador */}
      <div className="admin-card" style={{ marginTop: '2rem', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ flex: 1, minWidth: '250px' }}>
            <h2 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#1e293b', margin: '0 0 0.5rem 0' }}>
              🔐 Credenciais do Administrador
            </h2>
            <p style={{ fontSize: '0.875rem', color: '#64748b', margin: 0 }}>
              Gerencie as credenciais do primeiro usuário admin deste tenant
            </p>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            <button
              onClick={async () => {
                setLoadingCredentials(true);
                try {
                  const creds = await tenantsService.getAdminCredentials(tenant.id);
                  setCredentials(creds);
                  setShowCredentials(true);
                } catch (err: any) {
                  alert(err.response?.data?.detail || 'Erro ao buscar credenciais');
                } finally {
                  setLoadingCredentials(false);
                }
              }}
              className="admin-btn admin-btn-secondary"
              disabled={loadingCredentials}
              style={{ minWidth: '120px' }}
            >
              {loadingCredentials ? 'Carregando...' : '👁️ Ver Email'}
            </button>
            <button
              onClick={async () => {
                if (!confirm('Tem certeza que deseja resetar a senha do administrador? Uma nova senha será gerada.')) {
                  return;
                }
                setLoadingCredentials(true);
                try {
                  const result = await tenantsService.resetAdminPassword(tenant.id);
                  setCredentials({
                    email: result.email,
                    password: result.new_password,
                  });
                  setShowCredentials(true);
                  alert('Senha resetada com sucesso! A nova senha está sendo exibida abaixo.');
                } catch (err: any) {
                  alert(err.response?.data?.detail || 'Erro ao resetar senha');
                } finally {
                  setLoadingCredentials(false);
                }
              }}
              className="admin-btn admin-btn-primary"
              disabled={loadingCredentials}
              style={{ minWidth: '140px' }}
            >
              🔄 Resetar Senha
            </button>
          </div>
        </div>

        {!showCredentials && (
          <div style={{
            padding: '1rem',
            backgroundColor: '#f8fafc',
            borderRadius: '8px',
            border: '1px dashed #cbd5e1',
            textAlign: 'center',
            color: '#64748b',
            fontSize: '0.875rem'
          }}>
            Clique em "Ver Email" para visualizar o email do administrador ou "Resetar Senha" para gerar uma nova senha.
          </div>
        )}

        {showCredentials && credentials && (
          <div style={{
            marginTop: '1.5rem',
            padding: '1.5rem',
            backgroundColor: '#f0fdf4',
            borderRadius: '12px',
            border: '2px solid #86efac',
          }}>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ fontSize: '0.875rem', fontWeight: 600, color: '#374151', display: 'block', marginBottom: '0.5rem' }}>
                Email do Administrador:
              </label>
              <code style={{
                display: 'block',
                padding: '0.75rem',
                backgroundColor: 'white',
                borderRadius: '8px',
                fontSize: '0.875rem',
                fontFamily: 'monospace',
                color: '#1e293b',
                border: '1px solid #86efac',
              }}>
                {credentials.email}
              </code>
            </div>
            {credentials.password && (
              <div>
                <label style={{ fontSize: '0.875rem', fontWeight: 600, color: '#374151', display: 'block', marginBottom: '0.5rem' }}>
                  Nova Senha:
                </label>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                  <code style={{
                    flex: 1,
                    padding: '0.75rem',
                    backgroundColor: 'white',
                    borderRadius: '8px',
                    fontSize: '0.875rem',
                    fontFamily: 'monospace',
                    color: '#1e293b',
                    fontWeight: 600,
                    border: '1px solid #86efac',
                  }}>
                    {credentials.password}
                  </code>
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(credentials.password || '');
                      alert('Senha copiada!');
                    }}
                    className="admin-btn admin-btn-secondary"
                    style={{ padding: '0.75rem 1rem' }}
                  >
                    📋 Copiar
                  </button>
                </div>
                <p style={{ fontSize: '0.75rem', color: '#64748b', margin: '0.5rem 0 0 0' }}>
                  ⚠️ Anote esta senha! Ela não poderá ser recuperada novamente.
                </p>
              </div>
            )}
            {!credentials.password && (
              <p style={{ fontSize: '0.875rem', color: '#64748b', margin: 0 }}>
                A senha não pode ser recuperada. Use o botão "Resetar Senha" para gerar uma nova senha.
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}


'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { tenantsService } from '@/lib/api';

interface TenantFormData {
  name: string;
  slug: string;
  domain: string;
  email: string;
  phone: string;
  subscription_plan: string;
  max_projects: number;
  max_users: number;
  notes: string;
}

export default function NewTenantPage() {
  const router = useRouter();
  const [formData, setFormData] = useState<TenantFormData>({
    name: '',
    slug: '',
    domain: '',
    email: '',
    phone: '',
    subscription_plan: 'basic',
    max_projects: 10,
    max_users: 5,
    notes: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [slugManuallyEdited, setSlugManuallyEdited] = useState(false);
  const [createdCredentials, setCreatedCredentials] = useState<{email: string, password: string} | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'max_projects' || name === 'max_users' ? parseInt(value, 10) || 0 : value,
    }));

    // Auto-gerar slug e domain baseado no nome
    if (name === 'name' && value) {
      const slug = value
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '') // Remove acentos
        .replace(/[^a-z0-9]+/g, '-') // Substitui caracteres especiais por hífen
        .replace(/(^-+|-+$)/g, '') // Remove hífens no início e fim
        .trim();
      
      // Só atualizar slug se não foi editado manualmente
      setFormData(prev => ({
        ...prev,
        slug: slugManuallyEdited ? prev.slug : (slug || prev.slug),
        domain: slugManuallyEdited ? prev.domain : (slug ? `${slug}.structurone.com` : prev.domain),
      }));
    }

    // Auto-gerar domain baseado no slug quando o slug mudar
    if (name === 'slug' && value) {
      setSlugManuallyEdited(true); // Marcar que o slug foi editado manualmente
      const cleanSlug = value
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '') // Remove acentos
        .replace(/[^a-z0-9-]+/g, '') // Remove caracteres inválidos, mantém hífens
        .replace(/(^-+|-+$)/g, '') // Remove hífens no início e fim
        .trim();
      
      setFormData(prev => ({
        ...prev,
        slug: cleanSlug,
        domain: cleanSlug ? `${cleanSlug}.structurone.com` : '', // Sempre atualizar o domínio
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      const tenant = await tenantsService.create(formData);
      console.log('Tenant criado:', tenant);
      
      // Verificar se há credenciais na resposta
      if (tenant.admin_credentials) {
        setCreatedCredentials({
          email: tenant.admin_credentials.email,
          password: tenant.admin_credentials.password,
        });
        setIsSubmitting(false);
        // Não redirecionar ainda, mostrar credenciais
        return;
      }
      
      // Verificar se o tenant tem ID
      if (tenant && tenant.id) {
        router.push(`/tenants/${tenant.id}`);
      } else {
        // Se não tiver ID na resposta, buscar novamente ou redirecionar para lista
        console.warn('Tenant criado mas sem ID na resposta:', tenant);
        router.push('/tenants');
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 
                          err.response?.data?.message ||
                          (err.response?.data && typeof err.response.data === 'object' 
                            ? JSON.stringify(err.response.data)
                            : err.message) ||
                          'Erro ao criar tenant';
      setError(errorMessage);
      console.error('Error creating tenant:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

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
          Novo Tenant
        </h1>
        <p style={{ color: '#64748b', marginTop: '0.5rem' }}>
          Crie um novo tenant na plataforma
        </p>
      </div>

      {createdCredentials && (
        <div className="admin-card" style={{
          backgroundColor: '#f0fdf4',
          borderColor: '#86efac',
          marginBottom: '1.5rem',
        }}>
          <div style={{ marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#166534', margin: '0 0 0.5rem 0' }}>
              ✅ Tenant criado com sucesso!
            </h3>
            <p style={{ color: '#166534', margin: 0 }}>
              Credenciais do usuário administrador:
            </p>
          </div>
          <div style={{
            padding: '1rem',
            backgroundColor: 'white',
            borderRadius: '8px',
            border: '2px solid #86efac',
            marginBottom: '1rem',
          }}>
            <div style={{ marginBottom: '0.75rem' }}>
              <label style={{ fontSize: '0.875rem', fontWeight: 600, color: '#374151', display: 'block', marginBottom: '0.25rem' }}>
                Email:
              </label>
              <code style={{
                display: 'block',
                padding: '0.5rem',
                backgroundColor: '#f1f5f9',
                borderRadius: '4px',
                fontSize: '0.875rem',
                fontFamily: 'monospace',
                color: '#1e293b',
              }}>
                {createdCredentials.email}
              </code>
            </div>
            <div>
              <label style={{ fontSize: '0.875rem', fontWeight: 600, color: '#374151', display: 'block', marginBottom: '0.25rem' }}>
                Senha:
              </label>
              <code style={{
                display: 'block',
                padding: '0.5rem',
                backgroundColor: '#f1f5f9',
                borderRadius: '4px',
                fontSize: '0.875rem',
                fontFamily: 'monospace',
                color: '#1e293b',
                fontWeight: 600,
              }}>
                {createdCredentials.password}
              </code>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              onClick={() => {
                navigator.clipboard.writeText(`${createdCredentials.email}\n${createdCredentials.password}`);
                alert('Credenciais copiadas para a área de transferência!');
              }}
              className="admin-btn admin-btn-secondary"
              style={{ flex: 1 }}
            >
              📋 Copiar Credenciais
            </button>
            <Link href="/tenants" className="admin-btn admin-btn-primary" style={{ flex: 1, textAlign: 'center', textDecoration: 'none' }}>
              Ver Lista de Tenants
            </Link>
          </div>
        </div>
      )}

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

      {!createdCredentials && (
      <div className="admin-card">
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginBottom: '1.5rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#374151', marginBottom: '0.5rem' }}>
                Nome da Empresa *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  outline: 'none',
                  transition: 'border-color 0.2s',
                }}
                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#374151', marginBottom: '0.5rem' }}>
                Slug *
              </label>
              <input
                type="text"
                name="slug"
                value={formData.slug}
                onChange={handleChange}
                required
                pattern="[a-z0-9-]+"
                title="Apenas letras minúsculas, números e hífens"
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  fontFamily: 'monospace',
                  outline: 'none',
                  transition: 'border-color 0.2s',
                }}
                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#374151', marginBottom: '0.5rem' }}>
                Domínio *
              </label>
              <input
                type="text"
                name="domain"
                value={formData.domain}
                onChange={handleChange}
                required
                readOnly
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  outline: 'none',
                  backgroundColor: '#f8fafc',
                  color: '#64748b',
                  cursor: 'not-allowed',
                }}
                title="Domínio gerado automaticamente baseado no slug"
              />
              <p style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem', margin: '0.25rem 0 0 0' }}>
                Gerado automaticamente baseado no slug
              </p>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#374151', marginBottom: '0.5rem' }}>
                Email *
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  outline: 'none',
                  transition: 'border-color 0.2s',
                }}
                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#374151', marginBottom: '0.5rem' }}>
                Telefone
              </label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  outline: 'none',
                  transition: 'border-color 0.2s',
                }}
                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#374151', marginBottom: '0.5rem' }}>
                Plano de Assinatura *
              </label>
              <select
                name="subscription_plan"
                value={formData.subscription_plan}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  outline: 'none',
                  transition: 'border-color 0.2s',
                  backgroundColor: 'white',
                }}
                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
              >
                <option value="free">Gratuito</option>
                <option value="basic">Básico</option>
                <option value="professional">Profissional</option>
                <option value="enterprise">Enterprise</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#374151', marginBottom: '0.5rem' }}>
                Máximo de Projetos
              </label>
              <input
                type="number"
                name="max_projects"
                value={formData.max_projects}
                onChange={handleChange}
                min="1"
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  outline: 'none',
                  transition: 'border-color 0.2s',
                }}
                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#374151', marginBottom: '0.5rem' }}>
                Máximo de Usuários
              </label>
              <input
                type="number"
                name="max_users"
                value={formData.max_users}
                onChange={handleChange}
                min="1"
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '0.875rem',
                  outline: 'none',
                  transition: 'border-color 0.2s',
                }}
                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
              />
            </div>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#374151', marginBottom: '0.5rem' }}>
              Observações
            </label>
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              rows={4}
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                fontSize: '0.875rem',
                outline: 'none',
                transition: 'border-color 0.2s',
                fontFamily: 'inherit',
                resize: 'vertical',
              }}
              onFocus={(e) => e.target.style.borderColor = '#6366f1'}
              onBlur={(e) => e.target.style.borderColor = '#d1d5db'}
            />
          </div>

          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
            <Link href="/tenants" className="admin-btn admin-btn-secondary">
              Cancelar
            </Link>
            <button
              type="submit"
              className="admin-btn admin-btn-primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <div className="admin-spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></div>
                  Criando...
                </>
              ) : (
                <>
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path
                      d="M10 4V16M4 10H16"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  </svg>
                  Criar Tenant
                </>
              )}
            </button>
          </div>
        </form>
      </div>
      )}
    </div>
  );
}


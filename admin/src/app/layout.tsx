import type { Metadata } from 'next';
import './globals.css';
import './admin.css';
import AdminLayout from '@/components/AdminLayout';

export const metadata: Metadata = {
  title: 'StructurOne Admin - Painel Administrativo',
  description: 'Painel administrativo da plataforma StructurOne',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>
        <AdminLayout>{children}</AdminLayout>
      </body>
    </html>
  );
}


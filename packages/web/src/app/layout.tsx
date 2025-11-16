import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'StructurOne - Gestão de Empreendimentos',
  description: 'Plataforma SaaS para gestão completa de empreendimentos e captação de investimentos',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}


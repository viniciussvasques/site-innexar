import type { Metadata } from 'next';
import './globals.css';

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
      <body>{children}</body>
    </html>
  );
}


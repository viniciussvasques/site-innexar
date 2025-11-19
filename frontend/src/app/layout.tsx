import type { Metadata } from 'next';
import { LanguageProviderWrapper } from '@/components/LanguageProviderWrapper';
import './globals.css';

export const metadata: Metadata = {
  title: 'StructurOne',
  description: 'Plataforma SaaS para gestão de empreendimentos',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>
        <LanguageProviderWrapper>
          {children}
        </LanguageProviderWrapper>
      </body>
    </html>
  );
}

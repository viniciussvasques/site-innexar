import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Rotas públicas (incluindo onboarding e dashboard, que verificam autenticação no cliente)
  const publicRoutes = [
    '/login', 
    '/register', 
    '/forgot-password', 
    '/reset-password', 
    '/onboarding',
    '/dashboard' // Dashboard verifica autenticação no cliente
  ];
  const isPublicRoute = publicRoutes.some(route => pathname.startsWith(route));

  // Se está em rota pública, permitir acesso (verificação de auth no cliente)
  if (isPublicRoute || pathname === '/') {
    return NextResponse.next();
  }

  // Para outras rotas, permitir acesso (verificação de auth no cliente)
  // O middleware não bloqueia, mas o cliente verifica e redireciona se necessário
  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};

'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function AdminHome() {
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
        <h2>Bem-vindo ao Painel Administrativo</h2>
        <p>Selecione uma opção no menu acima para começar.</p>
      </main>
    </div>
  );
}


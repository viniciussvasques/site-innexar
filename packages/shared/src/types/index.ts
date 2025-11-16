// Multi-tenant types
export interface Tenant {
  id: string;
  name: string;
  slug: string;
  createdAt: Date;
  updatedAt: Date;
}

// Project types
export interface Project {
  id: string;
  tenantId: string;
  name: string;
  description?: string;
  status: ProjectStatus;
  completionPercentage: number;
  startDate: Date;
  expectedEndDate?: Date;
  createdAt: Date;
  updatedAt: Date;
}

export enum ProjectStatus {
  PLANNING = 'planning',
  IN_PROGRESS = 'in_progress',
  ON_HOLD = 'on_hold',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

// Investor types
export interface Investor {
  id: string;
  tenantId: string;
  name: string;
  email: string;
  phone?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Investment types
export interface Investment {
  id: string;
  tenantId: string;
  projectId: string;
  investorId: string;
  amount: number;
  currency: string;
  status: InvestmentStatus;
  createdAt: Date;
  updatedAt: Date;
}

export enum InvestmentStatus {
  PENDING = 'pending',
  CONFIRMED = 'confirmed',
  CANCELLED = 'cancelled',
}

// Financial types
export interface FinancialTransaction {
  id: string;
  tenantId: string;
  projectId?: string;
  type: TransactionType;
  amount: number;
  currency: string;
  description?: string;
  date: Date;
  createdAt: Date;
}

export enum TransactionType {
  INCOME = 'income',
  EXPENSE = 'expense',
}

// Document types
export interface Document {
  id: string;
  tenantId: string;
  projectId?: string;
  name: string;
  type: DocumentType;
  url: string;
  size: number;
  mimeType: string;
  uploadedAt: Date;
}

export enum DocumentType {
  CONTRACT = 'contract',
  INVOICE = 'invoice',
  RECEIPT = 'receipt',
  OTHER = 'other',
}

// Update types
export interface ProjectUpdate {
  id: string;
  tenantId: string;
  projectId: string;
  title: string;
  description?: string;
  completionPercentage: number;
  photos?: string[];
  videos?: string[];
  createdAt: Date;
}

// User types
export interface User {
  id: string;
  tenantId: string;
  email: string;
  name: string;
  role: UserRole;
  createdAt: Date;
  updatedAt: Date;
}

export enum UserRole {
  ADMIN = 'admin',
  MANAGER = 'manager',
  INVESTOR = 'investor',
}

// Language types
export type SupportedLanguage = 'pt-BR' | 'en-US' | 'es-ES';


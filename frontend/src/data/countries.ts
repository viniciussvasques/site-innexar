// Configurações de países para onboarding de construtoras/incorporadoras

export interface CountryConfig {
  code: string;
  name: string;
  taxIdLabel: string;
  taxIdPlaceholder: string;
  taxIdPattern?: string;
  taxIdMask?: (value: string) => string;
  currency: string;
  currencySymbol: string;
  language: string;
  timezone: string;
  dateFormat: string;
  numberFormat: string;
  phoneFormat?: string;
  addressFormat: {
    fields: string[];
    required: string[];
  };
  companyTypes: string[];
}

export const COUNTRIES: Record<string, CountryConfig> = {
  BR: {
    code: 'BR',
    name: 'Brasil',
    taxIdLabel: 'CNPJ',
    taxIdPlaceholder: '00.000.000/0000-00',
    taxIdPattern: '^\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}$',
    taxIdMask: (value: string) => {
      const numbers = value.replace(/\D/g, '');
      if (numbers.length <= 14) {
        return numbers
          .replace(/(\d{2})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1/$2')
          .replace(/(\d{4})(\d)/, '$1-$2');
      }
      return value;
    },
    currency: 'BRL',
    currencySymbol: 'R$',
    language: 'pt-br',
    timezone: 'America/Sao_Paulo',
    dateFormat: 'DD/MM/YYYY',
    numberFormat: '1.234,56',
    phoneFormat: '(00) 00000-0000',
    addressFormat: {
      fields: ['street', 'number', 'complement', 'neighborhood', 'city', 'state', 'zipcode'],
      required: ['street', 'number', 'city', 'state', 'zipcode'],
    },
    companyTypes: ['Construtora', 'Incorporadora', 'Construtora e Incorporadora', 'Imobiliária'],
  },
  US: {
    code: 'US',
    name: 'Estados Unidos',
    taxIdLabel: 'EIN (Employer Identification Number)',
    taxIdPlaceholder: '12-3456789',
    taxIdPattern: '^\\d{2}-\\d{7}$',
    taxIdMask: (value: string) => {
      const numbers = value.replace(/\D/g, '');
      if (numbers.length <= 9) {
        return numbers.replace(/(\d{2})(\d)/, '$1-$2');
      }
      return value;
    },
    currency: 'USD',
    currencySymbol: '$',
    language: 'en-us',
    timezone: 'America/New_York',
    dateFormat: 'MM/DD/YYYY',
    numberFormat: '1,234.56',
    phoneFormat: '(000) 000-0000',
    addressFormat: {
      fields: ['street', 'number', 'suite', 'city', 'state', 'zipcode'],
      required: ['street', 'number', 'city', 'state', 'zipcode'],
    },
    companyTypes: ['Construction Company', 'Real Estate Developer', 'General Contractor', 'Property Management'],
  },
  MX: {
    code: 'MX',
    name: 'México',
    taxIdLabel: 'RFC (Registro Federal de Contribuyentes)',
    taxIdPlaceholder: 'ABC123456789',
    taxIdPattern: '^[A-Z]{3,4}\\d{6}[A-Z0-9]{3}$',
    currency: 'MXN',
    currencySymbol: '$',
    language: 'es-es',
    timezone: 'America/Mexico_City',
    dateFormat: 'DD/MM/YYYY',
    numberFormat: '1,234.56',
    phoneFormat: '(00) 0000-0000',
    addressFormat: {
      fields: ['street', 'number', 'colonia', 'city', 'state', 'zipcode'],
      required: ['street', 'number', 'colonia', 'city', 'state', 'zipcode'],
    },
    companyTypes: ['Constructora', 'Inmobiliaria', 'Desarrolladora', 'Constructor'],
  },
  ES: {
    code: 'ES',
    name: 'Espanha',
    taxIdLabel: 'CIF (Código de Identificación Fiscal)',
    taxIdPlaceholder: 'A12345678',
    taxIdPattern: '^[A-Z]\\d{8}$',
    currency: 'EUR',
    currencySymbol: '€',
    language: 'es-es',
    timezone: 'Europe/Madrid',
    dateFormat: 'DD/MM/YYYY',
    numberFormat: '1.234,56',
    phoneFormat: '+34 000 000 000',
    addressFormat: {
      fields: ['street', 'number', 'city', 'province', 'zipcode'],
      required: ['street', 'number', 'city', 'province', 'zipcode'],
    },
    companyTypes: ['Constructora', 'Promotora', 'Inmobiliaria', 'Constructor'],
  },
  AR: {
    code: 'AR',
    name: 'Argentina',
    taxIdLabel: 'CUIT (Clave Única de Identificación Tributaria)',
    taxIdPlaceholder: '20-12345678-9',
    taxIdPattern: '^\\d{2}-\\d{8}-\\d{1}$',
    taxIdMask: (value: string) => {
      const numbers = value.replace(/\D/g, '');
      if (numbers.length <= 11) {
        return numbers
          .replace(/(\d{2})(\d)/, '$1-$2')
          .replace(/(\d{8})(\d)/, '$1-$2');
      }
      return value;
    },
    currency: 'ARS',
    currencySymbol: '$',
    language: 'es-es',
    timezone: 'America/Argentina/Buenos_Aires',
    dateFormat: 'DD/MM/YYYY',
    numberFormat: '1.234,56',
    phoneFormat: '+54 00 0000-0000',
    addressFormat: {
      fields: ['street', 'number', 'city', 'province', 'zipcode'],
      required: ['street', 'number', 'city', 'province', 'zipcode'],
    },
    companyTypes: ['Constructora', 'Inmobiliaria', 'Desarrolladora', 'Constructor'],
  },
  CO: {
    code: 'CO',
    name: 'Colômbia',
    taxIdLabel: 'NIT (Número de Identificación Tributaria)',
    taxIdPlaceholder: '900.123.456-7',
    taxIdPattern: '^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{1}$',
    taxIdMask: (value: string) => {
      const numbers = value.replace(/\D/g, '');
      if (numbers.length <= 10) {
        return numbers
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1-$2');
      }
      return value;
    },
    currency: 'COP',
    currencySymbol: '$',
    language: 'es-es',
    timezone: 'America/Bogota',
    dateFormat: 'DD/MM/YYYY',
    numberFormat: '1.234,56',
    phoneFormat: '+57 000 000 0000',
    addressFormat: {
      fields: ['street', 'number', 'city', 'department', 'zipcode'],
      required: ['street', 'number', 'city', 'department', 'zipcode'],
    },
    companyTypes: ['Constructora', 'Inmobiliaria', 'Desarrolladora', 'Constructor'],
  },
};

export const getCountryConfig = (countryCode: string): CountryConfig | null => {
  return COUNTRIES[countryCode.toUpperCase()] || null;
};

export const getCountryList = (): CountryConfig[] => {
  return Object.values(COUNTRIES);
};


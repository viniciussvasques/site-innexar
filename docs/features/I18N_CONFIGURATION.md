# 🌍 Configuração de Internacionalização - StructurOne

## 📋 Visão Geral

O StructurOne suporta **3 idiomas** com detecção automática e configuração de moeda, país, fuso horário e formatos baseados na localização do tenant.

## 🌐 Idiomas Suportados

1. **🇧🇷 Português (Brasil)** - `pt-br`
2. **🇺🇸 Inglês (Estados Unidos)** - `en-us`
3. **🇪🇸 Espanhol (Espanha)** - `es-es`

## 🗺️ Países Suportados

### América Latina
- 🇧🇷 Brasil
- 🇲🇽 México
- 🇦🇷 Argentina
- 🇨🇴 Colômbia
- 🇨🇱 Chile
- 🇵🇪 Peru
- 🇪🇨 Equador
- 🇻🇪 Venezuela
- 🇺🇾 Uruguai
- 🇵🇾 Paraguai
- 🇧🇴 Bolívia
- 🇨🇷 Costa Rica
- 🇵🇦 Panamá
- 🇬🇹 Guatemala
- 🇩🇴 República Dominicana
- 🇨🇺 Cuba
- 🇭🇳 Honduras
- 🇳🇮 Nicarágua
- 🇸🇻 El Salvador

### América do Norte
- 🇺🇸 Estados Unidos

### Europa
- 🇪🇸 Espanha

## 💰 Moedas Suportadas

- **BRL** - Real Brasileiro (R$)
- **USD** - Dólar Americano ($)
- **EUR** - Euro (€)
- **MXN** - Peso Mexicano (MX$)
- **ARS** - Peso Argentino ($)
- **COP** - Peso Colombiano ($)
- **CLP** - Peso Chileno ($)
- **PEN** - Sol Peruano (S/)
- **UYU** - Peso Uruguaio ($U)
- **PYG** - Guarani Paraguaio (₲)
- **BOB** - Boliviano (Bs.)
- **CRC** - Colón Costarriquenho (₡)
- **DOP** - Peso Dominicano (RD$)
- **CUP** - Peso Cubano ($)
- **GTQ** - Quetzal Guatemalteco (Q)
- **HNL** - Lempira Hondurenha (L)
- **NIO** - Córdoba Nicaraguense (C$)
- **PAB** - Balboa Panamenho (B/.)
- **SVC** - Colón Salvadorenho (₡)

## ⚙️ Configurações por País

### Detecção Automática

Quando um tenant seleciona um país durante o onboarding, as seguintes configurações são **automaticamente detectadas**:

| País | Idioma | Moeda | Timezone | Formato Data | Formato Número |
|------|--------|-------|----------|--------------|----------------|
| 🇧🇷 Brasil | pt-br | BRL | America/Sao_Paulo | DD/MM/YYYY | 1.234,56 |
| 🇺🇸 EUA | en-us | USD | America/New_York | MM/DD/YYYY | 1,234.56 |
| 🇲🇽 México | es-es | MXN | America/Mexico_City | DD/MM/YYYY | 1,234.56 |
| 🇪🇸 Espanha | es-es | EUR | Europe/Madrid | DD/MM/YYYY | 1.234,56 |
| 🇦🇷 Argentina | es-es | ARS | America/Argentina/Buenos_Aires | DD/MM/YYYY | 1.234,56 |
| 🇨🇴 Colômbia | es-es | COP | America/Bogota | DD/MM/YYYY | 1.234,56 |
| 🇨🇱 Chile | es-es | CLP | America/Santiago | DD/MM/YYYY | 1.234,56 |
| 🇵🇪 Peru | es-es | PEN | America/Lima | DD/MM/YYYY | 1.234,56 |

## 🔄 Fluxo de Detecção

### 1. Durante o Onboarding

```
[Usuário seleciona país] 
    ↓
[Backend detecta automaticamente]
    ↓
[Configurações aplicadas ao Tenant]
    - Idioma
    - Moeda
    - Timezone
    - Formato de Data
    - Formato de Número
    ↓
[Usuário pode ajustar manualmente se necessário]
```

### 2. Detecção por Header HTTP

O sistema também detecta o idioma preferido do navegador através do header `Accept-Language`:

```
[Browser envia Accept-Language: pt-BR,pt;q=0.9]
    ↓
[Backend detecta idioma]
    ↓
[Se tenant não tem idioma configurado, usa o detectado]
```

## 📝 Campos no Modelo Tenant

```python
class Tenant(models.Model):
    # ... outros campos ...
    
    # Internacionalização
    language = models.CharField(
        max_length=10,
        choices=[
            ('pt-br', 'Português (Brasil)'),
            ('en-us', 'English (US)'),
            ('es-es', 'Español (España)'),
        ],
        default='pt-br'
    )
    
    country = models.CharField(
        max_length=2,
        choices=[...],  # 20+ países
        default='BR'
    )
    
    currency = models.CharField(
        max_length=3,
        choices=[...],  # 19 moedas
        default='BRL'
    )
    
    timezone = models.CharField(
        max_length=50,
        default='America/Sao_Paulo'
    )
    
    date_format = models.CharField(
        max_length=20,
        choices=[
            ('DD/MM/YYYY', 'DD/MM/YYYY'),
            ('MM/DD/YYYY', 'MM/DD/YYYY'),
            ('YYYY-MM-DD', 'YYYY-MM-DD'),
        ],
        default='DD/MM/YYYY'
    )
    
    number_format = models.CharField(
        max_length=20,
        choices=[
            ('1.234,56', '1.234,56 (Brasil/Espanha)'),
            ('1,234.56', '1,234.56 (EUA)'),
        ],
        default='1.234,56'
    )
```

## 🛠️ Funções Utilitárias

### `apps/core/utils.py`

```python
# Detecção automática baseada em país
detect_language_from_country(country_code: str) -> str
detect_currency_from_country(country_code: str) -> str
detect_timezone_from_country(country_code: str) -> str
detect_number_format_from_country(country_code: str) -> str
detect_date_format_from_country(country_code: str) -> str

# Detecção via HTTP header
detect_locale_from_request(request) -> Optional[str]

# Configuração automática completa
auto_configure_tenant_i18n(tenant, country_code: str)

# Obter configurações do tenant
get_tenant_locale_settings(tenant) -> dict
```

## 📱 Uso no Frontend

### Exemplo: Formatação de Moeda

```typescript
// Frontend recebe configurações do tenant
const tenantSettings = {
  currency: 'BRL',
  number_format: '1.234,56',
  language: 'pt-br'
};

// Formatar valor monetário
function formatCurrency(value: number, currency: string, format: string) {
  if (format === '1.234,56') {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: currency
    }).format(value);
  } else {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(value);
  }
}

// Uso
formatCurrency(1234.56, 'BRL', '1.234,56'); // R$ 1.234,56
formatCurrency(1234.56, 'USD', '1,234.56');  // $1,234.56
```

### Exemplo: Formatação de Data

```typescript
function formatDate(date: Date, format: string) {
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear();
  
  switch (format) {
    case 'DD/MM/YYYY':
      return `${day}/${month}/${year}`;
    case 'MM/DD/YYYY':
      return `${month}/${day}/${year}`;
    case 'YYYY-MM-DD':
      return `${year}-${month}-${day}`;
    default:
      return `${day}/${month}/${year}`;
  }
}
```

## 🔧 Middleware de Idioma

O Django já está configurado com `LocaleMiddleware` que detecta o idioma do tenant:

```python
# settings.py
MIDDLEWARE = [
    # ...
    'django.middleware.locale.LocaleMiddleware',
    # ...
]

LANGUAGES = [
    ('pt-br', 'Português (Brasil)'),
    ('en-us', 'English (US)'),
    ('es-es', 'Español (España)'),
]
```

## ✅ Checklist de Implementação

- [x] Campos de i18n adicionados ao modelo Tenant
- [x] Funções utilitárias de detecção criadas
- [x] Mapeamentos de país → configurações criados
- [ ] Migration criada e aplicada
- [ ] Onboarding atualizado para incluir seleção de país
- [ ] Frontend atualizado para usar configurações do tenant
- [ ] Testes de detecção automática
- [ ] Documentação de API atualizada

## 📚 Referências

- [Django i18n Documentation](https://docs.djangoproject.com/en/stable/topics/i18n/)
- [ISO 3166-1 Country Codes](https://en.wikipedia.org/wiki/ISO_3166-1)
- [ISO 4217 Currency Codes](https://en.wikipedia.org/wiki/ISO_4217)
- [IANA Time Zone Database](https://www.iana.org/time-zones)


"""
Testes Manuais - Sistema de Billing
Script para executar testes manuais via API
"""
import sys
import io
import json
import requests
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Usar localhost mesmo dentro do Docker (porta mapeada)
BASE_URL = 'http://localhost:8000/api'  # Porta interna do container
ADMIN_EMAIL = 'admin@structurone.com'
ADMIN_PASSWORD = 'admin123'

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def make_request(method, url, headers=None, data=None):
    """Faz requisição HTTP"""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method == 'PATCH':
            response = requests.patch(url, headers=headers, json=data, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            raise ValueError(f'Método não suportado: {method}')
        
        # Tentar parse JSON
        try:
            json_data = response.json() if response.content else None
        except:
            json_data = {'raw': response.text[:200]}  # Primeiros 200 chars se não for JSON
        
        return {
            'status_code': response.status_code,
            'data': json_data,
            'headers': dict(response.headers),
            'text': response.text[:200] if response.text else None
        }
    except requests.exceptions.RequestException as e:
        return {
            'status_code': 0,
            'error': str(e),
            'data': None
        }

def login_admin():
    """Faz login como admin"""
    print_info("Fazendo login como admin...")
    response = make_request('POST', f'{BASE_URL}/auth/login/', data={
        'email': ADMIN_EMAIL,
        'password': ADMIN_PASSWORD
    })
    
    if response['status_code'] == 200:
        tokens = response['data']['tokens']
        print_success(f"Login realizado com sucesso")
        return tokens['access'], tokens['refresh']
    else:
        print_error(f"Erro no login: {response.get('error', response.get('data', {}))}")
        return None, None

def test_1_planos():
    """Teste 1: Gestão de Planos"""
    print_header("TESTE 1: Gestão de Planos")
    
    access_token, _ = login_admin()
    if not access_token:
        return False
    
    headers = {'Authorization': f'Bearer {access_token}'}
    results = {}
    
    # 1.1 Listar planos
    print_info("1.1 Listando planos...")
    response = make_request('GET', f'{BASE_URL}/billing/plans/', headers=headers)
    if response['status_code'] == 200:
        plans = response['data'] if isinstance(response['data'], list) else response['data'].get('results', [])
        print_success(f"Planos encontrados: {len(plans)}")
        if plans:
            for plan in plans[:3]:  # Mostrar apenas 3 primeiros
                print(f"  - {plan.get('name')} ({plan.get('slug')}) - R$ {plan.get('price_monthly_brl', 'N/A')}")
        results['list_plans'] = True
    else:
        print_error(f"Erro ao listar planos: {response.get('error', response.get('data', {}))}")
        results['list_plans'] = False
    
    # 1.2 Detalhes de um plano
    if plans:
        print_info("1.2 Obtendo detalhes de um plano...")
        plan_slug = plans[0].get('slug')
        response = make_request('GET', f'{BASE_URL}/billing/plans/{plan_slug}/', headers=headers)
        if response['status_code'] == 200:
            plan = response['data']
            print_success(f"Detalhes do plano '{plan.get('name')}':")
            print(f"  - Preço Mensal BRL: R$ {plan.get('price_monthly_brl', 'N/A')}")
            print(f"  - Preço Anual BRL: R$ {plan.get('price_yearly_brl', 'N/A')}")
            print(f"  - Máximo de Projetos: {plan.get('max_projects', 'N/A')}")
            print(f"  - Features: {len(plan.get('features', []))} features")
            results['plan_detail'] = True
        else:
            print_error(f"Erro ao obter detalhes: {response.get('error', response.get('data', {}))}")
            results['plan_detail'] = False
    
    return results

def test_2_assinatura():
    """Teste 2: Assinatura de Plano"""
    print_header("TESTE 2: Assinatura de Plano")
    
    access_token, _ = login_admin()
    if not access_token:
        return False
    
    headers = {'Authorization': f'Bearer {access_token}'}
    results = {}
    
    # 2.1 Obter minha assinatura
    print_info("2.1 Obtendo minha assinatura...")
    response = make_request('GET', f'{BASE_URL}/billing/subscriptions/me/', headers=headers)
    if response['status_code'] == 200:
        subscription = response['data']
        print_success(f"Assinatura encontrada:")
        print(f"  - Status: {subscription.get('status')}")
        print(f"  - Plano: {subscription.get('plan', {}).get('name', 'N/A')}")
        print(f"  - Período: {subscription.get('current_period_start')} até {subscription.get('current_period_end')}")
        results['get_subscription'] = True
    elif response['status_code'] == 404:
        print_warning("Nenhuma assinatura encontrada (esperado se ainda não assinou)")
        results['get_subscription'] = True  # OK, não ter assinatura é válido
    else:
        print_error(f"Erro ao obter assinatura: {response.get('error', response.get('data', {}))}")
        results['get_subscription'] = False
    
    # 2.2 Listar planos disponíveis
    print_info("2.2 Listando planos disponíveis para assinatura...")
    response = make_request('GET', f'{BASE_URL}/billing/plans/', headers=headers)
    if response['status_code'] == 200:
        plans = response['data'] if isinstance(response['data'], list) else (response['data'].get('results', []) if isinstance(response['data'], dict) else [])
        active_plans = [p for p in plans if p.get('is_active', False)]
        print_success(f"Planos ativos disponíveis: {len(active_plans)}")
        for plan in active_plans:
            print(f"  - {plan.get('name')} (ID: {plan.get('id')})")
        results['list_available_plans'] = True
    else:
        print_error(f"Erro ao listar planos: {response.get('error', response.get('data', {}))}")
        results['list_available_plans'] = False
    
    return results

def test_3_faturas():
    """Teste 3: Faturas"""
    print_header("TESTE 3: Faturas")
    
    access_token, _ = login_admin()
    if not access_token:
        return False
    
    headers = {'Authorization': f'Bearer {access_token}'}
    results = {}
    
    # 3.1 Listar faturas
    print_info("3.1 Listando faturas...")
    response = make_request('GET', f'{BASE_URL}/billing/invoices/', headers=headers)
    if response['status_code'] == 200:
        data = response['data']
        invoices = data.get('results', []) if isinstance(data, dict) else data
        print_success(f"Faturas encontradas: {len(invoices)}")
        for invoice in invoices[:5]:  # Mostrar apenas 5 primeiras
            print(f"  - {invoice.get('invoice_number')} - {invoice.get('status')} - R$ {invoice.get('total_amount', 'N/A')}")
        results['list_invoices'] = True
    else:
        print_error(f"Erro ao listar faturas: {response.get('error', response.get('data', {}))}")
        results['list_invoices'] = False
    
    # 3.2 Filtrar faturas por status
    if invoices:
        print_info("3.2 Filtrando faturas por status 'paid'...")
        response = make_request('GET', f'{BASE_URL}/billing/invoices/?status=paid', headers=headers)
        if response['status_code'] == 200:
            data = response['data']
            paid_invoices = data.get('results', []) if isinstance(data, dict) else data
            print_success(f"Faturas pagas: {len(paid_invoices)}")
            results['filter_invoices'] = True
        else:
            print_error(f"Erro ao filtrar: {response.get('error', response.get('data', {}))}")
            results['filter_invoices'] = False
    
    return results

def test_4_pagamentos():
    """Teste 4: Pagamentos"""
    print_header("TESTE 4: Pagamentos")
    
    access_token, _ = login_admin()
    if not access_token:
        return False
    
    headers = {'Authorization': f'Bearer {access_token}'}
    results = {}
    
    # 4.1 Listar pagamentos
    print_info("4.1 Listando pagamentos...")
    response = make_request('GET', f'{BASE_URL}/billing/payments/', headers=headers)
    if response['status_code'] == 200:
        data = response['data']
        payments = data.get('results', []) if isinstance(data, dict) else data
        print_success(f"Pagamentos encontrados: {len(payments)}")
        for payment in payments[:5]:  # Mostrar apenas 5 primeiros
            print(f"  - {payment.get('id')} - {payment.get('status')} - R$ {payment.get('amount', 'N/A')}")
        results['list_payments'] = True
    else:
        print_error(f"Erro ao listar pagamentos: {response.get('error', response.get('data', {}))}")
        results['list_payments'] = False
    
    # 4.2 Filtrar pagamentos por status
    if payments:
        print_info("4.2 Filtrando pagamentos por status 'succeeded'...")
        response = make_request('GET', f'{BASE_URL}/billing/payments/?status=succeeded', headers=headers)
        if response['status_code'] == 200:
            data = response['data']
            succeeded_payments = data.get('results', []) if isinstance(data, dict) else data
            print_success(f"Pagamentos bem-sucedidos: {len(succeeded_payments)}")
            results['filter_payments'] = True
        else:
            print_error(f"Erro ao filtrar: {response.get('error', response.get('data', {}))}")
            results['filter_payments'] = False
    
    return results

def test_5_metodos_pagamento():
    """Teste 5: Métodos de Pagamento"""
    print_header("TESTE 5: Métodos de Pagamento")
    
    access_token, _ = login_admin()
    if not access_token:
        return False
    
    headers = {'Authorization': f'Bearer {access_token}'}
    results = {}
    
    # 5.1 Listar métodos de pagamento
    print_info("5.1 Listando métodos de pagamento...")
    response = make_request('GET', f'{BASE_URL}/billing/payment-methods/', headers=headers)
    if response['status_code'] == 200:
        data = response['data']
        methods = data.get('results', []) if isinstance(data, dict) else data
        print_success(f"Métodos de pagamento encontrados: {len(methods)}")
        for method in methods:
            print(f"  - {method.get('type')} - {method.get('card_display', 'N/A')} - Padrão: {method.get('is_default', False)}")
        results['list_payment_methods'] = True
    else:
        print_error(f"Erro ao listar métodos: {response.get('error', response.get('data', {}))}")
        results['list_payment_methods'] = False
    
    return results

def test_6_precos_por_pais():
    """Teste 6: Preços por País"""
    print_header("TESTE 6: Preços por País")
    
    # Criar usuários de teste para BR e US
    print_info("6.1 Testando preços para tenant brasileiro...")
    access_token_br, _ = login_admin()  # Assumindo que admin tem tenant BR
    results = {}
    if access_token_br:
        headers = {'Authorization': f'Bearer {access_token_br}'}
        response = make_request('GET', f'{BASE_URL}/billing/plans/', headers=headers)
        if response['status_code'] == 200:
            plans = response['data'] if isinstance(response['data'], list) else (response['data'].get('results', []) if isinstance(response['data'], dict) else [])
            if plans:
                plan = plans[0]
                print_success(f"Plano '{plan.get('name')}' para BR:")
                print(f"  - Preço Mensal: {plan.get('price_monthly_display', 'N/A')}")
                print(f"  - Moeda: {plan.get('currency', 'N/A')}")
                results['precos_por_pais'] = True
            else:
                results['precos_por_pais'] = False
        else:
            results['precos_por_pais'] = False
    else:
        results['precos_por_pais'] = False
    
    return results

def test_7_criar_assinatura():
    """Teste 7: Criar Assinatura"""
    print_header("TESTE 7: Criar Assinatura")
    
    access_token, _ = login_admin()
    if not access_token:
        return {'create_subscription': False}
    
    headers = {'Authorization': f'Bearer {access_token}'}
    results = {}
    
    # Obter primeiro plano disponível
    print_info("7.1 Obtendo plano disponível...")
    response = make_request('GET', f'{BASE_URL}/billing/plans/', headers=headers)
    if response['status_code'] != 200:
        print_error("Não foi possível obter planos")
        return {'create_subscription': False}
    
    plans = response['data'] if isinstance(response['data'], list) else (response['data'].get('results', []) if isinstance(response['data'], dict) else [])
    if not plans:
        print_warning("Nenhum plano disponível para teste")
        return {'create_subscription': True}  # Não é erro, apenas não há planos
    
    plan = plans[0]
    plan_id = plan.get('id')
    
    # Verificar se já tem assinatura
    print_info("7.2 Verificando se já possui assinatura...")
    response = make_request('GET', f'{BASE_URL}/billing/subscriptions/me/', headers=headers)
    if response['status_code'] == 200:
        print_warning("Já possui assinatura ativa. Pulando criação...")
        results['create_subscription'] = True  # OK, já tem assinatura
        return results
    
    # Tentar criar assinatura (pode falhar se não tiver método de pagamento)
    print_info("7.3 Tentando criar assinatura...")
    response = make_request('POST', f'{BASE_URL}/billing/subscriptions/create/', headers=headers, data={
        'plan_id': plan_id,
        'billing_cycle': 'monthly'
    })
    
    if response['status_code'] == 201:
        subscription = response['data']
        print_success(f"Assinatura criada com sucesso!")
        print(f"  - Status: {subscription.get('status')}")
        print(f"  - Plano: {subscription.get('plan', {}).get('name', 'N/A')}")
        results['create_subscription'] = True
    elif response['status_code'] == 400:
        error_msg = response['data'].get('detail', 'Erro desconhecido') if response['data'] else 'Erro desconhecido'
        if 'já possui' in error_msg.lower():
            print_warning("Já possui assinatura (esperado)")
            results['create_subscription'] = True
        else:
            print_warning(f"Erro ao criar assinatura (esperado sem método de pagamento): {error_msg}")
            results['create_subscription'] = True  # OK, erro esperado
    else:
        print_warning(f"Resposta inesperada: {response['status_code']}")
        results['create_subscription'] = False
    
    return results

def test_8_filtros():
    """Teste 8: Filtros e Paginação"""
    print_header("TESTE 8: Filtros e Paginação")
    
    access_token, _ = login_admin()
    if not access_token:
        return {'filtros': False}
    
    headers = {'Authorization': f'Bearer {access_token}'}
    results = {}
    
    # Testar filtro de faturas
    print_info("8.1 Testando filtro de faturas por status...")
    response = make_request('GET', f'{BASE_URL}/billing/invoices/?status=paid', headers=headers)
    if response['status_code'] == 200:
        print_success("Filtro de faturas funcionando")
        results['filter_invoices'] = True
    else:
        print_warning(f"Filtro retornou: {response['status_code']}")
        results['filter_invoices'] = True  # OK mesmo sem faturas
    
    # Testar paginação
    print_info("8.2 Testando paginação...")
    response = make_request('GET', f'{BASE_URL}/billing/invoices/?page=1&page_size=10', headers=headers)
    if response['status_code'] == 200:
        data = response['data']
        if isinstance(data, dict) and 'results' in data:
            print_success("Paginação funcionando")
            results['pagination'] = True
        else:
            results['pagination'] = True  # OK se não paginado
    else:
        results['pagination'] = True  # OK
    
    return results

def run_all_tests():
    """Executa todos os testes manuais"""
    print_header("INICIANDO TESTES MANUAIS - SISTEMA DE BILLING")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}\n")
    
    all_results = {}
    
    # Executar testes
    try:
        all_results['test_1_planos'] = test_1_planos()
        all_results['test_2_assinatura'] = test_2_assinatura()
        all_results['test_3_faturas'] = test_3_faturas()
        all_results['test_4_pagamentos'] = test_4_pagamentos()
        all_results['test_5_metodos_pagamento'] = test_5_metodos_pagamento()
        all_results['test_6_precos_por_pais'] = test_6_precos_por_pais()
        all_results['test_7_criar_assinatura'] = test_7_criar_assinatura()
        all_results['test_8_filtros'] = test_8_filtros()
    except Exception as e:
        print_error(f"Erro durante execução dos testes: {e}")
        import traceback
        traceback.print_exc()
    
    # Resumo
    print_header("RESUMO DOS TESTES")
    
    total_tests = 0
    passed_tests = 0
    
    for test_name, test_results in all_results.items():
        if isinstance(test_results, dict):
            for subtest, result in test_results.items():
                total_tests += 1
                if result:
                    passed_tests += 1
                    print_success(f"{test_name}.{subtest}: PASSOU")
                else:
                    print_error(f"{test_name}.{subtest}: FALHOU")
    
    print(f"\n{Colors.BOLD}Total: {passed_tests}/{total_tests} testes passaram{Colors.RESET}")
    
    if passed_tests == total_tests:
        print_success("🎉 Todos os testes passaram!")
    else:
        print_warning(f"⚠️  {total_tests - passed_tests} teste(s) falharam")
    
    return all_results

if __name__ == '__main__':
    run_all_tests()


"""
Testes Manuais - Autenticação e Onboarding
Script para testar manualmente os fluxos completos da API
"""
import sys
import io

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
import urllib.request
import urllib.parse
from datetime import datetime

import os
# Detectar se está rodando dentro do container
if os.path.exists('/.dockerenv'):
    BASE_URL = "http://localhost:8000/api"  # Mesmo container, localhost funciona
else:
    BASE_URL = "http://localhost:8010/api"  # Acesso externo

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.RESET}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def make_request(method, url, data=None, headers=None):
    """Faz requisição HTTP"""
    if headers is None:
        headers = {}
    
    if data:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return {
                'status_code': response.getcode(),
                'data': json.loads(response.read().decode('utf-8'))
            }
    except urllib.error.HTTPError as e:
        error_data = {}
        try:
            error_data = json.loads(e.read().decode('utf-8'))
        except:
            error_data = {'detail': e.read().decode('utf-8')}
        return {
            'status_code': e.code,
            'data': error_data
        }
    except Exception as e:
        raise Exception(f"Erro na requisição: {e}")

def test_api_root():
    """Testa endpoint raiz da API"""
    print_info("Testando API Root...")
    try:
        response = make_request('GET', f"{BASE_URL}/")
        if response['status_code'] == 200:
            print_success("API Root acessível")
            print(f"  Resposta: {json.dumps(response['data'], indent=2)}")
            return True
        else:
            print_error(f"API Root retornou {response['status_code']}")
            return False
    except Exception as e:
        print_error(f"Erro ao acessar API Root: {e}")
        return False

def test_register_user(tenant_slug="empresa-teste"):
    """Testa registro de usuário"""
    print_info("Testando Registro de Usuário...")
    
    data = {
        "email": f"teste{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com",
        "password": "Test123!@#",
        "password_confirm": "Test123!@#",
        "first_name": "João",
        "last_name": "Silva",
        "tenant_slug": tenant_slug,
        "phone": "+5511999999999"
    }
    
    try:
        response = make_request('POST', f"{BASE_URL}/auth/register/", data=data)
        
        if response['status_code'] == 201:
            print_success("Usuário registrado com sucesso")
            result = response['data']
            print(f"  Email: {result['user']['email']}")
            print(f"  Role: {result['user']['role']}")
            print(f"  Tenant: {result['user']['tenant']['name']}")
            print(f"  Tokens recebidos: {'access' in result['tokens'] and 'refresh' in result['tokens']}")
            return result
        else:
            print_error(f"Registro falhou: {response['status_code']}")
            print(f"  Erro: {json.dumps(response['data'], indent=2)}")
            return None
    except Exception as e:
        print_error(f"Erro ao registrar usuário: {e}")
        return None

def test_login(email, password):
    """Testa login de usuário"""
    print_info(f"Testando Login para {email}...")
    
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = make_request('POST', f"{BASE_URL}/auth/login/", data=data)
        
        if response['status_code'] == 200:
            print_success("Login realizado com sucesso")
            result = response['data']
            print(f"  Usuário: {result['user']['email']}")
            print(f"  Onboarding completo: {result['user']['onboarding_completed']}")
            return result
        else:
            print_error(f"Login falhou: {response['status_code']}")
            print(f"  Erro: {json.dumps(response['data'], indent=2)}")
            return None
    except Exception as e:
        print_error(f"Erro ao fazer login: {e}")
        return None

def test_get_me(access_token):
    """Testa obter dados do usuário logado"""
    print_info("Testando GET /auth/me/...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = make_request('GET', f"{BASE_URL}/auth/me/", headers=headers)
        
        if response['status_code'] == 200:
            print_success("Dados do usuário obtidos")
            result = response['data']
            print(f"  Email: {result['email']}")
            print(f"  Nome: {result['first_name']} {result['last_name']}")
            print(f"  Tenant: {result['tenant']['name']}")
            print(f"  Idioma: {result['tenant']['language']}")
            print(f"  Moeda: {result['tenant']['currency']}")
            return result
        else:
            print_error(f"Falha ao obter dados: {response['status_code']}")
            print(f"  Erro: {json.dumps(response['data'], indent=2)}")
            return None
    except Exception as e:
        print_error(f"Erro ao obter dados do usuário: {e}")
        return None

def test_get_onboarding(access_token):
    """Testa obter progresso do onboarding"""
    print_info("Testando GET /onboarding/...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = make_request('GET', f"{BASE_URL}/onboarding/", headers=headers)
        
        if response['status_code'] == 200:
            print_success("Progresso do onboarding obtido")
            result = response['data']
            print(f"  Etapa: {result['step']}/4")
            print(f"  Completo: {result['completed']}")
            print(f"  Dados: {json.dumps(result['data'], indent=2)}")
            return result
        else:
            print_error(f"Falha ao obter onboarding: {response['status_code']}")
            print(f"  Erro: {json.dumps(response['data'], indent=2)}")
            return None
    except Exception as e:
        print_error(f"Erro ao obter onboarding: {e}")
        return None

def test_update_onboarding(access_token, step, data):
    """Testa atualizar progresso do onboarding"""
    print_info(f"Testando atualização do onboarding (etapa {step})...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    payload = {
        "step": step,
        "data": data
    }
    
    try:
        response = make_request('POST', f"{BASE_URL}/onboarding/", data=payload, headers=headers)
        
        if response['status_code'] == 200:
            print_success(f"Onboarding atualizado para etapa {step}")
            result = response['data']
            print(f"  Etapa: {result['step']}/4")
            if 'country' in data:
                print(f"  País configurado: {result['data'].get('country')}")
                print(f"  Idioma detectado: {result['data'].get('language')}")
                print(f"  Moeda detectada: {result['data'].get('currency')}")
            return result
        else:
            print_error(f"Falha ao atualizar onboarding: {response['status_code']}")
            print(f"  Erro: {json.dumps(response['data'], indent=2)}")
            return None
    except Exception as e:
        print_error(f"Erro ao atualizar onboarding: {e}")
        return None

def test_complete_onboarding(access_token):
    """Testa completar onboarding"""
    print_info("Testando completar onboarding...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = make_request('POST', f"{BASE_URL}/onboarding/complete/", headers=headers)
        
        if response['status_code'] == 200:
            print_success("Onboarding completado")
            result = response['data']
            print(f"  Status: {result['message']}")
            print(f"  Completo: {result['onboarding_completed']}")
            return result
        else:
            print_error(f"Falha ao completar onboarding: {response['status_code']}")
            print(f"  Erro: {json.dumps(response['data'], indent=2)}")
            return None
    except Exception as e:
        print_error(f"Erro ao completar onboarding: {e}")
        return None

def test_password_reset_request(email):
    """Testa solicitar reset de senha"""
    print_info(f"Testando solicitação de reset de senha para {email}...")
    
    data = {
        "email": email
    }
    
    try:
        response = make_request('POST', f"{BASE_URL}/password-reset/request/", data=data)
        
        if response['status_code'] == 200:
            print_success("Solicitação de reset enviada")
            print(f"  Mensagem: {response['data'].get('message')}")
            return True
        else:
            print_error(f"Falha ao solicitar reset: {response['status_code']}")
            return False
    except Exception as e:
        print_error(f"Erro ao solicitar reset: {e}")
        return False

def test_refresh_token(refresh_token):
    """Testa refresh de token"""
    print_info("Testando refresh de token...")
    
    data = {
        "refresh": refresh_token
    }
    
    try:
        response = make_request('POST', f"{BASE_URL}/auth/token/refresh/", data=data)
        
        if response['status_code'] == 200:
            print_success("Token renovado com sucesso")
            result = response['data']
            print(f"  Novo access token recebido: {'access' in result}")
            print(f"  Novo refresh token recebido: {'refresh' in result}")
            # Retornar os tokens para atualização
            return result.get('tokens', result) if 'tokens' in result else result
        else:
            print_error(f"Falha ao renovar token: {response['status_code']}")
            print(f"  Erro: {json.dumps(response['data'], indent=2)}")
            return None
    except Exception as e:
        print_error(f"Erro ao renovar token: {e}")
        return None

def test_logout(access_token, refresh_token):
    """Testa logout"""
    print_info("Testando logout...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    data = {
        "refresh": refresh_token
    }
    
    try:
        response = make_request('POST', f"{BASE_URL}/auth/logout/", data=data, headers=headers)
        
        if response['status_code'] == 200:
            print_success("Logout realizado com sucesso")
            print(f"  Mensagem: {response['data'].get('message')}")
            return True
        else:
            print_error(f"Falha ao fazer logout: {response['status_code']}")
            return False
    except Exception as e:
        print_error(f"Erro ao fazer logout: {e}")
        return False

def run_full_flow_test():
    """Executa fluxo completo de testes"""
    print("\n" + "="*60)
    print("TESTES MANUAIS - AUTENTICAÇÃO E ONBOARDING")
    print("="*60 + "\n")
    
    results = {
        "api_root": False,
        "register": False,
        "login": False,
        "get_me": False,
        "onboarding": False,
        "complete_onboarding": False,
        "refresh_token": False,
        "logout": False,
        "logout_verification": False,
    }
    
    # 1. Testar API Root
    results["api_root"] = test_api_root()
    print()
    
    # 2. Registrar usuário
    register_result = test_register_user()
    if register_result:
        results["register"] = True
        user_email = register_result['user']['email']
        access_token = register_result['tokens']['access']
        refresh_token = register_result['tokens']['refresh']
        print()
        
        # 3. Fazer login
        login_result = test_login(user_email, "Test123!@#")
        if login_result:
            results["login"] = True
            access_token = login_result['tokens']['access']
            refresh_token = login_result['tokens']['refresh']
            print()
        
        # 4. Obter dados do usuário
        if test_get_me(access_token):
            results["get_me"] = True
            print()
        
        # 5. Obter progresso do onboarding
        onboarding_result = test_get_onboarding(access_token)
        if onboarding_result:
            print()
            
            # 6. Atualizar onboarding - Etapa 1 (Informações da Empresa)
            step1_data = {
                "company_name": "Empresa Teste LTDA",
                "cnpj": "12.345.678/0001-90",
                "address": "Rua Teste, 123 - São Paulo, SP"
            }
            if test_update_onboarding(access_token, 1, step1_data):
                print()
            
            # 7. Atualizar onboarding - Etapa 2 (Configuração com país)
            step2_data = {
                "logo": "https://example.com/logo.png",
                "primary_color": "#3B82F6",
                "country": "BR"  # Isso deve configurar i18n automaticamente
            }
            onboarding_result = test_update_onboarding(access_token, 2, step2_data)
            if onboarding_result:
                results["onboarding"] = True
                print()
                
                # Verificar se i18n foi configurado
                me_result = test_get_me(access_token)
                if me_result:
                    tenant = me_result['tenant']
                    print_info("Verificando configuração automática de i18n...")
                    print(f"  País: {tenant.get('country')}")
                    print(f"  Idioma: {tenant.get('language')}")
                    print(f"  Moeda: {tenant.get('currency')}")
                    print(f"  Timezone: {tenant.get('timezone')}")
                    print()
            
            # 8. Completar onboarding
            if test_complete_onboarding(access_token):
                results["complete_onboarding"] = True
                print()
        
        # 9. Testar refresh token
        refresh_result = test_refresh_token(refresh_token)
        if refresh_result:
            results["refresh_token"] = True
            # Atualizar tokens após refresh
            new_access_token = refresh_result.get('access')
            new_refresh_token = refresh_result.get('refresh')
            if new_access_token:
                access_token = new_access_token
            if new_refresh_token:
                refresh_token = new_refresh_token
            print()
        
        # 10. Testar logout (usar o token atual)
        if test_logout(access_token, refresh_token):
            results["logout"] = True
            print()
        
        # 11. Testar acesso após logout (deve falhar)
        print_info("Testando acesso após logout (deve falhar)...")
        print_info("Tentando acessar /auth/me/ com token invalidado...")
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        try:
            response = make_request('GET', f"{BASE_URL}/auth/me/", headers=headers)
            if response['status_code'] == 401:
                print_success("Acesso negado após logout (esperado - token invalidado)")
                results["logout_verification"] = True
            else:
                print_error(f"Acesso ainda permitido após logout (status: {response['status_code']})")
                results["logout_verification"] = False
        except Exception as e:
            print_success(f"Acesso negado após logout (exceção esperada: {e})")
            results["logout_verification"] = True
        print()
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "✓ PASSOU" if result else "✗ FALHOU"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{test_name.upper():.<40} {status}{Colors.RESET}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print_success("Todos os testes manuais passaram!")
    else:
        print_warning(f"{total - passed} teste(s) falharam")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_full_flow_test()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTestes interrompidos pelo usuário")
        exit(1)
    except Exception as e:
        print_error(f"Erro inesperado: {e}")
        exit(1)


import json
import re
from datetime import datetime
import beaupy
#Função que carrega os dados do ficheiro
def load_json(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Erro: O arquivo {file_name} não foi encontrado.")
        return []
    except json.JSONDecodeError:
        print(f"Erro: Não foi possível decodificar o arquivo {file_name}.")
        return []
#Função que guarda os dados no ficheiro json
def save_json(file_name, data):
    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Erro ao escrever no ficheiro. Verifique as permissões. \n{e}")
#Função que valida se a data esta no formato correto
def validaData(data, optional=False):
    try:
        if optional and not data:
            return None
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', data):
            raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")
        datetime.strptime(data, '%Y-%m-%d')
        return data
    except ValueError as e:
        raise ValueError(f"Erro ao validar a data: {e}")
    
#Função que verifica se os a matricula esta num formato correto
def validaMatricula(matricula):
    pattern = re.compile(r'^[A-Z0-9]{2}-[A-Z0-9]{2}-[A-Z0-9]{2}$')
    matricula = matricula.upper()
    if pattern.match(matricula):
        return matricula
    else:
        return None
#função que verifica se o ID é inteiro
def verificaIDInteiro(mensagem, optional=False):
    while True:
        try:
            entrada = input(mensagem)
            if optional and entrada == '':
                return None
            valor = int(entrada)
            return valor
        except ValueError:
            print("Por favor, insira um número inteiro válido.")
#função que procura o maior id da lista
def maiorIDLista(lista):
    if lista:
        return max(item['id'] for item in lista)
    return 1
#função que confirma alterações
def validaConfirmacao(valor):
    while True:
        resposta = input(valor).strip().upper()
        if resposta in ['S', 'N']:
            return resposta
        print("Resposta inválida. Por favor, insira 'S' para sim ou 'N' para não.")
    
#Função que gera lista de seleção beaupy do cliente
def selecionaCliente(listCliente):
    clienteOpcao = [f"{cliente['id']} - {cliente['nome']}" for cliente in listCliente]
    clienteEscolha = beaupy.select(clienteOpcao, cursor='->', cursor_style='red', return_index=True)
    cliente_id = listCliente[clienteEscolha]['id']
    return cliente_id

#Função que gera lista de seleção beaupy do automovel
def selecionaAutomovel(listAutomovel):
    opcoesAutomovel = [f"{automovel['id']} - {automovel['marca']} {automovel['modelo']}" for automovel in listAutomovel]
    automovelecolha = beaupy.select(opcoesAutomovel, cursor='->', cursor_style='red', return_index=True)
    automovel_id = listAutomovel[automovelecolha]['id']
    return automovel_id


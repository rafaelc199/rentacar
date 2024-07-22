#importa as funções necesarias para esta classe
from utils.generalfunctions import load_json, save_json, maiorIDLista, validaConfirmacao, validaData
from models.cliente import Cliente
import beaupy

#Cria uma classe para os clientes
class ClienteService:
    #Função que importa dos dados do json para os objetos
    def __init__(self):
        self.listCliente = load_json('data/listcliente.json')
        self.listBooking = load_json('data/listbooking.json')
    #Função que gera o menu dos clientes em beaupy
    def menu(self):
        while True:
            options = ["Listar Clientes", "Adicionar Cliente", "Atualizar Cliente", "Remover Cliente", "Voltar"]
            choice = beaupy.select(options, cursor='->', cursor_style='red', return_index=True)
            if choice == 0:
                self.listaClientes()
            elif choice == 1:
                self.adicionaCliente()
            elif choice == 2:
                self.atualizaCliente()
            elif choice == 3:
                self.removeCliente()
            elif choice == 4:
                break
    #Função que imprime os cliente de uma forma estruturada
    def listaClientes(self):
        print("\n=== Lista de Clientes ===")
        for cliente in self.listCliente:
            print(f"ID: {cliente['id']}")
            print(f"Nome: {cliente['nome']}")
            print(f"NIF: {cliente['nif']}")
            print(f"Data de Nascimento: {cliente['dataNascimento']}")
            print(f"Telefone: {cliente['telefone']}")
            print(f"Email: {cliente['email']}")
            print("-" * 30)
    # Função que adiciiona um cliente á lista de clientes
    def adicionaCliente(self):
        try:
            novoID = maiorIDLista(self.listCliente) + 1
            nome = self.validaNoneNullInput("Nome: ")
            nif = self.validaNif()
            dataNascimento = validaData(input("Data de Nascimento (YYYY-MM-DD): "))
            telefone = self.validaTelefone()
            email = self.validaEmail()

            novo_cliente = Cliente(novoID, nome, nif, dataNascimento, telefone, email)
            self.listCliente.append(novo_cliente.__dict__)
            self.guardaAlteracoesCliente()
            print(f"Cliente adicionado com sucesso. ID atribuído: {novoID}")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao adicionar o cliente: {e}")

    def selecionaCliente(self):
        opcoesCliente = [f"{cliente['id']} - {cliente['nome']}" for cliente in self.listCliente]
        clienteEscolha = beaupy.select(opcoesCliente, cursor='->', cursor_style='red', return_index=True)
        return self.listCliente[clienteEscolha]


    #Função que atualiza o cliente com novos dados
    def atualizaCliente(self):
        try:
            cliente = self.selecionaCliente()
            cliente['nome'] = self.validaNoneNullInput(f"Novo Nome ({cliente['nome']}): ", optional=True) or cliente['nome']
            cliente['nif'] = self.validaNif(cliente['nif'])
            
            novaDataNascimento = input(f"Nova Data de Nascimento ({cliente['dataNascimento']}): ")
            cliente['dataNascimento'] = validaData(novaDataNascimento, optional=True) or cliente['dataNascimento']
            
            cliente['telefone'] = self.validaTelefone(cliente['telefone'])
            cliente['email'] = self.validaEmail(cliente['email'])

            self.guardaAlteracoesCliente()
            print("Cliente atualizado com sucesso.")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao atualizar o cliente: {e}")

    #Função que remove um cliente do ficheiro json
    def removeCliente(self):
        try:
            cliente = self.selecionaCliente()
            if any(booking['cliente_id'] == cliente['id'] for booking in self.listBooking):
                print("Este cliente não pode ser removido porque tem reservas associadas.")
                return

            confirm = validaConfirmacao(f"Tem certeza que deseja remover o cliente {cliente['nome']} (ID: {cliente['id']})? (S/N): ")
            if confirm == 'S':
                self.listCliente = [c for c in self.listCliente if c['id'] != cliente['id']]
                self.guardaAlteracoesCliente()
                print("Cliente removido com sucesso.")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao remover o cliente: {e}")
    #função que grava as alterações no ficheiro json
    
    def guardaAlteracoesCliente(self):
        save_json('data/listcliente.json', self.listCliente)
    # função que valida se o input não contem nada
    def validaNoneNullInput(self, valor, optional=False):
        while True:
            value = input(valor)
            if optional and not value:
                return None
            if value:
                return value
            print("Este campo não pode estar vazio.")
    # função que valida se o nif já existe em algum cliente
    def validaNif(self, NIFAtual=None):
        while True:
            try:
                nif = int(input("NIF: ") if NIFAtual is None else input(f"Novo NIF ({NIFAtual}): ") or NIFAtual)
                if nif != NIFAtual and any(cliente['nif'] == nif for cliente in self.listCliente):
                    print("Erro: Este NIF já está cadastrado para outro cliente.")
                else:
                    return nif
            except ValueError:
                print("Por favor, insira um NIF válido.")
    # Função que valida se o telefone já existe em algum cliente
    def validaTelefone(self, telefoneAtual=None):
        while True:
            telefone = input("Telefone: ") if telefoneAtual is None else input(f"Novo Telefone ({telefoneAtual}): ") or telefoneAtual
            if telefone != telefoneAtual and any(cliente['telefone'] == telefone for cliente in self.listCliente):
                print("Erro: Este telefone já está cadastrado para outro cliente.")
            else:
                return telefone
    # Função que valida se o email já existe em algum cliente
    def validaEmail(self, emailAtual=None):
        while True:
            email = input("Email: ") if emailAtual is None else input(f"Novo Email ({emailAtual}): ") or emailAtual
            if email != emailAtual and any(cliente['email'] == email for cliente in self.listCliente):
                print("Erro: Este email já está cadastrado para outro cliente.")
            else:
                return email
    def selecionaCliente(self):
        opcoesCliente = [f"{cliente['id']} - {cliente['nome']}" for cliente in self.listCliente]
        escolhaCliente = beaupy.select(opcoesCliente, cursor='->', cursor_style='red', return_index=True)
        return self.listCliente[escolhaCliente]

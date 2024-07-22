# Importa as funções que vamos utilizar nesta classe
from utils.generalfunctions import load_json, save_json, validaMatricula, maiorIDLista, verificaIDInteiro, validaConfirmacao
from models.automovel import Automovel
import beaupy

# Cria a classe
class AutomovelService:
    # Carrega os dados para os objetos
    def __init__(self):
        self.listAutomovel = load_json('data/listAutomovel.json')
        self.listBooking = load_json('data/listbooking.json')

    # Cria o menu dos automóveis
    def menu(self):
        while True:
            options = ["Listar Automóveis", "Adicionar Automóvel", "Atualizar Automóvel", "Remover Automóvel", "Voltar"]
            choice = beaupy.select(options, cursor='->', cursor_style='red', return_index=True)
            if choice == 0:
                self.listaAutomoveis()
            elif choice == 1:
                self.adicionaAutomovel()
            elif choice == 2:
                self.atualizaAutomovel()
            elif choice == 3:
                self.removeAutomovel()
            elif choice == 4:
                break

    # Função que lista os automóveis
    def listaAutomoveis(self):
        print("\n=== Lista de Automóveis ===")
        for automovel in self.listAutomovel:
            print(f"ID: {automovel['id']}")
            print(f"Matrícula: {automovel['matricula']}")
            print(f"Marca: {automovel['marca']}")
            print(f"Modelo: {automovel['modelo']}")
            print(f"Cor: {automovel['cor']}")
            print(f"Número de Portas: {automovel['portas']}")
            print(f"Preço Diário: €{automovel['precoDiario']:.2f}")
            print(f"Cilindrada: {automovel['cilindrada']} cc")
            print(f"Potência: {automovel['potencia']} cv")
            print("-" * 30)

    # Função que adiciona um automóvel à lista
    def adicionaAutomovel(self):
        try:
            novoID = maiorIDLista(self.listAutomovel) + 1
            matricula = self.verificaMatricula()
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            cor = input("Cor: ")
            portas = verificaIDInteiro("Portas: ")
            precoDiario = self.verificaFloat("Preço Diário: ")
            cilindrada = verificaIDInteiro("Cilindrada: ")
            potencia = verificaIDInteiro("Potência: ")

            novo_automovel = Automovel(novoID, matricula, marca, modelo, cor, portas, precoDiario, cilindrada, potencia)
            self.listAutomovel.append(novo_automovel.__dict__)
            self.guardaAlteracoesAutomovel()
            print("Automóvel adicionado com sucesso!")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao adicionar o automóvel: {e}")

    # Função que cria uma listagem de automóveis
    def selecionaAutomovel(self):
        opcoesAutomovel = [f"{automovel['id']} - {automovel['marca']} {automovel['modelo']}" for automovel in self.listAutomovel]
        automovelecolha = beaupy.select(opcoesAutomovel, cursor='->', cursor_style='red', return_index=True)
        return self.listAutomovel[automovelecolha]

    # Função que atualiza os dados de um automóvel
    def atualizaAutomovel(self):
        try:
            automovel = self.selecionaAutomovel()

            # Pede a matrícula, se fornecido, atualiza; senão, mantém o valor antigo
            automovel['matricula'] = self.verificaMatricula(automovel["matricula"], optional=True) or automovel['matricula']

            # Pede cada atributo, se fornecido, atualiza; senão, mantém o valor antigo
            automovel['marca'] = input(f"Marca ({automovel['marca']}): ") or automovel['marca']
            automovel['modelo'] = input(f"Modelo ({automovel['modelo']}): ") or automovel['modelo']
            automovel['cor'] = input(f"Cor ({automovel['cor']}): ") or automovel['cor']
            automovel['portas'] = verificaIDInteiro(f"Portas ({automovel['portas']}): ", optional=True) or automovel['portas']
            automovel['precoDiario'] = self.verificaFloat(f"Preço Diário ({automovel['precoDiario']}): ", optional=True) or automovel['precoDiario']
            automovel['cilindrada'] = verificaIDInteiro(f"Cilindrada ({automovel['cilindrada']}): ", optional=True) or automovel['cilindrada']
            automovel['potencia'] = verificaIDInteiro(f"Potência ({automovel['potencia']}): ", optional=True) or automovel['potencia']

            self.guardaAlteracoesAutomovel()
            print("Automóvel atualizado com sucesso!")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao atualizar o automóvel: {e}")

    # Função que remove um automóvel da lista
    def removeAutomovel(self):
        try:
            automovel = self.selecionaAutomovel()
            # Verifica se o carro tem algum booking associado
            if any(booking['automovel_id'] == automovel['id'] for booking in self.listBooking):
                print("Este automóvel não pode ser removido porque tem reservas associadas.")
                return
            # Confirma se o usuário quer fazer as alterações
            confirm = validaConfirmacao(f"Tem certeza que deseja remover o automóvel com a matrícula {automovel['matricula']} (ID: {automovel['id']})? (S/N): ")
            if confirm == 'S':
                self.listAutomovel = [c for c in self.listAutomovel if c['id'] != automovel['id']]
                self.guardaAlteracoesAutomovel()
                print("Automóvel removido com sucesso.")
        except (ValueError, IOError) as e:
            print(f"Ocorreu um erro ao remover o automóvel: {e}")

    # Função que guarda as alterações no ficheiro json
    def guardaAlteracoesAutomovel(self):
        save_json('data/listAutomovel.json', self.listAutomovel)

    # Função que verifica se é float, e que tem uma opção para colocar o valor como None
    def verificaFloat(self, mensagem, optional=False):
        while True:
            try:
                entrada = input(mensagem)
                if optional and entrada == '':
                    return None
                valor = float(entrada)
                return valor
            except ValueError:
                print("Por favor, insira um valor decimal válido.")

    # Função que verifica se a matrícula está no formato correto
    def verificaMatricula(self, matricula_antiga=None, optional=False):
        while True:
            try:
                entrada = input(f"Matrícula ({matricula_antiga if matricula_antiga else ''}): ")
                if optional and not entrada:
                    return None
                matricula = validaMatricula(entrada)
                if matricula:
                    return matricula
                else:
                    print("Matrícula inválida.")
            except ValueError as e:
                print(f"Erro: {e}")

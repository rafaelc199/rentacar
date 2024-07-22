import datetime
import beaupy
from utils.generalfunctions import load_json

#cria a classe pesquisas
class PesquisasService:
    def __init__(self):
        self.listBooking = load_json('data/listbooking.json')
        self.listCliente = load_json('data/listcliente.json')
        self.listAutomovel = load_json('data/listautomovel.json')
    #Cria o menu de pesquisas com validação  de inout
    def menu(self):
        while True:
            opcoes = ["Pesquisa por Cliente", "Pesquisa por Matrícula", "Listagem de Bookings Futuros", "Voltar"]
            opcao = beaupy.select(opcoes, cursor='->', cursor_style='red', return_index=True)
            if opcao == 0:
                try:    
                    nif = int(input("Introduza um NIF válido: "))
                    self.pesquisaClientePorNif(self.listCliente, self.listBooking, nif)
                except ValueError:
                    print("NIF inválido.")
            elif opcao == 1:
                try:    
                    matricula = input("Introduza uma matrícula válida: ")
                    self.pesquisaPorMatricula(self.listAutomovel, self.listBooking, matricula)
                except ValueError:
                    print("Matrícula inválida.")
            elif opcao == 2:
                self.listarBookingsFuturos(self.listBooking, self.listCliente, self.listAutomovel)
            elif opcao == 3:
                break
    #Função que vpesquisa o cliente com o NIF
    def pesquisaClientePorNif(self, listCliente, listBooking, nif):
        cliente = next((c for c in listCliente if c['nif'] == nif), None)
        if cliente:
            print(f"ID: {cliente['id']}, Nome: {cliente['nome']}, NIF: {cliente['nif']}, Telefone: {cliente['telefone']}, Email: {cliente['email']}")
            ultimos_alugueres = [b for b in listBooking if b['cliente_id'] == cliente['id']][-5:]
            for booking in ultimos_alugueres:
                print(f"Reserva de {booking['data_inicio']} a {booking['data_fim']} ({booking['numeroDias']} dias) - Total: {booking['precoReserva']:.2f}€")
        else:
            print("Cliente não encontrado.")
    #função que pesquisa o automvel com a matricula
    def pesquisaPorMatricula(self, listAutomovel, listBooking, matricula):
        automovel = next((a for a in listAutomovel if a['matricula'] == matricula), None)
        if automovel:
            print(f"ID: {automovel['id']}, Marca: {automovel['marca']}, Modelo: {automovel['modelo']}, Cor: {automovel['cor']}, Portas: {automovel['portas']}, Preço Diário: {automovel['precoDiario']}€")
            ultimos_alugueres = [b for b in listBooking if b['automovel_id'] == automovel['id']][-5:]
            for booking in ultimos_alugueres:
                print(f"Reserva de {booking['data_inicio']} a {booking['data_fim']} ({booking['numeroDias']} dias) - Total: {booking['precoReserva']:.2f}€")
        else:
            print("Automóvel não encontrado.")
    #Função que procura os futuros bookings
    def listarBookingsFuturos(self, listBooking, listCliente, listAutomovel):
        hoje = datetime.datetime.today().date()
        for booking in listBooking:
            data_inicio = datetime.datetime.strptime(booking['data_inicio'], '%Y-%m-%d').date()
            if data_inicio >= hoje:
                cliente = next((c for c in listCliente if c['id'] == booking['cliente_id']), None)
                automovel = next((a for a in listAutomovel if a['id'] == booking['automovel_id']), None)
                if cliente and automovel:
                    print(f"Booking data início: {booking['data_inicio']} | data fim: {booking['data_fim']} ({booking['numeroDias']} dias)")
                    print(f"Cliente: {cliente['nome']}")
                    print(f"Automóvel: {automovel['marca']} – Matrícula: {automovel['matricula']}")
                    print(f"Total: {booking['precoReserva']:.2f}€\n")


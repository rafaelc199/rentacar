#importa as funções que vamos utilizar neste codigo
from utils.generalfunctions import load_json, save_json, validaConfirmacao, maiorIDLista, selecionaCliente , selecionaAutomovel,validaData
from datetime import datetime
import beaupy
#Definimos uma classe para os bookings
class BookingService:
    #Função que carrega os dados em json para os objetos
    def __init__(self):
        self.listBooking = load_json('data/listbooking.json')
        self.listAutomovel = load_json('data/listautomovel.json')
        self.listCliente = load_json('data/listcliente.json')
    #Função que cria o menu dos bookings com o beaupy
    def menu(self):
        while True:
            options = ["Listar Reservas", "Adicionar Reserva", "Atualizar Reserva", "Remover Reserva", "Voltar"]
            choice = beaupy.select(options, cursor='->', cursor_style='red', return_index=True)
            if choice == 0:
                self.listaBookings()
            elif choice == 1:
                self.adicionaBookings()
            elif choice == 2:
                self.atualizaBookings()
            elif choice == 3:
                self.removeBooking()
            elif choice == 4:
                break
    #Função que imprime os bookings de uma forma estruturada
    def listaBookings(self):
        print("\n=== Lista de Reservas ===")
        for booking in self.listBooking:
            cliente = next((c for c in self.listCliente if c['id'] == booking['cliente_id']), None)
            automovel = next((a for a in self.listAutomovel if a['id'] == booking['automovel_id']), None)
            
            print(f"ID da Reserva: {booking['id']}")
            print(f"Data de Início: {booking['data_inicio']}")
            print(f"Data de Fim: {booking['data_fim']}")
            print(f"Cliente: {cliente['nome']}")
            print(f"Automóvel: {automovel['marca']} {automovel['modelo']}")
            print(f"Preço da Reserva: €{booking['precoReserva']:.2f}")
            print(f"Número de Dias: {booking['numeroDias']}")
            print("-" * 30)
    
    #Função que adiciona um novo booking a lista de bookings
    def adicionaBookings(self):
        try:
            data_inicio = validaData(input("Introduza a Data de Início (YYY-MM-DD)"))
            data_fim = validaData(input("Selecionar Data de Fim (YYYY-MM-DD)"))
            if datetime.strptime(data_fim, '%Y-%m-%d') <= datetime.strptime(data_inicio, '%Y-%m-%d'):
                raise ValueError("A data de fim deve ser posterior à data de início.")

            cliente_id = selecionaCliente(self.listCliente)
            automovel_id = selecionaAutomovel(self.listAutomovel)
            
            numeroDias = (datetime.strptime(data_fim, '%Y-%m-%d') - datetime.strptime(data_inicio, '%Y-%m-%d')).days
            precoReserva = self.calculaPreco(automovel_id, numeroDias)
            precoFinal = self.AplicaDescontos(numeroDias, precoReserva)
            
            novaReserva = {
                "id": maiorIDLista(self.listBooking)+1,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "cliente_id": cliente_id,
                "automovel_id": automovel_id,
                "precoReserva": precoFinal,
                "numeroDias": numeroDias
            }
            
            if self.verificaDisponibilidade(automovel_id, data_inicio, data_fim):
                self.listBooking.append(novaReserva)
                self.guardaAlteracoesBooking()
                print("Reserva adicionada com sucesso!")
            else:
                print("Este automóvel não está disponível para as datas especificadas.")
        
        except ValueError as e:
            print(f"Erro ao adicionar reserva: {e}")
    #Função booleana que verifica a diponibilidade do carro numa determinada data
    def verificaDisponibilidade(self, automovel_id, data_inicio, data_fim):
        for reserva in self.listBooking:
            if reserva["automovel_id"] == automovel_id:
                if (data_inicio >= reserva["data_inicio"] and data_inicio <= reserva["data_fim"]) or \
                   (data_fim >= reserva["data_inicio"] and data_fim <= reserva["data_fim"]) or \
                   (data_inicio <= reserva["data_inicio"] and data_fim >= reserva["data_fim"]):
                    return False 
        return True 
    #Função que atualiza os bookings com novos dados
    def atualizaBookings(self):
        try:
            booking_options = []
            for booking in self.listBooking:
                cliente = next((c for c in self.listCliente if c['id'] == booking['cliente_id']), None)
                automovel = next((a for a in self.listAutomovel if a['id'] == booking['automovel_id']), None)
                
                if cliente and automovel:
                    option = f"ID: {booking['id']} | Data Início: {booking['data_inicio']} | Data Fim: {booking['data_fim']} | Cliente: {cliente['nome']} | Automóvel: {automovel['marca']} {automovel['modelo']}"
                    booking_options.append(option)
            
            escolhaBooking = beaupy.select(booking_options, cursor='->', cursor_style='red', return_index=True)
            booking = self.listBooking[escolhaBooking]
            
            cliente = next((c for c in self.listCliente if c['id'] == booking['cliente_id']), None)
            automovel = next((a for a in self.listAutomovel if a['id'] == booking['automovel_id']), None)
            
            print(f"\nReserva selecionada para atualização:")
            print(f"ID: {booking['id']}")
            print(f"Data de Início: {booking['data_inicio']}")
            print(f"Data de Fim: {booking['data_fim']}")
            print(f"Cliente: {cliente['nome']}")
            print(f"Automóvel: {automovel['marca']} {automovel['modelo']}")
            print(f"Preço da Reserva: €{booking['precoReserva']:.2f}")
            print(f"Número de Dias: {booking['numeroDias']}")
            print("-" * 30)

            novaDataInicio = input(f"Nova Data de Início ({booking['data_inicio']}): ")
            novaDataFim = input(f"Nova Data de Fim ({booking['data_fim']}): ")

            novaDataInicio = validaData(novaDataInicio, optional=True) or booking['data_inicio']
            novaDataFim = validaData(novaDataFim, optional=True) or booking['data_fim']

            if novaDataInicio:
                booking['data_inicio'] = novaDataInicio
            if novaDataFim:
                booking['data_fim'] = novaDataFim

            # seleciona cliente e automovel com o beaupy
            booking['cliente_id'] = selecionaCliente(self.listCliente)
            booking['automovel_id'] = selecionaAutomovel(self.listAutomovel)
            
            # Calcula o numero de dias e preço da reserva para atualizar
            numeroDias = (datetime.strptime(booking['data_fim'], '%Y-%m-%d') - datetime.strptime(booking['data_inicio'], '%Y-%m-%d')).days
            booking['precoReserva'] = self.calculaPreco(booking['automovel_id'], numeroDias)
            booking['precoReserva'] = self.AplicaDescontos(numeroDias, booking['precoReserva'])
            # Guarda as alterações no ficheiro json
            self.guardaAlteracoesBooking()
            print("Reserva atualizada com sucesso.")
        
        except ValueError as e:
            print(f"Erro ao atualizar reserva: {e}")
   
    # Função que remove um booking
    def removeBooking(self):
        try:
            booking_options = []
            for booking in self.listBooking:
                cliente = next((c for c in self.listCliente if c['id'] == booking['cliente_id']), None)
                automovel = next((a for a in self.listAutomovel if a['id'] == booking['automovel_id']), None)
                
                if cliente and automovel:
                    option = f"Data inicio: {booking['data_inicio']} Data fim: {booking['data_fim']} Cliente: {cliente['nome']} Automovel: {automovel['marca']} {automovel['modelo']}"
                    booking_options.append(option)
            
            escolhaBooking = beaupy.select(booking_options, cursor='->', cursor_style='red', return_index=True)
            booking = self.listBooking[escolhaBooking]
            
            cliente = next((c for c in self.listCliente if c['id'] == booking['cliente_id']), None)
            automovel = next((a for a in self.listAutomovel if a['id'] == booking['automovel_id']), None)

            confirmarRemocao = validaConfirmacao(f"Tem a certeza que deseja eliminar a reserva com Data Inicio: {booking['data_inicio']} Data fim: {booking['data_fim']} Cliente: {cliente['nome']} Automovel: {automovel['marca']} {automovel['modelo']} ? S/N")
            
            if confirmarRemocao:
                self.listBooking.remove(booking)
                self.guardaAlteracoesBooking()
                print("Reserva removida com sucesso!")
            else:
                print("Operação cancelada.")
        
        except ValueError as e:
            print(f"Erro ao remover reserva: {e}")
    # Função que calcula o preço da reseva
    def calculaPreco(self, automovel_id, numeroDias):
        for automovel in self.listAutomovel:
            if automovel['id'] == automovel_id:
                return automovel['precoDiario'] * numeroDias
        return 0
    #Função que aplica os descontos de acordo com os dias da reserva
    def AplicaDescontos(self, numeroDias, precoReserva):
        if numeroDias <= 4:
            desconto = 0
        elif 5 <= numeroDias <= 8:
            desconto = 0.15
        elif numeroDias >=9:
            desconto = 0.25
        return precoReserva * (1 - desconto)
    #Função que guarda os booking no ficheiro json
    def guardaAlteracoesBooking(self):
        save_json('data/listbooking.json', self.listBooking)

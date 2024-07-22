#cria a classe booking
class Booking:
    def __init__(self, data_inicio, data_fim, cliente_id, automovel_id, precoReserva, numeroDias):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.cliente_id = cliente_id
        self.automovel_id = automovel_id
        self.precoReserva = precoReserva
        self.numeroDias = numeroDias

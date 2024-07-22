#cria a classe cliente
class Cliente:
    def __init__(self, id, nome, nif, dataNascimento, telefone, email):
        self.id = id
        self.nome = nome
        self.nif = nif
        self.dataNascimento = dataNascimento
        self.telefone = telefone
        self.email = email

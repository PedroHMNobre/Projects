import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("Saldo excedido")
            return False
        
        if valor > 0:
            self._saldo -= valor
            print("Saque realizado")
            return True
        
        print("Operação falhou")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado")
            return True
        
        print("Operação falhou")
        return False
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Valor de saque excede o limite")
            return False
        
        if excedeu_saques:
            print("Número máximo de saques excedido")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
"""

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def obter_cpf():
    while True:
        cpf = input("CPF: ")
        if cpf:
            return cpf
        print("CPF não pode ser vazio. Tente novamente.")

def menu():
    menu_texto = f"""\n
    {"-=-"*6} MENU {"-=-"*6}
    [d]\tDepositar;
    [s]\tSacar;
    [e]\tExtrato;     
    [nc]\tNova Conta;
    [nu]\tNovo Usuário;
    [q]\tSair
    --> """
    return input(textwrap.dedent(menu_texto))

def depositar(clientes):               
    cpf = obter_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return 
    
    valor = float(input("Depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = obter_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return

    valor = float(input("Saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
       
def ver_extrato(clientes):
    cpf = obter_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return 
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("Extrato\n")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")

def criar_cliente(clientes):
    while True:
        cpf = input("Informe o CPF (somente números): ")
        cliente = filtrar_cliente(cpf, clientes)

        if cliente:
            print("Já existe usuário com esse CPF!")
            continue
        
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

        clientes.append(cliente)
        print("Usuário criado com sucesso")
        break

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None 

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui contas")
        return None

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def criar_conta(numero_conta, clientes, contas):
    while True:
        cpf = obter_cpf()
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("Cliente não encontrado")
            continue 
        
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.adicionar_conta(conta)

        print("Conta criada com sucesso")
        break

def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "d":
            depositar(clientes)
        
        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            ver_extrato(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "q":
            print("Obrigado por ser nosso cliente, tenha um ótimo dia!")
            break
        
        else:
            print("Opção inválida, tente novamente.")
            
main()

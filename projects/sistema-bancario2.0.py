import datetime
import textwrap

"""-- 1.0
    Sistema deve informar que não a saldo, caso não haja saldo !!
    Todos os saques e deposito devem ser exibidos em uma variavel "extrato"!
    Os valores deve ser exibidos no formato: R$ xxx.xx
-- 2.0
    Alterar todas as outras funcionalidades para funções
    Adicionar 2 novas funções, 'criar usuário' e 'criar conta corrente'
"""


def menu():
    menu = f"""\n
    {"-=-"*6} MENU {"-=-"*6}
    [c]\tConsultar saldo;
    [d]\tDepositar;
    [s]\tSacar;
    [e]\tExtrato;     
    [nc]\tNova Conta;
    [nu]\tNovo Usuário;
    [q]\tSair
    --> """
    return input(textwrap.dedent(menu))

def login(login_user, login_pass):
    print("Bem-vindo ao banco Nobre")
    login_user = input("Usurário: ")
    login_pass = input("Senha: ")
    if login_user in usuarios and usuarios[login_user]["senha"] == login_pass:
        return f"\nOlá, {login_user},\nSaldo atual: R$ {usuarios[login_user]['saldo']}"
    else:
        return "Tente novamente!!"

def depositar(saldo, deposito, extrato, /):               
    if deposito > 0:
        saldo += deposito
        agora = datetime.datetime.now()
        extrato += f"Depósito: R$ {deposito:.2f} -- Time: {agora.strftime("%d/%m/%Y %H:%M:%S")}\n"
        print(f"Deposito realizado com sucesso")
    else:
        print("Valor informado errado, tente novamente!")
    
    return saldo, extrato
  
def sacar(*, saldo, saque, extrato, limite_diario, cont_saques, limite_saque):
    excedeu_saldo = saque > saldo
    excedeu_limite = saque > limite_diario
    excedeu_saque = cont_saques == limite_saque
    if excedeu_saldo:
        print("Operação falhou, saldo insuficiente.")
    if excedeu_limite:
        print("Operação falhou, excedeu limite de saque.")
    if excedeu_saque:
        print("Operação falhou, excedeu números de saques permitidos")
    elif saque > 0:
        saldo -= saque
        agora = datetime.datetime.now()
        print(f"Saque: R$ -{saque}\nSaldo Restante: R$ {saldo:.2f} ")
        extrato += f"Saque: R$ -{saque:.2f} -- Registro: {agora.strftime("%d/%m/%Y %H:%M:%S")}\n"
        cont_saques += 1
    else:
        print("Erro, certifique-se de que tenha o saldo em conta e o valor sacado seja inferior ao limite de R$ 500,00")
        
    return saldo, extrato, cont_saques
        
def ver_extrato(saldo, /, *, extrato):
    print("\nNão foram realizadas movimentações" if not extrato else extrato)        
    return (f"\nSegue seu extrato:\n{saldo:.2f}")

def criar_usuario(usuario):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): )")

    usuario.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco":endereco})
    print("Usuario criado com sucesso")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None 

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso!")
        return {"agencia":agencia, "numero_conta":numero_conta, "usuario":usuario}
    
    print("Usuario não encontrado, fluxo de criação de conta encerrado!!")


def main():
    LIMITE_SAQUE = 3
    AGENCIA = "0001"

    saldo = 0
    extrato = ""
    limite_diario = 500
    cont_saques = 0
    usuarios = []
    contas = []
    
    while True:
        init = menu()
        
        if init == "d":
            deposito = float(input("Insira o valor de depósito: "))
            
            saldo, extrato = depositar(saldo, deposito, extrato)

        elif init == "s":
            
            saque = float(input("Insira o valor de saque: "))

            saldo, extrato, cont_saques = sacar(
                saldo=saldo,
                saque=saque,
                extrato=extrato,
                limite_diario=limite_diario,
                cont_saques=cont_saques,
                limite_saque=LIMITE_SAQUE,
            )

        elif init == "e":
            ver_extrato(saldo, extrato=extrato)

        elif init == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif init == "nu":
            criar_usuario(usuarios)

        elif init == "q":
            print("Obrigado por ser nosso cliente, tenha um otimo dia!")
            break
        
        else:
            print("Opção inválido, tente novamente.")
            
main()

                  
import datetime

"""-- 1.0
    Sistema deve informar que não a saldo, caso não haja saldo !!
    Todos os saques e deposito devem ser exibidos em uma variavel "extrato"!
    Os valores deve ser exibidos no formato: R$ xxx.xx"""


menu = """
    (c) - Consultar Saldo;
    (d) - Depositar;
    (s) - Sacar;
    (e) - Extrato;     
    (q) - Sair
--> """
saldo = 0
extrato = ""
limite_diario = 500
cont_saques = 0
LIMITE_SAQUE = 3

usuarios = {  #Banco de Dados Usuários
    "pedronobre": {"senha": "1234", "saldo": 0.0, "extrato": ""},
    "brendastephanie": {"senha": "1234", "saldo": 0.0, "extrato": ""}
           }

while True:
    print("Bem-vindo ao banco Nobre")
    login_user = input("Usurário: ")
    login_pass = input("Senha: ")
    

    if login_user in usuarios and usuarios[login_user]["senha"] == login_pass:
        print(f"\nOlá, {login_user},\nSaldo atual: R$ {usuarios[login_user]["saldo"]}")
    
        while True:
            init = input(menu)

            if init == "c":

                agora = datetime.datetime.now()
                print(f"Seu saldo é: R${usuarios[login_user]["saldo"]} -- Time: {agora.strftime("%d/%m/%Y %H:%M:%S")}\n ")

            elif init == "d":
                
                try: 
                    deposito = float(input("Insira o valor de depósito: "))

                    if deposito > 0:
                        usuarios[login_user]["saldo"] += deposito
                        print(f"Saldo:R$ {usuarios[login_user]["saldo"]:.2f}")
                        agora = datetime.datetime.now()
                        usuarios[login_user]["extrato"] += f"Depósito: R$ {deposito:.2f} -- Time: {agora.strftime("%d/%m/%Y %H:%M:%S")}\n"

                    else:
                        print("Valor informado errado, tente novamente!")
                except:
                    print("Verifique o valor inserido!")
            elif init == "s":
                
                if cont_saques == LIMITE_SAQUE:
                    print("Você atingiu o limite de 3 saques diário!")

                else:
                    try:
                        saque = float(input("Insira o valor de saque: "))
                        
                        if usuarios[login_user]["saldo"] >= saque and saque <= limite_diario:

                            usuarios[login_user]["saldo"] -= saque
                            agora = datetime.datetime.now()
                            print(f"Saque: R$ -{saque}\nSaldo Restante: R$ {usuarios[login_user]["saldo"]:.2f} ")
                            usuarios[login_user]["extrato"] += f"Saque: R$ -{saque:.2f} -- Registro: {agora.strftime("%d/%m/%Y %H:%M:%S")}\n"
                            cont_saques += 1

                        else:
                            print("Erro, certifique-se de que tenha o saldo em conta e o valor sacado seja inferior ao limite de R$ 500,00")
                    except:
                        print("Verifique o valor inserido!")

            elif init == "e":

                print(f"Segue abaixo seu extrato:\n{usuarios[login_user]["extrato"]}\nSaldo: {usuarios[login_user]["saldo"]}")
                           
            elif init == "q":

                print("Obrigado por ser nosso cliente, tenha um otimo dia!")
                break

            else:
                print("Opção inválido, tente novamente.")

    else:
        print("Tente novamente, usuario ou senha incorreto")
    
    out = input("Digite 'q' novamente para sair ou 'r para acessar novamente: ")
    if out == "q":
        print("Obrigado, volte sempre!")
        break
    
    else:
        print("Tente novamente, usuario ou senha incorreto")

    

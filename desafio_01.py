"""
    Desafio onde deverá ser criado um sistema bancário com as funções de depósito, saque e extrato.

# OPERAÇÃO DE DEPÓSITO:
    - o sistema trabalha com apenas um único usuário
    - depósito apenas de valores positivos
    - valores inseridos na variável e exibidos na função de extrato
# OPERAÇÃO DE SAQUE:
    - limite de 3 saques diários com limite total de cada um sendo de R$ 500,00
    - caso o cliente tente sacar valor que não tem na conta o sistema informa o valor restante e diz que nao pode sacar além disso
    - todos os saques devem ser armazenados em uma varoável e exibidos na função de extrato
# OPERAÇÃO DE EXTRATO:
    - lista todas as operações realizadas na conta
    - no fim da listagem deve exibir pro usuário o saldo atual da conta
"""


lista_extrato = []
valor_conta = 0
limite_saque = 3
total_sacado = 0

def deposito(valor_conta, lista_extrato):
    valor_deposito = float(input('Digite o valor a ser depositado em R$(apenas números)-> '))
    if valor_deposito > 0:
        lista_extrato.append(f'Depósito: R$ {valor_deposito:.2f}')
        valor_conta += valor_deposito
        print('Valor transferido para a sua conta com sucesso!')
        print(f'Valor atual -> R${valor_conta:.2f}')
    return valor_conta, lista_extrato


def saque(valor_conta, total_sacado, limite_saque, lista_extrato):
    print(f'Você ainda pode fazer {limite_saque} saques')
    print('Cada saque tem limite de R$500,00')
    print('-=' * 30)
    valor_saque = float(input('Digite o valor a ser sacado em R$(apenas números) _>)'))

    if valor_saque > valor_conta:
        print('Operação não pode ser realizada: saldo insuficiente na conta.')
    
    elif limite_saque == 0:
        print("Operação não pode ser realizada: limite diário de saques atingido.")

    elif valor_saque > 500:
        print('Operação não pode ser realizada: valor excede o limite de R$500,00 por saque.')

    elif valor_saque <= 0:
        print('Operação inválida: valor deve ser maior que zero.')

    else:
        lista_extrato.append(f'Saque: R${valor_saque:.2f}')
        valor_conta -= valor_saque
        total_sacado += valor_saque
        limite_saque -= 1
        print('Valor sacado com sucesso!')
        print(f'Valor atual -> R${valor_conta:.2f}')
    return valor_conta, total_sacado, limite_saque



while True:
    print("""
    ================ MENU ================
    [1] Depósito
    [2] Saque
    [3] Extrato
    [4] Sair
    ======================================
    """)

    escolha = int(input('Digite o número da operação desejada-> '))

    if escolha == 1:
        valor_conta, lista_extrato = deposito(valor_conta, lista_extrato)
    
    elif escolha == 2:
        valor_conta, total_sacado, limite_saque = saque(valor_conta, total_sacado, limite_saque, lista_extrato)

    elif escolha == 3:
        if lista_extrato:
            print('Extrato da conta:')
            for operacao in lista_extrato:
                print(operacao)
        else:
            print('Nenhuma Operação Realizada!')
        print( f'Saldo atual: R${valor_conta:.2f}')

    elif escolha == 4:
        print('Você escolheu sair, programa encerrado!')
        break

    else:
        print('X_X_Opção_Inválida_Programa_Encerrado_X_X')
        break
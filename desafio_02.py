# melhoria no sistema bancário feito no desafio_01.py

usuarios = []
contas = []
AGENCIA = '0001'

def deposito(saldo, valor, extrato, /):
    if valor > 0:
        extrato.append(f'Depósito: R$ {valor:.2f}')
        saldo += valor
        print('Valor depositado com sucesso!')
    else:
        print('Valor inválido para depósito')
    return saldo, extrato


def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print('Limite diário de saques atingidos.')
    elif valor > limite:
        print('valor excede o limite por saque.')
    elif valor > saldo:
        print('Saldo insuficiente.')
    elif valor <= 0:
        print('Valor de saque inválido.')
    else:
        extrato.append(f'Saque: R$ {valor:.2f}')
        saldo -= valor
        numero_saques +=1
        print('Saque realizado com sucesso.')
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n======= EXTRATO =======")
    if extrato:
        for operacao in extrato:
            print(operacao)
    else:
        print('Não foram realizadas movimentações.')
        print(f'Saldo atual: R$ {saldo:.2f}')
        print("========================\n")


def criar_usuario():
    cpf = input('Digite o CPF (somente números): ').strip()
    cpf = ''.join(filter(str.isdigit, cpf))

    if any(u['cpf'] == cpf for u in usuarios):
        print('Usuário com esse cpf já existe.')
        return

    nome = input('Nome completo: ').strip()
    nascimento = input('Data de nascimento (dd-mm-aaaa): ').strip()
    endereco = input('Endereço (logradouro, nro - bairro - cidade/sigla estado): ').strip()

    usuarios.append({
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print('Usuário criado com sucesso!')


def encontrar_usuario(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    for u in usuarios:
        if u['cpf'] == cpf:
            return u
    return None


def criar_conta():
    cpf = input('Informe o CPF do usuário: ').strip()
    usuario = encontrar_usuario(cpf)

    if usuario:
        numero_conta = len(contas) + 1
        contas.append({
            "agencia": AGENCIA,
            "numero": numero_conta,
            "usuario": usuario
        })
        print(f"Conta criada: Agência {AGENCIA} Número {numero_conta}")
    else:
        print("Usuário não encontrado.")


def listar_contas():
    for conta in contas:
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero']} | Titular: {conta['usuario']['nome']}")



def menu():
    saldo = 0
    extrato_lista = []
    limite = 500
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        print("""
        ================ MENU ================
        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Criar Usuário
        [5] Criar Conta
        [6] Listar Contas
        [7] Sair
        ======================================
        """)
        
        opcao = input("Escolha a operação: ")

        if opcao == "1":
            valor = float(input("Digite o valor do depósito: R$ "))
            saldo, extrato_lista = deposito(saldo, valor, extrato_lista)

        elif opcao == "2":
            valor = float(input("Digite o valor do saque: R$ "))
            saldo, extrato_lista, numero_saques = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato_lista,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato_lista)

        elif opcao == "4":
            criar_usuario()

        elif opcao == "5":
            criar_conta()

        elif opcao == "6":
            listar_contas()

        elif opcao == "7":
            print("Saindo... Até logo!")
            break

        else:
            print("Opção inválida.")


menu()
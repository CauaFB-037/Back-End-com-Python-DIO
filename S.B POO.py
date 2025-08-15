from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

# ================== CLASSES DE CLIENTE ==================

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


# ================== CLASSE HISTÓRICO ==================

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


# ================== CLASSES DE CONTA ==================

class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def saldo_conta(self):
        return self.saldo
    
    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para saque! @@@")
            return False
        if valor > self.saldo:
            print("\n@@@ Saldo insuficiente! @@@")
            return False

        self.saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para depósito! @@@")
            return False

        self.saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ O valor do saque excedeu o limite. @@@")
            return False
        elif excedeu_saques:
            print("\n@@@ Número máximo de saques excedido. @@@")
            return False
    
        if super().sacar(valor):
            self.numero_saques += 1
            return True
        
        return False


# ================== INTERFACE E TRANSAÇÕES ==================

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
        
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


# ================== FUNÇÕES AUXILIARES ==================

def menu():
    opcoes = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(opcoes)).lower().strip()


def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]  # sempre retorna a primeira conta


def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f} em {transacao['data']}")

    print(f"\nSaldo:\t\tR$ {conta.saldo_conta():.2f}")
    print("==========================================")


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}    
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


# ================== MAIN ==================

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
            
            valor = float(input("Informe o valor do depósito: "))
            transacao = Deposito(valor)

            conta = recuperar_conta_cliente(cliente)
            if conta:
                cliente.realizar_transacao(conta, transacao)

        elif opcao == "s":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)
            
            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
            
            valor = float(input("Informe o valor do saque: "))
            transacao = Saque(valor)

            conta = recuperar_conta_cliente(cliente)
            if conta:
                cliente.realizar_transacao(conta, transacao)

        elif opcao == "e":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
                
            conta = recuperar_conta_cliente(cliente)
            if conta:
                exibir_extrato(conta)
        
        elif opcao == "nu":
            cpf = input("Informe o CPF (somente números): ")
            cliente = filtrar_cliente(cpf, clientes)

            if cliente:
                print("\n@@@ Já existe um cliente com esse CPF! @@@")
                continue
            
            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sígla estado): ")

            cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
            clientes.append(cliente)
            print("\n=== Cliente criado com sucesso! ===")

        elif opcao == "nc":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue
                
            numero_conta = len(contas) + 1
            conta = ContaCorrente.nova_conta(cliente, numero_conta)
            contas.append(conta)
            cliente.adicionar_conta(conta)

            print("\n=== Conta criada com sucesso! ===")

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break
            
        else:
            print("\n@@@ Operação inválida! @@@")


if __name__ == "__main__":
    main()

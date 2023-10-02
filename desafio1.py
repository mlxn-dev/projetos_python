from datetime import datetime
import locale
#  Configuração de locale para formatação de moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#  Classe Banking gerencia saldo, limite e uso do limite e permite emissão de extrato de entrada e saída de valores e suas datas   
class Banking:
    def __init__(self):
        self.saldo = 0
        self.uso_limite = 0
        self.limite = 100000
        self.extrato = []

    def saldo_com_limite(self) -> str:
        #  Retorna o saldo e o limite restante
        return 'Saldo: {}\nLimite Utilizado: {}\nLimite Restante: {}'.format(locale.currency(self.saldo/100), locale.currency((self.uso_limite)/100), locale.currency((self.limite - self.uso_limite)/100))

    def depositar(self, valor: int):
        #  testa se o limite foi usado
        if self.flag_uso_limite():
            #  testa de o valor depositado é maior que o limite usado
            if valor >= self.uso_limite:
                self.saldo += (valor - self.uso_limite)
                self.uso_limite = 0
                self.extrato.append({'+': str(locale.currency(valor/100)), 'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')})
                return self.saldo_com_limite()
            
            else:
                self.uso_limite -= valor
                self.extrato.append({'+': str(locale.currency(valor/100)), 'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')})
                return self.saldo_com_limite()
            
        else:
            self.saldo += valor
            self.extrato.append({'+': str(locale.currency(valor/100)), 'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')})
            return self.saldo_com_limite()
    
    def flag_uso_limite(self) -> bool:
        #  testa se o limite foi usado
        if self.uso_limite == 0:
            return False
        else:
            return True
    
    def flag_limite_estourado(self) -> bool:
        #  testa se o limite foi atingido, a função sacar() não pode ser usada se o limite foi atingido
        if self.uso_limite == self.limite:
            return True
        else:
            return False

    def sacar(self, valor: int):
        #  testa bloqueio de saque
        if self.flag_limite_estourado():
            return "Limite de saque atingido - operação bloqueada."
        
        #  checa se há saldo disponível para o saque
        if self.saldo >= valor:
            self.saldo -= valor
            self.extrato.append({'-': str(locale.currency(valor/100)), 'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')})

            return self.saldo_com_limite()
        
        #  checa se há saldo disponível + limite para o saque
        elif self.saldo + self.limite >= valor:
            #  checa de deseja usar o limite
            usar_limite = input("Deseja usar o limite disponível? [s]/[n]): ")

            if str(usar_limite).lower() == 's':
                self.uso_limite += (valor - self.saldo)
                self.saldo = 0
                self.extrato.append({'-': str(locale.currency(valor/100)), 'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')})
                return self.saldo_com_limite()
            
            else:
                return "Operação cancelada."
            
        else:
            return "Fundos insuficientes."
        
    def emitir_extrato(self):
        #  emite extrato de transações
        print('='*40)
        print('EXTRATO')

        if len(self.extrato) == 0:
            print('Nenhuma transação realizada.')
            print('='*40)
            return None
        
        print('OP R$ VALOR, DATA')
        for i in self.extrato:
            key = list(i.keys())

            value = list(i.values())
            print(key[0], value[0], ', ', value[1])
        print('-'*40)
        print(self.saldo_com_limite())
        print('='*40)


#  Funções auxiliares
#  Função para tratamento de input de valores monetários
def currency_input_handler() -> int:
    #  exemplo: input=1.010,75 -> output=101075
    #           input=1.010,7 -> output=101070
    #           input=1.010, -> output=101000
    #           input=1.010 -> output=101000
    #           input=1010 -> output=101000
    #           input=0, -> output=erro
    #  não sei como daria para melhorar, mas funciona
    #  a ideia é todo armazenamento dos valores ser feito como número inteiro
    #  e a formatação para moeda ser feita apenas na exibição dos valores
    #  a formatação para moeda é feita com locale.currency(valor/100) sendo type(valor) == int
    #  float não é usado para evitar problemas de arredondamento (e.g. 1.010,75 -> 1010.75 == 1010.7499999999999)
    try:
        print('Digite o valor desejado (e.g. 1.010,75)')
        valor = str(input('Valor: R$ '))
        if ',' in valor:
            if len(valor.split(',')[-1]) <= 2:

                if len(valor.split(',')[-1]) == 1:
                    valor = valor+'0'

                valor = int(valor.replace('.', '').replace(',', ''))

                if valor == 0:
                    print('Valor nulo!')
                    return currency_input_handler()

                return valor
            
            else:
                print('Valor inválido!')
                return currency_input_handler()

        else:
            valor = int(valor.replace('.', ''))*100

            if valor == 0:
                print('Valor nulo!')
                return currency_input_handler()

            return valor

    except:
        print('Valor inválido!')
        return currency_input_handler()

#  Structural Pattern Matching
#  Menu pra seleção das operações
def menu():
    
    main_menu = """
    MENU DE OPERACAO BANCARIA - BANCO MLXN
    [c] - Consultar Saldo
    [e] - Extrato
    [d] - Depositar
    [s] - Sacar
    [q] - Sair
    - > """

    print('-'*40)
    event_get = input(main_menu)

    match event_get.lower():
        case 'c':
            print('-'*40)
            print('- > [c] - Consultar Saldo\n')
            print(conta.saldo_com_limite())
        case 'e':
            print('-'*40)
            print('- > [e] - Extrato\n')
            conta.emitir_extrato()
        case 'd':
            print('-'*40)
            print('- > [d] - Depositar\n')
            print(conta.depositar(currency_input_handler()))
        case 's':
            print('-'*40)
            print('- > [s] - Sacar\n')
            print(conta.sacar(currency_input_handler()))
        case 'q':
            print('- > [q] - Sair')
            print('\nO BANCO MLXN AGRADECE SUA PREFERÊNCIA')
            exit()
        case _:
            print('Opção inválida')

#  Inicializa a classe Banking - assume usuário autenticado e conta especificada
conta = Banking()

while True:
    menu()

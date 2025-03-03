import textwrap

def menu(): 
    menu ="""
    ================= BANCO =================
    Selecione uma opção:
    [1]\tDepositar
    [3]\tSacar
    [5]\tExtrato
    [7]\tCriar usuário
    [9]\tCriar conta 
    [11]\tListar contas
    [0]\tSair
    ================================================
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, extrato, valor, /): #Função para realizar depósitos
    
    saldo += valor
    extrato += f"(+) Depósito:\t\tR$ {valor:.2f}\n"
    print("Depósito realizado.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, numero_saques): #Função para realizar saques
    
    saldo -= valor
    extrato += f"(-) Saque:\t\tR$ {valor:.2f}\n"
    numero_saques += 1
    print("Saque realizado.")
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, /, *, extrato): #Função para exibir o extrato
    
    print("\n=========Extrato=========\n")
    if extrato == "":
        print("**Nenhuma operação realizada ainda.**\n")
        print("=====Fim do extrato=====\n")
        
    else:
        print(extrato)
        print(f"\n(=) Saldo:\t\tR$ {saldo:.2f}\n")
        print("======Fim do extrato======\n")
        return saldo, extrato

def criar_usuario(usuarios): #Função para criar um usuário
    
    cpf = input("Digite o CPF do usuário *APENAS DIGITOS*: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario: #Verifica se o usuário já está cadastrado
        print("Usuário já cadastrado.")
    
    nome = input("Digite o nome do usuário: ")
    data_nascimento = input("Digite a data de nascimento do usuário(dd/mm/aaaa): ")
    endereco = ""
    endereco += input("Endereço:\nLogradouro: ")
    endereco += input("Número: ")
    endereco += input("Bairro: ")
    endereco += input("Cidade: ")
    endereco += input("Estado(sigla): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n\n=== Usuário criado com sucesso! ===")
    return nome, cpf, usuarios

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios): #Função para criar uma conta corrente
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    else :
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas): #Função para listar as contas criadas
    
    if not contas: #Verifica se há contas cadastradas
        print("\n===**Nenhuma conta cadastrada ainda.**===\n")
        return
    
    else: 
        for conta in contas:
            linha = f"""
Agência:\t{conta['agencia']}
Cc:\t\t{conta['numero_conta']}
Titular:\t{conta['usuario']['nome']}
"""
            print("=" * 20)
            print(linha.strip())

def main():
    
    LIMITE_SAQUES = 3 #Limite de saques diários
    AGENCIA = "0001" #Agência padrão

    saldo = 0 #Saldo inicial da conta
    limite = 500 #Limite de saque
    extrato = "" 
    numero_saques = 0 #número inicial de saques diários realizados
    usuarios = [] #Lista de usuários cadastrados
    contas = [] #Lista de contas criadas

    while True: #Loop infinito até que o usuário escolha a opção de sair

        opcao = menu()
        
        if opcao == "1": #Depositar
            try: #Tratamento de exceção para valores inválidos
                valor = float(input("Digite o valor do depósito: "))
                if valor <= 0:
                    print("O valor precisa ser maior que zero. Tente novamente.")
                
                else: 
                    saldo, extrato = depositar(saldo, extrato, valor) #Chamada da função depositar SE TUDO ESTIVER CORRETO
                continue
    
            except ValueError: #Exceção para valores inválidos
                print("\n***Entrada inválida! Digite apenas números.***\n***Tente novamente.***")
                continue

        elif opcao == "3": #Sacar
        
            if numero_saques >= LIMITE_SAQUES: #Verifica o número de saques diários
                print("Não é possível realizar essa operação.\nLimite de saques diários atingido.")
            
            else:    
                
                valor = float(input("Digite o valor do saque: ")) 
                
                if valor <= 0: #Verifica se o valor é negativo ou zero
                    print("O valor precisa ser maior que zero. Tente novamente.")
            
                elif valor > limite: #Verifica se o valor do saque é maior que o limite de saque
                    print("Erro. Valor maior que o limite de saque. Tente novamente.")
                
                elif valor > saldo: #Verifica se o saldo é suficiente para o saque
                    print("Saldo insuficiente.")
                else:
                    saldo, extrato, numero_saques = sacar(
                        saldo=saldo, 
                        valor=valor, 
                        extrato=extrato, 
                        numero_saques=numero_saques,) #Chamada da função sacar SE TUDO ESTIVER CORRETO
            continue
    
        elif opcao == "5": #Extrato
            mostrar_extrato(saldo, extrato=extrato)
            continue

        elif opcao == "7": #Criar usuário
            criar_usuario(usuarios)
            continue
        
        elif opcao == "9": #Criar conta
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "11": #Listar contas
            listar_contas(contas)
            
        elif opcao == "0": #Sair
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
        
main()
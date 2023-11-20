import json

def exibir_menu(dados, primeiro_menu=True):
    # Função para exibir o menu e obter a opção do usuário

    # Imprime as opções disponíveis no menu
    print('-------------')
    cont = 0
    disponiveis = {}

    for i in dados.keys():
        item = dados[i]

        # Se o item é um dicionário, incrementa o contador e o adiciona às opções disponíveis
        if isinstance(item, dict):
            cont += 1
            disponiveis[cont] = i
            print(f'{cont}: {i}')
        # Se o item é uma lista, imprime a chave e a lista
        elif isinstance(item, list):
            print(f'{i}: {item}')
        # Se o item é outro tipo de dado, imprime a chave e o valor
        else:
            print(f'{i}: {item}')

    # Imprime as opções de sair e, se for o primeiro menu, a opção de mostrar dados
    print('-------------')
    print('0: Sair')
    if primeiro_menu:
        print('Dados: Mostrar dados de exames e datas de entregas')
    
    # Obtém a opção do usuário
    opcao = input('Escolha uma opcao: ')
    print('↓')

    try:
        opcao = int(opcao)
    except ValueError:
        # Se a opção não for um número, verifica se contém "dados" ou "Dados" para mostrar os dados
        if "dados" in opcao or "Dados" in opcao:
            mostrar_dados_finais_entregues(dados)
            print('↓')
        else:
            print('*Opcao invalida*')
            print('↓')

    return opcao, disponiveis

def navegar_dados(dados, menus_anteriores=[], primeiro_menu=True):
    # Função principal para navegar pelos dados

    while True:
        # Obtém a opção do usuário e as opções disponíveis
        opcao, disponiveis = exibir_menu(dados, primeiro_menu)
        primeiro_menu = False  # Desativa a opção dados nos menus subsequentes
    
        # Verifica a opção escolhida
        if opcao == 0:
            # Se a opção for 0, sai do programa ou volta para o menu anterior
            if not menus_anteriores:
                print('Saindo...')
                break
            else:
                dados = menus_anteriores.pop()
                continue
        elif opcao == "dados" or opcao == "Dados":
            # Se a opção for "dados" ou "Dados", mostra os dados
            pass
        else:
            # Se a opção for um número, verifica se corresponde a uma opção disponível
            token = disponiveis.get(opcao)
            if token:
                print(f'Item: {token}')
                item = dados.get(token)

                # Se o item for um dicionário, avança para o próximo nível
                if isinstance(item, dict):
                    menus_anteriores.append(dados)
                    dados = item
                # Se o item for outro tipo de dado, imprime o valor
                else:
                    print(f'Valor: {item}')
            else:
                print('*Opcao invalida*')
                print('↓')

def mostrar_dados_finais_entregues(dados):
    # Função para mostrar os dados finais de exames e entregas

    dados_finais = {"finalizado": {}, "entregue": {}, "exame": {}}
    
    def procurar_dados(item, clinica_atual):
        # Função interna para percorrer os dados e coletar as informações relevantes
        if isinstance(item, dict):
            for chave, valor in item.items():
                if chave == "IDclientes" and isinstance(valor, dict):
                    for cliente, dados_cliente in valor.items():
                        if "finalizado" in dados_cliente and isinstance(dados_cliente["finalizado"], list):
                            # Adiciona os dados de finalizado, exame e entrega (se existir) à estrutura final
                            dados_finais["finalizado"].setdefault(clinica_atual, []).append({
                                "finalizado": dados_cliente["finalizado"],
                                "exame": dados_cliente.get("exame"),
                                "entregue": dados_cliente.get("entrega")  # Corrigido para buscar "entrega"
                            })
                        procurar_dados(dados_cliente, clinica_atual)
                elif isinstance(valor, (list, dict)):
                    procurar_dados(valor, clinica_atual)
    
    # Itera sobre as clínicas e chama a função para procurar dados em cada uma
    for clinica, dados_clinica in dados.items():
        procurar_dados(dados_clinica, clinica)
    
    # Imprime os dados finais por clínica
    for chave in ["finalizado"]:
        print(f"\n{chave.capitalize()} por clínica:")
        for clinica, dados_clinica in dados_finais[chave].items():
            print(f"\n{clinica}:")
            for dado in dados_clinica:
                print(dado)

# Carrega os dados do arquivo JSON
with open('./dados.json', 'r', encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

# Inicia a navegação
navegar_dados(dados)

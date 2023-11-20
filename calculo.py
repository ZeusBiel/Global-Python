import matplotlib.pyplot as plt
import json
from datetime import datetime

with open("dadosExtraidos.json", "r", encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

datas = [
    [datetime.strptime(data, "%H:%M, %d/%m/%Y") for data in linha] for linha in dados["datas"]
]

# Calcular o tempo restante entre o segundo valor e o primeiro em cada lista
tempos_restantes = [linha[1] - linha[0] for linha in datas]

# Extrair o dia do calendário, o mês e o ano, e o tempo em minutos para cada valor em dados
info_datas = [(data[0].strftime('%d/%m'), data[0].strftime('%Y'), tempo.total_seconds() / 60) for data, tempo in zip(datas, tempos_restantes)]

# Separar as informações para facilitar o uso no gráfico
dias_do_calendario, anos, tempos_em_minutos = zip(*info_datas)

# Criar o gráfico
plt.plot(dias_do_calendario, tempos_em_minutos, marker='o')
plt.xlabel('Dia (DD/MM)')
plt.ylabel('Tempo (minutos)')
plt.title(f'Tempo de Entrega dos Exames - {anos[0]}')
plt.xticks(rotation=45, ha='right')  # Rotacionar os rótulos do eixo x para melhor legibilidade
plt.show()

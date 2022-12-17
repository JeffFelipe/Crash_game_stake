import pandas as pd
import matplotlib.pyplot as plt
import hashlib
import hmac
import numpy as np

# Semente do jogo
game_seed = '0000000000000000001b34dc6a1e86083f95500b096231436e9b25cbdd0075c4'
# Primeira hash gerada
first_game = '78a9757d3be42b74a3f70239078ad9317125fe9ee630d5bdada46de963e56752'

# Última  hash inserida pelo usuário
game_hash = '1f93980af45e9f01a6dacf9d203eb568065994fd7e2039a771dd86f6a99e36e6'  # Mude esse valor


def get_result(gamehash, seed):
    """Retorna o resultado da hash analisada no momento"""
    digest = hmac.new(bytes(gamehash, 'UTF-8'),
                      bytes(seed, 'UTF-8'), hashlib.sha256)
    signature = digest.hexdigest()
    h = int(signature[:8], 16)
    resultado_atual = 4294967296 / (h + 1) * (1 - 0.01)
    return resultado_atual


def get_prev_game(a):
    """Retorna hash anterior"""
    m = hashlib.sha256()
    m.update(a.encode("utf-8"))
    return m.hexdigest()


results = []
count = 0

while game_hash != first_game:
    count += 1
    resultado_decimal = round(get_result(game_hash, game_seed), 3)
    results.append(resultado_decimal)
    game_hash = get_prev_game(game_hash)

amostragem = list(reversed(results))  # Especifique a quantidade de dados a analisar

ordem = []
resultado = []
banca = []

crashpoint = 5  # Quanto x deseja parar
stake = 0.002  # Stake fixa
casas_para_gale = 40  # quantas vezes desejar fazer gale
nivel_gale = 1.25

stake_gale = stake


saldo_simulado = 60
banca_simulada = []


nao_ocorrencia = 0


contador = 0  # Está sendo utilizado para ser manipulado pela var ordem

ocorrencia = 0
qtd_de_ocorrencias = []
rate = []
ordem_de_ocorrencia = []
ocorrencia_salva = [0]

for i in amostragem:

    if i < crashpoint:
        contador += 1
        ordem.append(contador)  # ordem
        rate.append((ocorrencia / contador) * 100)
        nao_ocorrencia += 1

        if nao_ocorrencia > casas_para_gale:
            stake_gale = stake
            resultado.append(-stake_gale)

            saldo_simulado = round(saldo_simulado - stake_gale, 8)
            banca_simulada.append(saldo_simulado)

            nao_ocorrencia = 1
            ordem_de_ocorrencia.append(nao_ocorrencia)

        else:

            saldo_simulado = round(saldo_simulado - stake_gale, 8)
            banca_simulada.append(saldo_simulado)
            resultado.append(-stake_gale)

            stake_gale = stake_gale * nivel_gale

            ordem_de_ocorrencia.append(nao_ocorrencia)

    else:  # Se maior que crashpoint
        contador += 1
        ocorrencia += 1  # rate
        rate.append((ocorrencia / contador) * 100)

        if nao_ocorrencia == casas_para_gale:

            ordem.append(contador)  # ordem
            ocorrencia_salva.append(contador)

            ocorrencia += 1  # rate
            rate.append((ocorrencia / contador) * 100)

            stake_gale = stake
            saldo_simulado = round(saldo_simulado + ((crashpoint * stake_gale) - stake_gale), 8)

            nao_ocorrencia = 1
            ordem_de_ocorrencia.append(nao_ocorrencia)

            resultado.append((crashpoint * stake_gale) - stake)
            banca_simulada.append(saldo_simulado)

        else:

            ordem.append(contador)  # ordem

            ordem_de_ocorrencia.append(nao_ocorrencia + 1)

            resultado.append((crashpoint * stake_gale) - stake_gale)

            # buscando gale no 5x
            nao_ocorrencia = 0

            saldo_simulado = round(saldo_simulado + ((crashpoint * stake_gale) - stake_gale), 8)
            banca_simulada.append(saldo_simulado)

            stake_gale = stake


qtd_de_ocorrencias.append(ocorrencia)
media_rate = (ocorrencia / contador) * 100

df = pd.DataFrame(
    list(zip(ordem, amostragem, resultado, rate, ordem_de_ocorrencia, banca_simulada)),
    columns=['ORDEM', 'CRASHPOINT', 'RESULTADO', 'RATE', 'DIF OCORRENCIA', 'BANCA SIMULADA'])


media_diferenca_de_ocorrencia = sum(ordem_de_ocorrencia) / ocorrencia
quantidade_de_itens_com_dif_acima_da_media = len([i for i in ordem_de_ocorrencia if i > media_diferenca_de_ocorrencia])


print(f'Foram analisados {len(amostragem)} e tivemos {ocorrencia}\n ')
print(f'Média de ocorrencia de foi {round(media_rate, 4)}%\n ')
print(f'A média da diferença de ocorrência é {(sum(ordem_de_ocorrencia)) / ocorrencia}\n ')
print(f'A quantidade de itens acima da média de dif foram {quantidade_de_itens_com_dif_acima_da_media}')
print(max(amostragem))

# Gráfico
plt.title('EVOLUÇÃO DA BANCA- 5X - ENTRANDO SEMPRE')
plt.plot(list(df['ORDEM']), df['BANCA SIMULADA'])
plt.show()
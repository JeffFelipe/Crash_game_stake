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
game_hash = 'c870adbf72a66eff98959d8e759ea2d959ba6087d5078f30253dd9a86266b6e7'  # Mude esse valor


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

crashpoint = 5
stake = 0.01

# Simular Gale buscando 5x
saldo_simulado = 60
banca_simulada = []
stake_gale = 0.002
nao_ocorrencia_5x = 0
ocorrencias_5x_dif = [0]

contador = 0  # Está sendo utilizado para ser manipulado pela var ordem

ocorrencia = 0
qtd_de_ocorrencias = []
rate = []
ordem_de_ocorrencia = []
ocorrencia_salva = [0]

for i in amostragem:

    if i >= crashpoint:

        if nao_ocorrencia_5x > 40:
            contador += 1
            stake_gale = 0.002
            saldo_simulado = round(saldo_simulado - stake_gale, 4)

            nao_ocorrencia_5x = 0
            banca_simulada.append(saldo_simulado)
        else:
            contador += 1
            ordem.append(contador)  # ordem

            ocorrencia_salva.append(contador)
            diferenca_do_ultimo_aparecimento = contador - ocorrencia_salva[-2]
            ordem_de_ocorrencia.append(diferenca_do_ultimo_aparecimento)

            resultado.append((crashpoint * stake) - stake)
            # saldo = round(saldo + ((crashpoint * stake) - stake), 2)
            # banca.append(saldo)

            ocorrencia += 1  # rate
            rate.append((ocorrencia / contador) * 100)

            # buscando gale no 5x

            ocorrencias_5x_dif.append(nao_ocorrencia_5x)
            ocorrencia_5x = nao_ocorrencia_5x - ocorrencias_5x_dif[-2]
            ocorrencias_5x_dif.append(ocorrencia_5x)
            nao_ocorrencia_5x = 0

            saldo_simulado = round(saldo_simulado + ((crashpoint * stake_gale) - stake_gale), 2)
            stake_gale = 0.002
            banca_simulada.append(saldo_simulado)

    else:
        contador += 1
        ordem.append(contador)  # ordem
        ordem_de_ocorrencia.append(0)

        resultado.append(-stake)
        rate.append((ocorrencia / contador) * 100)

        if nao_ocorrencia_5x > 40:

            stake_gale = 0.002
            saldo_simulado = round(saldo_simulado - stake_gale, 4)
            nao_ocorrencia_5x = 0
            banca_simulada.append(saldo_simulado)

        else:
            nao_ocorrencia_5x += 1
            ocorrencias_5x_dif.append(nao_ocorrencia_5x)

            saldo_simulado = round(saldo_simulado - stake_gale, 4)
            stake_gale = stake_gale * 1.25
            banca_simulada.append(saldo_simulado)

qtd_de_ocorrencias.append(ocorrencia)
media_rate = (ocorrencia / contador) * 100

df = pd.DataFrame(
    list(zip(ordem, amostragem, resultado, rate, ordem_de_ocorrencia, banca_simulada)),
    columns=['ORDEM', 'CRASHPOINT', 'RESULTADO', 'RATE', 'DIF OCORRENCIA', 'BANCA SIMULADA'])

# df1 = pd.DataFrame(list(zip(ordem)))

media_diferenca_de_ocorrencia = sum(ordem_de_ocorrencia) / ocorrencia
quantidade_de_itens_com_dif_acima_da_media = len([i for i in ordem_de_ocorrencia if i > media_diferenca_de_ocorrencia])


print(f'Foram analisados {len(amostragem)} e tivemos {ocorrencia}\n ')
print(f'Média de ocorrencia de foi {round(media_rate, 4)}%\n ')
print(f'A média da diferença de ocorrência é {(sum(ordem_de_ocorrencia)) / ocorrencia}\n ')
print(f'A quantidade de itens acima da média de dif foram {quantidade_de_itens_com_dif_acima_da_media}')

# Gráfico
plt.title('EVOLUÇÃO DA BANCA- 5X - ENTRANDO SEMPRE')
plt.plot(list(df['ORDEM']), df['BANCA SIMULADA'])
plt.show()


# Análise probabilística


def analise_probabilidades():
    negatives = []
    in_a_row = 0
    for item in results:
        if item < crashpoint:
            in_a_row += 1
        else:
            in_a_row = 0
        negatives.append(in_a_row)
    negatives = np.array(negatives)

    for i in range(1, 41):
        print(f'Probabilidade de perder {i} jogo(s) consecutivos: {round(((negatives >= i).mean()) * 100, 3)} %')


analise_probabilidades()

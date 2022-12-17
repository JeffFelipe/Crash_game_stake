import requests
from requests import ReadTimeout
import json
from json import JSONDecodeError
import time


def requisitar_resultados(api):
    """Essa função é responsável por extrair o último resultado finalizado e registrado. O índice 0 de objeto é
     justamente o que define o último resultado"""

    cookies = {
        'currency_cryptoCurrencies': '["btc","eth","ltc","usdt"]',
        'currency_currencyView': 'crypto',
        'sportsSearch': '["Liverpool FC","Kansas City Chiefs","Los Angeles Lakers","FC Barcelona","FC Bayern Munich"]',
        'oddsFormat': 'decimal',
        'sportMarketGroupMap': '{}',
        'locale': 'pt',
        '_ga': 'GA1.2.396580709.1665922915',
        'intercom-id-cx1ywgf2': '24c0087d-1fac-4bfc-a647-df2f46bfbeec',
        'currency_bankingCurrencies': '["brl"]',
        'cookie_consent': 'true',
        '_gid': 'GA1.2.2089233544.1668862975',
        'intercom-device-id-cx1ywgf2': '9703147f-52db-4573-a9b8-4d739a0da411',
        'session': f'{api}',
        'currency_currency': 'usdt',
        'sidebarView': 'hidden',
        'currency_hideZeroBalances': 'true',
        'leftSidebarView_v2': 'expanded',
        'cf_clearance': 'kh_eprz6biINqjzZBw6cAylBiPcYmMRY4c0mJBKyyWc-1671008561-0-160',
        'mp_e29e8d653fb046aa5a7d7b151ecf6f99_mixpanel': '%7B%22distinct_id%22%3A%20%22710fa01e4608bcef5eebca75128efdcc7e717c167f5344229dc8c15defbbc8cc%22%2C%22%24device_id%22%3A%20%22183e0be5c0c50b-04523d28da47cf-26021f51-1fa400-183e0be5c0d902%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fstake.com%2F%3F__cf_chl_tk%3DvnJWXfiD7meFnpV9xc74d7L.VlqH7lKnoLVCqHyk5_M-1665922908-0-gaNycGzNCJE%22%2C%22%24initial_referring_domain%22%3A%20%22stake.com%22%2C%22%24user_id%22%3A%20%22710fa01e4608bcef5eebca75128efdcc7e717c167f5344229dc8c15defbbc8cc%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24search_engine%22%3A%20%22google%22%7D',
        '_gat_UA-102002770-1': '1',
        '__cf_bm': 'qsxQ95bb0M_xXZbw2qlM1liBFwVizdcP5BROfF40.Uw-1671019856-0-AYzZ+RF9D3JKWnuRDE8HfS/Gp8la8SmyaPeeJAnOneGPPK/WKu5g24oFFx5Sg6t3DzgFEY4MS7f/r+R1dPuN1XDRFEoxsL6ab+DsoMALHamXsM5VXHBxKkGEhBSbjLCJoiq/pQquT2FnWKKGLUrQp2EyOfGPkTtJlUd1av0DMtHLXLo15BQoxNQO6uKAzdkwzA==',
        '_sp_srt_ses.2cca': '*',
        'intercom-session-cx1ywgf2': 'WmJXa3JTZDlhVmFkWENrZDRjcXo2VXd0djdYWVdZMFloelZpeVNiTjk0QzVkZEhXU0NJbHZNZTBSa29iRmV3bS0tQmx5VG1xdE02Z2NIbVBKRzBRcXdqdz09--49e448a9aa16b7da783a0744edf73ff486457886',
        '_sp_srt_id.2cca': 'f24cad6d-1858-4fc3-b37b-d6ad08775fb8.1670281841.60.1671019858.1671008567.bf76b0de-c74d-42fd-91c7-0672e3d6139d',
    }

    headers = {
        'authority': 'stake.com',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cf-device-type': '',
        'content-type': 'application/json',
        'origin': 'https://stake.com',
        'referer': 'https://stake.com/casino/games/crash',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-access-token': f'{api}',
        'x-geoip-country': 'BR',
        'x-geoip-state': 'BR-CE',
        'x-language': 'pt',
        'x-lockdown-token': 's5MNWtjTM5TvCMkAzxov',
    }

    json_data = {
        'query': 'query CrashGameListHistory($limit: Int, $offset: Int) {\n  crashGameList(limit: $limit, offset: $offset) {\n    id\n    startTime\n    crashpoint\n    hash {\n      id\n      hash\n      __typename\n    }\n    __typename\n  }\n}\n',
        'operationName': 'CrashGameListHistory',
        'variables': {},
    }

    try:
        response = requests.post('https://stake.com/_api/graphql', cookies=cookies, headers=headers, json=json_data)
        objeto = json.loads(response.text)

        return objeto['data']['crashGameList'][0]['crashpoint']

    except ValueError:
        time.sleep(1)
        response = requests.post('https://stake.com/_api/graphql', cookies=cookies, headers=headers, json=json_data)

        objeto = json.loads(response.text)

        return objeto['data']['crashGameList'][0]['crashpoint']

    except ReadTimeout:
        time.sleep(1)
        response = requests.post('https://stake.com/_api/graphql', cookies=cookies, headers=headers, json=json_data)

        objeto = json.loads(response.text)

        return objeto['data']['crashGameList'][0]['crashpoint']


def requisitar_saldo(api):
    """ Essa função puxa o saldo, ela será responsável para a lógica de vitória ou perda. Se após um novo resultado
     apurado, o saldo for menor que o inicial, então sabemos que foi uma rodada perdida. Se o saldo for maior, então foi
     uma rodada de sucesso"""
    cookies = {
        'currency_cryptoCurrencies': '["btc","eth","ltc","usdt"]',
        'currency_currencyView': 'crypto',
        'sportsSearch': '["Liverpool FC","Kansas City Chiefs","Los Angeles Lakers","FC Barcelona","FC Bayern Munich"]',
        'oddsFormat': 'decimal',
        'sportMarketGroupMap': '{}',
        'locale': 'pt',
        '_ga': 'GA1.2.396580709.1665922915',
        'intercom-id-cx1ywgf2': '24c0087d-1fac-4bfc-a647-df2f46bfbeec',
        'currency_bankingCurrencies': '["brl"]',
        'cookie_consent': 'true',
        '_gid': 'GA1.2.2089233544.1668862975',
        'intercom-device-id-cx1ywgf2': '9703147f-52db-4573-a9b8-4d739a0da411',
        'session': f'{api}',
        'currency_currency': 'usdt',
        'sidebarView': 'hidden',
        'currency_hideZeroBalances': 'true',
        'leftSidebarView_v2': 'expanded',
        'cf_clearance': 'kh_eprz6biINqjzZBw6cAylBiPcYmMRY4c0mJBKyyWc-1671008561-0-160',
        'mp_e29e8d653fb046aa5a7d7b151ecf6f99_mixpanel': '%7B%22distinct_id%22%3A%20%22710fa01e4608bcef5eebca75128efdcc7e717c167f5344229dc8c15defbbc8cc%22%2C%22%24device_id%22%3A%20%22183e0be5c0c50b-04523d28da47cf-26021f51-1fa400-183e0be5c0d902%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fstake.com%2F%3F__cf_chl_tk%3DvnJWXfiD7meFnpV9xc74d7L.VlqH7lKnoLVCqHyk5_M-1665922908-0-gaNycGzNCJE%22%2C%22%24initial_referring_domain%22%3A%20%22stake.com%22%2C%22%24user_id%22%3A%20%22710fa01e4608bcef5eebca75128efdcc7e717c167f5344229dc8c15defbbc8cc%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24search_engine%22%3A%20%22google%22%7D',
        '_gat_UA-102002770-1': '1',
        '__cf_bm': 'qsxQ95bb0M_xXZbw2qlM1liBFwVizdcP5BROfF40.Uw-1671019856-0-AYzZ+RF9D3JKWnuRDE8HfS/Gp8la8SmyaPeeJAnOneGPPK/WKu5g24oFFx5Sg6t3DzgFEY4MS7f/r+R1dPuN1XDRFEoxsL6ab+DsoMALHamXsM5VXHBxKkGEhBSbjLCJoiq/pQquT2FnWKKGLUrQp2EyOfGPkTtJlUd1av0DMtHLXLo15BQoxNQO6uKAzdkwzA==',
        '_sp_srt_ses.2cca': '*',
        'intercom-session-cx1ywgf2': 'WmJXa3JTZDlhVmFkWENrZDRjcXo2VXd0djdYWVdZMFloelZpeVNiTjk0QzVkZEhXU0NJbHZNZTBSa29iRmV3bS0tQmx5VG1xdE02Z2NIbVBKRzBRcXdqdz09--49e448a9aa16b7da783a0744edf73ff486457886',
        '_sp_srt_id.2cca': 'f24cad6d-1858-4fc3-b37b-d6ad08775fb8.1670281841.60.1671019858.1671008567.bf76b0de-c74d-42fd-91c7-0672e3d6139d',
    }

    headers = {
        'authority': 'stake.com',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cf-device-type': '',
        'content-type': 'application/json',
        'origin': 'https://stake.com',
        'referer': 'https://stake.com/casino/games/crash',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-access-token': f'{api}',
        'x-geoip-country': 'BR',
        'x-geoip-state': 'BR-CE',
        'x-language': 'pt',
        'x-lockdown-token': 's5MNWtjTM5TvCMkAzxov',
    }

    json_data = {
        'query': 'query UserBalances {\n  user {\n    id\n    balances {\n      available {\n        amount\n        '
                 'currency\n        __typename\n      }\n      vault {\n        amount\n        currency\n        '
                 '__typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
        'operationName': 'UserBalances',
    }

    try:
        response = requests.post('https://stake.com/_api/graphql', cookies=cookies, headers=headers, json=json_data)
        objeto = json.loads(response.text)
        return objeto['data']['user']['balances'][-2]['available']['amount']

    except ValueError:
        time.sleep(2)
        response = requests.post('https://stake.com/_api/graphql', cookies=cookies, headers=headers, json=json_data)
        objeto = json.loads(response.text)
        return objeto['data']['user']['balances'][-2]['available']['amount']


def aposta(amount_, cashout_, api):
    """Essa função busca fazer a aposta, após a mudança de resultado e considerando os devidos parâmetros.
    Ela necessita ser forçada, pois há uma delay entre o tmepo qeu permite apostar e a api. """
    cookies = {
        'currency_cryptoCurrencies': '["btc","eth","ltc","usdt"]',
        'currency_currencyView': 'crypto',
        'sportsSearch': '["Liverpool FC","Kansas City Chiefs","Los Angeles Lakers","FC Barcelona","FC Bayern Munich"]',
        'oddsFormat': 'decimal',
        'sportMarketGroupMap': '{}',
        'locale': 'pt',
        '_ga': 'GA1.2.396580709.1665922915',
        'intercom-id-cx1ywgf2': '24c0087d-1fac-4bfc-a647-df2f46bfbeec',
        'currency_bankingCurrencies': '["brl"]',
        'cookie_consent': 'true',
        '_gid': 'GA1.2.2089233544.1668862975',
        'intercom-device-id-cx1ywgf2': '9703147f-52db-4573-a9b8-4d739a0da411',
        'session': f'{api}',
        'currency_currency': 'usdt',
        'sidebarView': 'hidden',
        'currency_hideZeroBalances': 'true',
        'leftSidebarView_v2': 'expanded',
        'cf_clearance': 'kh_eprz6biINqjzZBw6cAylBiPcYmMRY4c0mJBKyyWc-1671008561-0-160',
        'mp_e29e8d653fb046aa5a7d7b151ecf6f99_mixpanel': '%7B%22distinct_id%22%3A%20%22710fa01e4608bcef5eebca75128efdcc7e717c167f5344229dc8c15defbbc8cc%22%2C%22%24device_id%22%3A%20%22183e0be5c0c50b-04523d28da47cf-26021f51-1fa400-183e0be5c0d902%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fstake.com%2F%3F__cf_chl_tk%3DvnJWXfiD7meFnpV9xc74d7L.VlqH7lKnoLVCqHyk5_M-1665922908-0-gaNycGzNCJE%22%2C%22%24initial_referring_domain%22%3A%20%22stake.com%22%2C%22%24user_id%22%3A%20%22710fa01e4608bcef5eebca75128efdcc7e717c167f5344229dc8c15defbbc8cc%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24search_engine%22%3A%20%22google%22%7D',
        '_gat_UA-102002770-1': '1',
        '__cf_bm': 'qsxQ95bb0M_xXZbw2qlM1liBFwVizdcP5BROfF40.Uw-1671019856-0-AYzZ+RF9D3JKWnuRDE8HfS/Gp8la8SmyaPeeJAnOneGPPK/WKu5g24oFFx5Sg6t3DzgFEY4MS7f/r+R1dPuN1XDRFEoxsL6ab+DsoMALHamXsM5VXHBxKkGEhBSbjLCJoiq/pQquT2FnWKKGLUrQp2EyOfGPkTtJlUd1av0DMtHLXLo15BQoxNQO6uKAzdkwzA==',
        '_sp_srt_ses.2cca': '*',
        'intercom-session-cx1ywgf2': 'WmJXa3JTZDlhVmFkWENrZDRjcXo2VXd0djdYWVdZMFloelZpeVNiTjk0QzVkZEhXU0NJbHZNZTBSa29iRmV3bS0tQmx5VG1xdE02Z2NIbVBKRzBRcXdqdz09--49e448a9aa16b7da783a0744edf73ff486457886',
        '_sp_srt_id.2cca': 'f24cad6d-1858-4fc3-b37b-d6ad08775fb8.1670281841.60.1671019858.1671008567.bf76b0de-c74d-42fd-91c7-0672e3d6139d',
    }

    headers = {
        'authority': 'stake.com',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cf-device-type': '',
        'content-type': 'application/json',
        'origin': 'https://stake.com',
        'referer': 'https://stake.com/casino/games/crash',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-access-token': f'{api}',
        'x-geoip-country': 'BR',
        'x-geoip-state': 'BR-CE',
        'x-language': 'pt',
        'x-lockdown-token': 's5MNWtjTM5TvCMkAzxov',
    }

    json_data_aposta = {
        'query': 'mutation MultiplayerCrashBet($amount: Float!, $currency: CurrencyEnum!, $cashoutAt: Float!) {\n  '
                 'multiplayerCrashBet(amount: $amount, currency: $currency, cashoutAt: $cashoutAt) {\n    '
                 '...MultiplayerCrashBet\n    user {\n      id\n      activeCrashBet {\n        '
                 '...MultiplayerCrashBet\n      }\n    }\n  }\n}\n\nfragment MultiplayerCrashBet on '
                 'MultiplayerCrashBet {\n  id\n  user {\n    id\n    name\n  }\n  payoutMultiplier\n  gameId\n  '
                 'amount\n  payout\n  currency\n  result\n  updatedAt\n  cashoutAt\n  btcAmount: amount(currency: '
                 'btc)\n}\n',
        'variables': {
            'amount': amount_,
            'currency': 'usdt',
            'cashoutAt': cashout_,
        },
    }

    response = requests.post('https://stake.com/_api/graphql', cookies=cookies, headers=headers, json=json_data_aposta)

    resposta = json.loads(response.text)

    return resposta


def forcar_aposta(a, b, c):
    """Enquanto não apostar, execute a função apostar"""
    while True:
        if 'errors' in aposta(a, b):
            print('Tentando apostar')
            time.sleep(2)
        else:
            print(f'Aposta de {c} realizada!')
            break


amount_fixo = 0.002  # O usuário deve alterar somente este valor, pois ele será imutável
api_stake = ''  # MUITO CUIDADO COM ESSA INFORMAÇÃO!

amount = 0.00045
cashout = 5
casas_gale = 42  # defina um valor um inteiro superior em 1 a sua estimativa
porcentagem_de_gale = 0.30  # defina quantos porcentos deve subir após uma derrota


contador_de_rodada = 0
resultado_anterior = requisitar_resultados(api_stake)
saldo_anterior = requisitar_saldo(api_stake)

print('Iniciando bot')
print(f'Saldo atual {saldo_anterior} USDT')
print(f'Resultado do jogo anterior {resultado_anterior}')

saldo_inicio_ciclo = saldo_anterior


def rodar_bot():
    global resultado_anterior, saldo_anterior, contador_de_rodada, amount
    ciclo = 0  # isso irá definir um marcador de cilos, para evitar que o bot trave, pois a api o limita

    while ciclo < 200:  # Esse looping é o que define que o bot não pare

        resultado_atual = requisitar_resultados(api_stake)

        if resultado_anterior != resultado_atual:  # Se for diferente, então mudou a rodada

            saldo_atual = requisitar_saldo(api_stake)

            if saldo_atual != saldo_anterior:  # Se for diferente, significa que apostou na rodada anterior.

                if saldo_atual > saldo_anterior:
                    print('Rodada ganha!, Reiniciando parâmetros')
                    # Na vitória, reinicia os parâmetros e inicia a rodada 1

                    amount = amount_fixo
                    time.sleep(2)

                    # Faça a aposta inicial
                    try:
                        forcar_aposta(amount, cashout, amount)
                    except JSONDecodeError:
                        time.sleep(1)
                        forcar_aposta(amount, cashout, amount)

                    contador_de_rodada = 1

                    print(f'------------------------------------------------------------\n'
                          f'Rodada {contador_de_rodada}.')
                    ciclo += 1

                if saldo_atual < saldo_anterior:
                    print('Rodada perdida!')

                    if contador_de_rodada < casas_gale:  # Até 40 rodadas, deve fazer o abaixo
                        """  # Se estivesse anteriormente na rodada 40, isso irá fazer com que a próxima rodada
                        seja a de número 41, forçando o else abaixo"""
                        contador_de_rodada += 1
                        amount = amount + (amount * porcentagem_de_gale)

                        try:
                            forcar_aposta(amount, cashout, amount)
                        except JSONDecodeError:
                            time.sleep(1)
                            forcar_aposta(amount, cashout, amount)

                        print(f'------------------------------------------------------------\n'
                              f'Rodada {contador_de_rodada}.')

                    if contador_de_rodada > (casas_gale - 1):
                        # Rodada 41, quebra a abanca e reinicia os parâmetros
                        amount = amount_fixo

                        try:
                            forcar_aposta(amount, cashout, amount)
                        except JSONDecodeError:
                            time.sleep(1)
                            forcar_aposta(amount, cashout, amount)

                        contador_de_rodada = 1

                        print(f'QUEBROU A BANCA!\n SALDO ATUAL: {requisitar_saldo(api_stake)}')

                        print(f'------------------------------------------------------------\n'
                              f'Rodada {contador_de_rodada}.')

            else:  # Se o saldo não mudou, então essa é a primeira rodada

                amount = amount_fixo

                try:
                    forcar_aposta(amount, cashout, amount)
                except JSONDecodeError:
                    time.sleep(1)
                    forcar_aposta(amount, cashout, amount)

                contador_de_rodada = 1

                print(f'------------------------------------------------------------\n'
                      f'Iniciando a rodada {contador_de_rodada}.')

            saldo_anterior = saldo_atual

            print(f'------------------------------------------------------------\n'
                  f'ROI = {round((saldo_atual - saldo_inicio_ciclo), 9)} USDT\n'
                  f'------------------------------------------------------------\n')  # Esse round é por pura estética,
            # assim fica com valor idêntico ao da Stake

        resultado_anterior = float(resultado_atual)
        time.sleep(2)


while True:
    rodar_bot()
    time.sleep(60000)
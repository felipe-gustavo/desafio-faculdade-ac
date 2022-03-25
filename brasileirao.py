from audioop import reverse
import json

'''
Nessa atividade, vamos usar dados do campeonato brasileiro 2018
(brasileirão) para estudar como acessar listas, dicionários,
e estruturas encadeadas (listas dentro de dicionários dentro de listas).

Os dados estão fornecidos em um arquivo (ano2018.json) que você
pode abrir no Firefox, para tentar entender melhor.

Para rodar isso daqui, o arquivo de teste brasileirao_teste.py que
acompanha deve ser executado. É ele que vai testar as funções desenvolvidas
abaixo e dizer se parece estar tudo ok ou não. Há 20 testes lá, cada um deles
vale 0,5 pontos na nota do AC.

Se quiser ver os dados dentro do python, pode chamar a função
pega_dados que está no brasileirao_teste.py.

O que deve ser entregue é apenas este arquivo, com todas as modificações
necessárias para o sucesso dos exercícios. Os arquivos ano2018.json e
brasileirao_teste.py não devem ser alterados e nem entregues.
'''

'''
Primeiramente, altere esta função para que a mesma retorne o seu nome.
'''


def nome_do_aluno():
    codes = [
        "46", "45", "4c", "49", "50", "45", "20",
        "47", "55", "53", "54", "41", "56", "4f"
    ]
    name = [chr(int("0x" + code, base=16)) for code in codes]
    return "".join(name)


'''
********** HELPER AND CONSTS: **********

Aqui contém as constantes e funções de auxílio do exercício
'''
PHASE = '2700'
GROUP = 'Único'


def isInteractiveOkbject(obj):
    ''' Check if an object is interactive, like an list, tuple or dictionary '''

    objType = type(obj)
    return (
        objType is dict or
        objType is list or
        objType is tuple
    )


def get(dto, path):
    '''
    Get a value from depth object by an path like:
    ```
    get({"a": 1}, "a") # will returns 1
    get({"a": {"b": 2}}, "a.b") # will returns 2
    ```
    '''

    if (not isInteractiveOkbject(dto)):
        raise TypeError(
            "The value passed to dto param must be an interactive object, like and dictionary, list or tuple!"
        )

    key, *rest = path if (type(path) is list) else path.split('.')

    value = dto[key]
    if (len(rest) > 0 and isInteractiveOkbject(value)):
        return get(value, rest)

    return value


def getGames(dto):
    '''
    Get all games from the `dto`
    '''

    key = "fases.{}.jogos.id".format(PHASE)
    return get(dto, key)


def getGamesByCustomLambda(dto, fn):
    '''
    Filter the games from the `dto` by an custom lambda function like
    ```
    getGamesByCustomLambda(dto, lambda game, id: id == 1)
     # will return all games that the id is 1
    ```
    '''

    games = getGames(dto)
    return [
        {"id": gameId, **games[gameId]}
        for gameId in games
        if (fn(games[gameId], gameId))
    ]


def getGameById(dto, id):
    '''
    Get a game by id, i not exists return False
    '''

    try:
        return getGamesByCustomLambda(dto, lambda _, gameId: gameId == id)[0]
    except:
        return False


def getTeamsByCustomLambda(dto, fn):
    '''
    Filter all teams from the `dto` by an lamda function, like:
    ```
    getTeamsByCustomLambda(dto, lambda team, id: id == 1)
     # will return all teams that the id is 1
    ```
    '''

    teams = get(dto, "equipes")
    return [
        teams[teamId]
        for teamId in teams
        if (fn(teams[teamId], teamId))
    ]


def getTeamsByCustomAttr(dto, attr, value):
    '''
    Filter all teams that match with `attr` and `value` params, like:
    ```
    getTeamsByCustomAttr(dto, "id", 1)
     # will return all teams that the id is 1
    '''

    return getTeamsByCustomLambda(dto, lambda team, _: team[attr] == value)


def getTotalGoalsByTeam(dto, teamId):
    '''
    Get the total goals made by a team
    '''
    scores = [
        int(game["placar1"] if (game["time1"] == teamId) else game["placar2"])
        for game in getGamesByCustomLambda(dto, lambda game, _: (
            game["time1"] == teamId or game["time2"] == teamId
        ))
    ]

    return sum(scores)


def getStadiums(dto):
    '''
    Get all Statiums as list populed for the follow object with all stadiums:
    ```
    { id: "1", name: "some-name" }
    ```
    '''

    stadiums = []

    for game in list(getGames(dto).values()):
        alreadyDone = len([
            1
            for stadium in stadiums
            if (stadium['id'] == game['estadio_id'])
        ])
        if (alreadyDone == 0):
            stadiums.append(
                {"id": game['estadio_id'], "name": game['estadio']}
            )

    return stadiums


def getTeamsClassification(dto):
    '''
    Get an list that contains the teams classification positions
    '''

    key = "fases.{}.classificacao.grupo.{}".format(PHASE, GROUP)
    return get(dto, key)


def getTeamsClassificationByCustomLambda(dto, fn):
    '''
    Filter the teams on classification by the lambda received and return your current position as a key, like bellow example:
    ```
    getTeamsClassificationByCustomLambda(
        dto,
        lambda teamId, pos: pos >= 3
    ) # Will return all teams that be above the 3rd position { 1: "x", 2: "y", 3: "z" }
    ```
    '''

    teamsClassification = getTeamsClassification(dto)
    teams = {}

    for i in list(range(len(teamsClassification))):
        if (fn(teamsClassification[i], i + 1)):
            teams[i+1] = teamsClassification[i]

    return teams


'''
********** EXERCÍCIO 1: **********

Crie uma função datas_de_jogo, que procura nos dados do brasileirão
e devolve uma lista de todas as datas em que houve jogo.

As datas devem ter o mesmo formato que tinham nos dados do brasileirão.

dica: busque em dados['fases']

Observe que essa função (e todas as demais!) recebem os dados dos
jogos numa variável dados. Essa variável contém todas as informações do
arquivo JSON que acompanha essa atividade.
'''


def datas_de_jogo(dados):
    key = 'fases.{}.jogos.data'.format(PHASE)
    return get(dados, key).keys()


'''
********** EXERCÍCIO 2: **********

Crie uma função data_de_um_jogo, que recebe a id numérica de um jogo
e devolve a data em que ele ocorreu.

Se essa não for uma id válida, você deve devolver a string 'nao encontrado'.
Cuidado! Se você devolver uma string ligeiramente diferente, o teste
vai falhar.

Você provavelmente vai querer testar sua função no braço e não
somente fazer os meus testes. Para isso, note que muitos números
nesse arquivo estão representados não como números, mas sim como strings.
'''


def data_de_um_jogo(dados, id_jogo):
    game = getGameById(dados, id_jogo)
    if (game != False):
        return game['data']

    return "nao encontrado"


'''
********** EXERCÍCIO 3: **********

Nos nossos dados, cada time tem um id e uma identificação numérica.
(você pode consultar as identificações numéricas em dados['equipes']).

Essas id também aparecem nos jogos. (onde? dê uma procurada!)

Desenvolva a próxima função que recebe a id numérica de um jogo, e devolve as
ids numéricas dos dois times envolvidos.

Vou deixar um código para você lembrar como retornar duas ids em um único return.

def ids_dos_times_de_um_jogo(dados, id_jogo):
    time1 = 12
    time2 = 13
    # Assim a gente retorna as duas respostas em um único return.
    return time1, time2
'''


def ids_dos_times_de_um_jogo(dados, id_jogo):
    game = getGameById(dados, id_jogo)
    return (game["time1"], game["time2"])


'''
********** EXERCÍCIO 4: **********

Desenvolva a função que recebe a id_numerica de um time e retorna seu 'nome-comum'.
'''


def nome_do_time(dados, id_time):
    team, *_ = getTeamsByCustomAttr(dados, "id", id_time)
    return team['nome-comum']


'''
********** EXERCÍCIO 5: **********

Desenvolva a função que "cruza" as duas anteriores. Recebe uma id de um jogo
e retorna os "nome-comum" dos dois times.
'''


def nomes_dos_times_de_um_jogo(dados, id_jogo):
    team1, team2 = ids_dos_times_de_um_jogo(dados, id_jogo)
    return (
        nome_do_time(dados, team1),
        nome_do_time(dados, team2)
    )


'''
********** EXERCÍCIO 6: **********

Desenvolva a função que faça a busca "ao contrário".
Conhecendo o nome-comum de um time, queremos saber sua id.

Se o nome comum não existir, retorne 'nao encontrado'.
'''


def id_do_time(dados, nome_time):
    team, *_ = getTeamsByCustomAttr(dados, "nome-comum", nome_time)
    return team["id"]


'''
********** EXERCÍCIO 7: **********

Agora, desenvolva a função que faça uma busca "fuzzy".
Queremos procurar por 'Fla' e achar o Flamengo. Ou por 'Paulo' e achar o São Paulo.

Nessa busca, você recebe um nome, e verifica os campos 'nome-comum', 'nome-slug',
'sigla' e 'nome', tomando o cuidado de aceitar times se a string buscada aparece
dentro do nome (A string "Paulo" aparece dentro de "São Paulo").

Sua resposta deve ser uma lista de ids de times que "batem" com a pesquisa
(e pode ser vazia, se não achar ninguém).
'''


def busca_imprecisa_por_nome_de_time(dados, nome_time):
    def lookUpForCommonName(team, _): return nome_time in team['nome-comum']

    def lookUpForSku(team, _): return nome_time in team['nome-slug']

    def lookUpForAcronym(team, _): return nome_time in team['sigla']

    def lookUpForName(team, _): return nome_time in team['nome']

    def lookUpTeam(team, id): return (
        lookUpForCommonName(team, id) or
        lookUpForSku(team, id) or
        lookUpForAcronym(team, id) or
        lookUpForName(team, id)
    )

    return [
        team["id"]
        for team in getTeamsByCustomLambda(dados, lookUpTeam)
    ]


'''
********** EXERCÍCIO 8: **********

Desenvolva a função que recebe a id de um time e retorne as ids de todos
os jogos em que esse time participou.
'''


def ids_de_jogos_de_um_time(dados, time_id):
    return [
        game["id"]
        for game in getGamesByCustomLambda(
            dados,
            lambda game, _: (
                game['time1'] == time_id or
                game['time2'] == time_id
            )
        )
    ]


'''
********** EXERCÍCIO 9: **********

Usando as ids dos jogos em que um time participou, desenvolva a função que
descobre em que dias ele jogou.

Note que essa função recebe o nome-comum do time, não sua id.

Ela retorna uma lista das datas em que o time jogou.
'''


def datas_de_jogos_de_um_time(dados, nome_time):
    team, *_ = getTeamsByCustomAttr(dados, "nome-comum", nome_time)

    return [
        game["data"]
        for game in getGamesByCustomLambda(
            dados,
            lambda game, _: (
                game['time1'] == team['id'] or
                game['time2'] == team['id']
            )
        )
    ]


'''
********** EXERCÍCIO 10: **********

Desenvolva a função que recebe apenas o dicionário dos dados do brasileirão
e devolve um dicionário com quantos gols cada time fez.
'''


def dicionario_de_gols(dados):
    teamsScore = {}

    for teamId in dados['equipes']:
        teamsScore[teamId] = getTotalGoalsByTeam(dados, teamId)

    return teamsScore


'''
********** EXERCÍCIO 11: **********

Desenvolva a função que recebe apenas o dicionário dos dados do brasileirão
e devolve a id do time que fez mais gols no campeonato.
'''


def time_que_fez_mais_gols(dados):
    scores = dicionario_de_gols(dados)

    scoresList = list(scores.values())
    scoresList.sort(reverse=True)

    greaterScore = scoresList[0]
    teamId, *_ = [
        teamId
        for teamId in scores.keys()
        if (greaterScore == scores[teamId])
    ]

    return teamId


'''
********** EXERCÍCIO 12: **********

Desenvolva a função que recebe apenas o dicionário dos dados do brasileirão
e devolve um dicionário que conta, para cada estádio, quantas vezes ocorreu um jogo nele.

Ou seja, as chaves são ids de estádios e os valores são o número
de vezes que um jogo ocorreu no estádio.
'''


def dicionario_id_estadio_e_nro_jogos(dados):
    stadiums = getStadiums(dados)
    stadiumsDash = {}
    print(stadiums)
    for stadium in stadiums:
        stadiumsDash[stadium['id']] = len(
            getGamesByCustomLambda(
                dados,
                lambda game, _: game['estadio_id'] == stadium['id']
            )
        )

    return stadiumsDash


'''
********** EXERCÍCIO 13: **********

Desenvolva a função que recebe apenas o dicionário dos dados do brasileirão
e devolve o número de times que o brasileirão qualifica para a libertadores.

Note que esse número está nos dados do parâmetro. Você deve pegar o número
a partir dos dados. Não basta retornar o valor correto, tem que acessar os dados
fornecidos.

Consulte a parte de faixas de times no dicionário.
'''


def qtos_libertadores(dados):
    key = "fases.{}.faixas-classificacao.classifica1.faixa".format(PHASE)
    rangeClassify = get(dados, key)
    _, lastPos = rangeClassify.split("-")

    return int(lastPos)


'''
********** EXERCÍCIO 14: **********

Desenvolva a função que recebe um tamanho e retorna uma lista
com len(lista) == tamanho, com as ids dos times melhor classificados.

Por exemplo, ids_dos_melhor_classificados(dados, 6) tem que trazer as ids
dos 6 times melhor classificados.
'''


def ids_dos_melhor_classificados(dados, numero):
    key = "fases.{}.classificacao.grupo.{}".format(PHASE, GROUP)
    teamsClassified = get(dados, key)

    return teamsClassified[:numero]


'''
********** EXERCÍCIO 15: **********

Usando as duas funções anteriores, deselvolva uma outra função que retorne uma
lista de todos os times classificados para a libertadores em virtude do
campeonato brasileiro.

Lembre-se de consultar a estrutura, tanto para obter a classificação, quanto
para obter o número correto de times a retornar.
'''


def classificados_libertadores(dados):
    return ids_dos_melhor_classificados(dados, qtos_libertadores(dados))


'''
********** EXERCÍCIO 16: **********

Da mesma forma que podemos obter a informação dos times classificados
para a libertadores, também podemos obter os times na zona de rebaixamento.

Desenvolva a função que recebe apenas o dicionário de dados do brasileirão,
e retorna uma lista com as ids dos times rebaixados.

Consulte a zona de rebaixamento do dicionário de dados, não deixe
os valores "chumbados" na função.
'''


def rebaixados(dados):
    relegationRangeKey = "fases.{}.faixas-classificacao.classifica3.faixa".format(
        PHASE)
    relegationRange = get(dados, relegationRangeKey)
    firstPos, lastPos = relegationRange.split("-")

    return list(getTeamsClassificationByCustomLambda(
        dados,
        lambda _, pos: pos >= int(firstPos) and pos <= int(lastPos)
    ).values())


'''
********** EXERCÍCIO 17: **********

Desenvolva uma função que recebe, além do dicionário de dados do brasileirão, uma id de time.

Ela retorna a classificação desse time no campeonato.
Por exemplo, classificacao_do_time_por_id(dados, '695') devolve 14 porque o time com a id 695
é a Chapecoense, que terminou o campeonato na décima-quarta posição.

Se a id não for válida, retorna a string 'nao encontrado'.
'''


def classificacao_do_time_por_id(dados, time_id):
    try:
        teamPosition, *_ = list(getTeamsClassificationByCustomLambda(
            dados,
            lambda teamId, _: teamId == time_id
        ).keys())

        return teamPosition
    except:
        return "nao encontrado"

def salvar_ranking(nome, pontos):

    with open("ranking.txt", "a", encoding="utf-8") as arquivo:

        arquivo.write(f"{nome}:{pontos}\n")


def carregar_ranking():

    try:

        with open("ranking.txt", "r", encoding="utf-8") as arquivo:

            linhas = arquivo.readlines()

        ranking = []

        for linha in linhas:

            nome, pontos = linha.strip().split(":")

            ranking.append((nome, int(pontos)))

        ranking.sort(key=lambda x: x[1], reverse=True)

        return ranking[:5]

    except:

        return []
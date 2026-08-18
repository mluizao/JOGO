def salvar_ranking(nome, pontos):

    with open("ranking.txt", "a", encoding="utf-8") as arquivo:

        arquivo.write(f"{nome}:{pontos}\n")


def carregar_ranking():

    try:

        with open("ranking.txt", "r", encoding="utf-8") as arquivo:

            linhas = arquivo.readlines()

        ranking = []

        for linha in linhas:

            linha = linha.strip()

            if not linha:
                continue

            if ":" in linha:

                nome, pontos_str = linha.split(":", 1)

            elif "," in linha:

                nome, pontos_str = linha.split(",", 1)

            else:

                continue

            nome = nome.strip()

            try:

                pontos = int(pontos_str.strip())

            except ValueError:

                continue

            ranking.append((nome, pontos))

        ranking.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return ranking

    except FileNotFoundError:

        return []

    except Exception as e:

        print("Erro ao carregar ranking:", e)

        return []


def adicionar_pontuacao(nome, pontos):

    salvar_ranking(nome, pontos)

    return carregar_ranking()


def obter_melhores_pontuacoes(limite=10):

    ranking = carregar_ranking()

    return ranking[:limite]
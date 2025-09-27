from fitness import calcular_fitness
from model import *


def torneio_selecao(
    populacao: list[Cromossomo],
    atividades: list[Atividade],
    horas_totais: int,
    k: int = 4,
) -> Cromossomo:
    """Seleciona um cromossomo via torneio de tamanho k."""
    competidores = random.sample(populacao, k)
    melhor = max(
        competidores, key=lambda ind: calcular_fitness(ind, atividades, horas_totais)
    )
    return melhor.clone()


def selecionar_proxima_geracao(
    populacao: list[Cromossomo],
    atividades: list[Atividade],
    horas_totais: int,
    n_elite: int = 1,
    k: int = 2,
) -> list[Cromossomo]:
    """
    Seleção com elitismo + torneio.
    - n_elite: número de melhores cromossomos mantidos diretamente.
    - k: tamanho do torneio.
    """
    # Avalia fitness de todos
    avaliados = [
        (ind, calcular_fitness(ind, atividades, horas_totais)) for ind in populacao
    ]
    avaliados.sort(key=lambda x: x[1], reverse=True)

    # Elite: mantém os melhores
    nova_pop = [ind.clone() for ind, _ in avaliados[:n_elite]]

    # Preenche o resto com torneio
    while len(nova_pop) < len(populacao):
        novo = torneio_selecao(populacao, atividades, horas_totais, k)
        nova_pop.append(novo)

    return nova_pop

# A função de fitness deverá levar em conta o número de atividades que foram corretamente entregues no prazo, o número de horas que restaram da semana (devem restar poucas), e
# o peso de cada atividade não entregue perdida (atividades importantes não entregues são prejudiciais)
from typing import List
from model import *


def calcular_fitness(
    individuo: Cromossomo, atividades: List[Atividade], horas_totais_semana: int
) -> float:
    fitness = 0

    # Mapear horas alocadas por atividade
    horas_por_atividade = {a.id: 0 for a in atividades}
    horas_por_dia = {d: 0 for d in range(6)}  # 6 dias: segunda-sábado

    for aloc in individuo.genes:
        horas_por_atividade[aloc.atividade_id] += aloc.horas_alocadas
        horas_por_dia[aloc.dia] += aloc.horas_alocadas

    # Critério 1: Recompensa atividades concluídas no prazo
    for atividade in atividades:
        horas = horas_por_atividade[atividade.id]
        if horas >= atividade.duracao:  # concluída
            fitness += atividade.peso
        else:
            # penaliza pela parte que faltou
            falta = atividade.duracao - horas
            fitness -= atividade.peso * (falta / atividade.duracao)

    # Critério 2: Penalizar excesso de horas por dia (>3h)
    for dia, horas in horas_por_dia.items():
        if horas > 3:
            fitness -= (horas - 3) * 2  # penalidade maior

    # Critério 3: Penalizar horas ociosas da semana
    horas_usadas = sum(horas_por_atividade.values())
    horas_restantes = horas_totais_semana - horas_usadas
    if horas_restantes > 0:
        fitness -= horas_restantes * 0.5  # penaliza um pouco

    return fitness

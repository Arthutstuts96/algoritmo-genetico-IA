# Funções para gerar a população inicial
from typing import List
from model import Alocacao, Atividade, Cromossomo, DiaSemana
import random



# def calcular_horas_totais(atividades: List[Atividade]) -> int:
#     """Horas totais são a soma dos pesos (1h por unidade de peso)."""
#     return sum(a.peso for a in atividades)


def gerar_individuo(atividades: List[Atividade]) -> Cromossomo:
    """Gera uma alocação inicial aleatória respeitando 3h por dia."""
    genes = []
    horas_por_dia = {d: 0 for d in DiaSemana}

    for atividade in atividades:
        horas_restantes = atividade.peso
        while horas_restantes > 0:
            dia = random.choice(list(DiaSemana))
            aloc_horas = min(horas_restantes, 1)  # Cada tarefa tem pelo menos 1 hora

            # respeitar limite de 3h/dia
            if horas_por_dia[dia] + aloc_horas <= 3:
                genes.append(Alocacao(atividade.id, dia, aloc_horas))
                horas_por_dia[dia] += aloc_horas
                horas_restantes -= aloc_horas

    return Cromossomo(genes)


def gerar_populacao_inicial(
    atividades: List[Atividade], tamanho: int = 4
) -> List[Cromossomo]:
    return [gerar_individuo(atividades) for _ in range(tamanho)]

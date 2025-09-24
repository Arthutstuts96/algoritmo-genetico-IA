from typing import List
from model import *


def calcular_fitness(
    individuo: Cromossomo, atividades: List[Atividade], horas_totais_semana: int
) -> float:
    """
    a função fitness é baseada em:
        - bônus por entregas no prazo,
        - bônus por restarem poucas horas na semana livres,
        - penalidade pelo peso de atividades não entregues,
        - penalidade por excesso em um dia (>3h) e por alocação além do total informado.
    """
    # Constantes representando o bônus/penalidade de cada aspecto da função de fitness
    ON_TIME_BONUS_MULT = 5.0
    MISSING_PENALTY_MULT = 3.0
    HOUR_REMAIN_PENALTY = 2.0
    OVERALLOCATION_PENALTY = 4.0
    DAY_EXCESS_PENALTY = 6.0
    LATE_DAY_PENALTY_PER_DAY = 2.0

    # Se horas_totais_semana não informado ou <= 0, usa soma dos pesos como mínimo necessário
    if not horas_totais_semana or horas_totais_semana <= 0:
        horas_totais_semana = sum(a.peso for a in atividades)

    fitness = 0.0

    # Agregados
    horas_por_atividade = {a.id: 0 for a in atividades}
    horas_por_dia = {d: 0 for d in DiaSemana}  # chaves: DiaSemana
    ultima_aloc_por_atividade = {a.id: None for a in atividades}

    # Preenche agregados a partir dos genes
    for aloc in individuo.genes:
        # soma horas por atividade
        horas_por_atividade[aloc.atividade_id] = (
            horas_por_atividade.get(aloc.atividade_id, 0) + aloc.horas_alocadas
        )

        # soma horas por dia (aloc.dia deve ser DiaSemana)
        horas_por_dia[aloc.dia] = horas_por_dia.get(aloc.dia, 0) + aloc.horas_alocadas

        # registra última data (valor inteiro) em que houve alocação para essa atividade
        day_val = aloc.dia.value if hasattr(aloc.dia, "value") else int(aloc.dia)
        prev = ultima_aloc_por_atividade.get(aloc.atividade_id)
        if prev is None or day_val > prev:
            ultima_aloc_por_atividade[aloc.atividade_id] = day_val

    # Avalia cada atividade
    for atividade in atividades:
        req_horas = atividade.peso  # regra: peso -> horas mínimas requeridas
        alocadas = horas_por_atividade.get(atividade.id, 0)
        frac_concluida = min(alocadas / req_horas, 1.0) if req_horas > 0 else 1.0

        # crédito proporcional ao que foi alocado (incentiva progresso parcial)
        fitness += atividade.peso * frac_concluida

        if alocadas >= req_horas:
            # atividade concluída (verifica prazo)
            ultima = ultima_aloc_por_atividade.get(atividade.id)
            prazo_val = (
                atividade.prazo.value
                if hasattr(atividade.prazo, "value")
                else int(atividade.prazo)
            )
            if ultima is not None and ultima <= prazo_val:
                # concluída no prazo -> grande bônus proporcional ao peso
                fitness += atividade.peso * ON_TIME_BONUS_MULT
            else:
                # concluída, mas atrasada -> pequena recompensa menos penalidade por dias atrasados
                fitness += atividade.peso * (ON_TIME_BONUS_MULT / 2.0)
                # se ultima for None, deixa sem penalidade adicional (caso raro)
                if ultima is not None:
                    dias_atraso = max(0, ultima - prazo_val)
                    fitness -= atividade.peso * LATE_DAY_PENALTY_PER_DAY * dias_atraso
        else:
            # não concluída: penaliza a fração que falta (atividades importantes penalizam mais)
            falta_frac = 1.0 - frac_concluida
            fitness -= atividade.peso * MISSING_PENALTY_MULT * falta_frac

    # Penaliza excesso de horas em qualquer dia (> 3h)
    for dia, horas in horas_por_dia.items():
        if horas > 3:
            fitness -= (horas - 3) * DAY_EXCESS_PENALTY

    # Penaliza horas restantes na semana (queremos usar a disponibilidade)
    horas_usadas = sum(horas_por_atividade.values())
    horas_restantes = horas_totais_semana - horas_usadas
    if horas_restantes > 0:
        fitness -= horas_restantes * HOUR_REMAIN_PENALTY
    elif horas_restantes < 0:
        # se alocou mais que o total informado, penaliza forte
        fitness -= (-horas_restantes) * OVERALLOCATION_PENALTY

    return float(fitness)

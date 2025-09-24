from dataclasses import dataclass, field
import random
from typing import List, Optional
from enum import IntEnum


# Enum para dias da semana (domingo fora, já que não tem atividade)
class DiaSemana(IntEnum):
    SEGUNDA = 0
    TERCA = 1
    QUARTA = 2
    QUINTA = 3
    SEXTA = 4
    SABADO = 5


@dataclass
class Atividade:
    id: str
    nome: str
    prazo: DiaSemana
    peso: int


@dataclass
class Alocacao:
    atividade_id: str
    dia: DiaSemana
    horas_alocadas: int


# Cromossomo (indivíduo); Cada tarefa é estimada em um mínimo de 1 hora para resolução, além de que não deve haver mais de 3 horas de atividade em um mesmo dia, a não ser que o
# total de horas ainda não tenha sido cumprido (prioriza tarefas mais perto)


# O horário é considerado bom caso ele seja capaz de terminar todas as suas tarefas e alocar corretamente as horas disponíveis, permitindo o usuário usá-lo para estudos
@dataclass
class Cromossomo:
    genes: List[Alocacao] = field(default_factory=list)
    fitness: Optional[float] = None

    def clone(self) -> "Cromossomo":
        cloned_genes = [Alocacao(**vars(g)) for g in self.genes]
        return Cromossomo(genes=cloned_genes, fitness=self.fitness)

    def __len__(self) -> int:
        return len(self.genes)


# Funções para gerar a população inicial
def calcular_horas_totais(atividades: List[Atividade]) -> int:
    """Horas totais são a soma dos pesos (1h por unidade de peso)."""
    return sum(a.peso for a in atividades)


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

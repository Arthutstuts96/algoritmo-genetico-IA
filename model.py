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

    # def clone(self) -> "Alocacao":
    #     cloned_genes = [Alocacao(**vars(g)) for g in self.genes]
    #     return Cromossomo(genes=cloned_genes, fitness=self.fitness)


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

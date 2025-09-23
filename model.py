from dataclasses import dataclass, field
from typing import List, Optional
from enum import IntEnum

class DiaSemana(IntEnum):
    SEGUNDA = 0
    TERCA   = 1
    QUARTA  = 2
    QUINTA  = 3
    SEXTA   = 4
    SABADO  = 5

# Representa uma atividade que precisa ser feita na semana
@dataclass
class Atividade:
    id: str
    nome: str
    duracao: int            # horas necessárias para completar
    prazo: DiaSemana              # dia limite (ex: "segunda", "quarta"...)
    peso: int               # prioridade da atividade

# Representa um dia da semana (exceto domingo)
@dataclass
class Dia:
    dia: DiaSemana
    horas_disponiveis: int  # quantas horas a pessoa pode dedicar nesse dia

# Representa a alocação de uma atividade em um dia
@dataclass
class Alocacao:
    atividade_id: str
    dia: DiaSemana
    horas_alocadas: int

# Cromossomo (um indivíduo da população)
@dataclass
class Individual:
    genes: List[Alocacao] = field(default_factory=list)
    fitness: Optional[float] = None

    def clone(self) -> 'Individual':
        cloned_genes = [Alocacao(**vars(g)) for g in self.genes]
        new_individual = Individual(genes=cloned_genes)
        new_individual.fitness = self.fitness
        return new_individual

    def __len__(self) -> int:
        return len(self.genes)

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Professor:
    id: str
    nome: str
    areas: List[str]

@dataclass
class Disciplina:
    id: str
    nome: str
    area: str
    horas_semanais: int

@dataclass
class Turma:
    id: str
    disciplina_id: str
    curso: str
    periodo: str
    horas_necessarias: int
    tipo_periodo: str # Ex: "diurno" ou "noturno"

@dataclass
class Sala:
    id: str
    capacidade: int
    tipo: str # Ex: "teorica" ou "laboratorio"

@dataclass
class Periodo:
    id: str
    dia: str
    horario: str
    slot_id: int

@dataclass
class Alocacao:
    turma_id: str
    professor_id: str
    sala_id: str
    periodo_id: str
    fixed: bool = False # Atributo opcional com valor padrão

@dataclass
class Individual:
    genes: List[Alocacao] = field(default_factory=list)
    fitness: Optional[float] = None

    def clone(self) -> 'Individual':
        """Retorna uma cópia do indivíduo."""
        # Cria uma nova lista de genes com cópias dos genes originais
        cloned_genes = [gene for gene in self.genes]
        new_individual = Individual(genes=cloned_genes)
        new_individual.fitness = self.fitness
        return new_individual

    def __len__(self) -> int:
        """Retorna a quantidade de genes (alocações)."""
        return len(self.genes)
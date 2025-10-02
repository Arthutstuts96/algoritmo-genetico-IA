import random
from model import Cromossomo, Alocacao, DiaSemana


def crossover_uniforme(pai1: Cromossomo, pai2: Cromossomo) -> tuple[Cromossomo, Cromossomo]:
    """Crossover uniforme: cada gene do filho vem aleatoriamente de um dos pais."""
    tamanho = min(len(pai1.genes), len(pai2.genes))
    filho1_genes, filho2_genes = [], []

    for i in range(tamanho):
        if random.random() < 0.5:
            filho1_genes.append(pai1.genes[i])
            filho2_genes.append(pai2.genes[i])
        else:
            filho1_genes.append(pai2.genes[i])
            filho2_genes.append(pai1.genes[i])

    return Cromossomo(filho1_genes), Cromossomo(filho2_genes)


def mutacao(populacao: list[Cromossomo], prob: float = 0.3) -> None:
    """
    Aplica mutação em todos os indivíduos (menos elite) com certa probabilidade.
    Cada mutação pode alterar múltiplos genes.
    """
    for ind in populacao[1:]:  # mantém o elite intacto
        if random.random() < prob and ind.genes:
            n_genes_mutar = random.randint(1, max(1, len(ind.genes) // 2))  
            for _ in range(n_genes_mutar):
                gene = random.choice(ind.genes)
                if random.random() < 0.5:
                    gene.dia = random.choice(list(DiaSemana))
                else:
                    gene.horas_alocadas = random.randint(1, 3)

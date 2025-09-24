from fitness import calcular_fitness
from model import *


def main():
    # População inicial
    # TODO: substituir para entradas do usuário, gerar id automático
    atividades = [
        Atividade("A1", "Relatório", peso=3, prazo=DiaSemana.QUARTA),
        Atividade("A2", "Estudo", peso=2, prazo=DiaSemana.SEXTA),
        Atividade("A3", "Exercícios", peso=1, prazo=DiaSemana.SABADO),
    ]
    populacao = gerar_populacao_inicial(atividades, tamanho=4)

    # Print dos cromossomos, para debug
    for i, cromossomo in enumerate(populacao, start=1):
        print(f"\nCromossomo {i}:")
        for gene in cromossomo.genes:
            print(f" - {gene.atividade_id} | {gene.dia.name} | {gene.horas_alocadas}h")

    # Avaliando Fitness da população inicial
    print("\n--- Avaliação inicial ---")
    for i, cromossomo in enumerate(populacao, start=1):
        score = calcular_fitness(cromossomo, atividades, 6)
        print(f"Cromossomo {i} | Fitness = {score:.2f}")


if __name__ == "__main__":
    main()

from fitness import calcular_fitness
from model import *


def main():
    # População inicial (atividades estão para debug, depois substituir para entradas do usuário)
    atividades = [
        Atividade("A1", "Relatório", peso=3, prazo=DiaSemana.QUARTA),
        Atividade("A2", "Estudo", peso=2, prazo=DiaSemana.SEXTA),
        Atividade("A3", "Exercícios", peso=1, prazo=DiaSemana.SABADO),
    ]
    populacao = gerar_populacao_inicial(atividades, tamanho=4)

    # 3. Mostrar cromossomos
    for i, cromossomo in enumerate(populacao, start=1):
        print(f"\nCromossomo {i}:")
        for gene in cromossomo.genes:
            print(f" - {gene.atividade_id} | {gene.dia.name} | {gene.horas_alocadas}h")

if __name__ == "__main__":
    main()

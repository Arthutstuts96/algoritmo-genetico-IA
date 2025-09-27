from model import *


def imprimir_horario(cromossomo: Cromossomo):
    print("\n===== MELHOR HORÁRIO ENCONTRADO =====")
    dias = {dia: [] for dia in DiaSemana}
    for gene in cromossomo.genes:
        dias[gene.dia].append((gene.atividade_id, gene.horas_alocadas))

    for dia in DiaSemana:
        print(f"\n📅 {dia.name}:")
        if dias[dia]:
            for atividade, horas in dias[dia]:
                print(f"   - {atividade} ({horas}h)")
        else:
            print("   - (nenhuma atividade)")
    print("=====================================")

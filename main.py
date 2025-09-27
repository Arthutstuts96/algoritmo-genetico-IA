import random
from crossover import crossover_uniforme, mutacao
from init_population import gerar_populacao_inicial
from model import Atividade, DiaSemana, Cromossomo
from fitness import *
from print_schedule import imprimir_horario
from selection import selecionar_proxima_geracao


def main():
    # --- configuração ---
    atividades = [
        Atividade("A1", "Relatório", peso=3, prazo=DiaSemana.QUARTA),
        Atividade("A2", "Estudo", peso=2, prazo=DiaSemana.SEXTA),
        Atividade("A3", "Exercícios", peso=1, prazo=DiaSemana.QUARTA),
        Atividade("A4", "Exercícios", peso=3, prazo=DiaSemana.SABADO),
        Atividade("A5", "Exercícios", peso=2, prazo=DiaSemana.TERCA),
        Atividade("A6", "Exercícios", peso=4, prazo=DiaSemana.SABADO),
    ]

    horas_semana = 15  # DEVE SER pelo menos a soma dos pesos das atividades
    tamanho_populacao = 24
    n_elite = 1
    torneio_k = 12
    max_geracoes = len(atividades) * 10

    # --- população inicial ---
    populacao = gerar_populacao_inicial(atividades, tamanho=tamanho_populacao)

    fitness_max = fitness_maximo_teorico(atividades)
    geracao = 0

    while geracao < max_geracoes:
        geracao += 1
        print(f"\n=== Geração {geracao} ===")

        for i in populacao:
            print(calcular_fitness(i, atividades, horas_semana)) 

        # Avalia população atual
        scores = [calcular_fitness(ind, atividades, horas_semana) for ind in populacao]
        melhor_fitness = max(scores)
        melhor_idx = scores.index(melhor_fitness)
        melhor_individuo = populacao[melhor_idx]

        print(f"Melhor fitness da geração = {melhor_fitness:.2f} / {fitness_max:.2f}")

        # critério de parada
        if melhor_fitness >= fitness_max:
            print("\n✅ Parada: melhor fitness máximo atingido!")
            imprimir_horario(melhor_individuo)
            return

        # ---------------------------
        # SELEÇÃO (torneio + elitismo)
        # ---------------------------
        populacao_selecionada = selecionar_proxima_geracao(
            populacao, atividades, horas_semana, n_elite=n_elite, k=torneio_k
        )

        # separamos elites (já clonados pela função de seleção idealmente)
        elites = [ind.clone() for ind in populacao_selecionada[:n_elite]]

        # pool que vai ao crossover (não inclui elites)
        pool = populacao_selecionada[n_elite:]
        random.shuffle(pool)

        # ---------------------------
        # CROSSOVER (aplica só no pool, preservando elites)
        # ---------------------------
        children = []
        for i in range(0, len(pool), 2):
            if i + 1 < len(pool):
                pai1, pai2 = pool[i], pool[i + 1]
                filho1, filho2 = crossover_uniforme(pai1, pai2)

                # garantir deep-copy (evita referências compartilhadas)
                filho1 = filho1.clone()
                filho2 = filho2.clone()

                children.extend([filho1, filho2])
            else:
                # item solitário: passa adiante como clone (ou podemos cruzá-lo com elite)
                children.append(pool[i].clone())

        # Monta nova população: elites + filhos
        nova_pop = elites + children

        # Ajusta tamanho caso necessário (trunca ou completa com clones aleatórios)
        if len(nova_pop) > tamanho_populacao:
            nova_pop = nova_pop[:tamanho_populacao]
        while len(nova_pop) < tamanho_populacao:
            nova_pop.append(random.choice(populacao).clone())

        # ---------------------------
        # MUTAÇÃO (aplica só nos não-elites para preservar elite)
        # ---------------------------
        # se quiser proteger elites: muta somente a fatia [n_elite:]
        mutacao(nova_pop[n_elite:], prob=0.3)

        # Atualiza população para próxima geração
        populacao = nova_pop

    # Se chegou aqui, atingiu limite de gerações
    print("\nLimite de gerações atingido sem encontrar solução ótima.")
    # exibe melhor encontrado
    scores = [calcular_fitness(ind, atividades, horas_semana) for ind in populacao]
    best_idx = scores.index(max(scores))
    imprimir_horario(populacao[best_idx])


if __name__ == "__main__":
    main()

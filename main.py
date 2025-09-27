import random
from crossover import crossover_uniforme, mutacao
from init_population import gerar_populacao_inicial
from model import Atividade, DiaSemana
from fitness import *
from save_schedule import salvar_horario
from selection import selecionar_proxima_geracao


def main():
    # --- Inputs do usuário e configurações iniciais ---
    atividades = []
    horas_semana = 0
    limite = 30
    id_counter = 1

    while horas_semana < limite:
        nome = input("Digite o nome da atividade (ou ENTER para parar): ").strip()
        if not nome:
            break

        peso = int(input("Digite o peso (horas necessárias), indo de 1 a 5: "))
        if peso > 5: peso = 5
        if peso < 1: peso = 1
        
        prazo_str = input("Digite o prazo (SEGUNDA, TERCA, QUARTA, QUINTA, SEXTA, SABADO): ").upper()

        prazo = DiaSemana[prazo_str]
        atividade = Atividade(f"A{id_counter}", nome, peso=peso, prazo=prazo)
        atividades.append(atividade)
        horas_semana += peso
        id_counter += 1

        if horas_semana >= limite:
            print("⚠️ Limite de 30 horas semanais atingido!")
            break

    tamanho_populacao = 24
    n_elite = 1
    torneio_k = 12
    # RODA o loop por até 100 vezes o número de atividades, devolve a melhor encontrada
    max_geracoes = len(atividades) * 100

    populacao = gerar_populacao_inicial(atividades, tamanho=tamanho_populacao)
    fitness_max = fitness_maximo_teorico(atividades)
    geracao_atual = 0

    # --- Loop principal ---
    while geracao_atual < max_geracoes:
        geracao_atual += 1
        print(f"\n=== Geração {geracao_atual} ===")

        pontuacoes = [
            calcular_fitness(ind, atividades, horas_semana) for ind in populacao
        ]
        melhor_fitness = max(pontuacoes)
        melhor_idx = pontuacoes.index(melhor_fitness)
        melhor_individuo = populacao[melhor_idx]

        print(f"Melhor fitness da geração = {melhor_fitness:.2f} / {fitness_max:.2f}")

        # Critério de parada (SUCESSO)
        if melhor_fitness >= fitness_max:
            print("\n✅ Parada: melhor fitness máximo atingido!")
            salvar_horario(melhor_individuo, atividades)
            return

        # ---------------------------
        # SELEÇÃO (torneio + elitismo)
        # ---------------------------
        populacao_selecionada = selecionar_proxima_geracao(
            populacao, atividades, horas_semana, n_elite=n_elite, k=torneio_k
        )
        elites = [ind.clone() for ind in populacao_selecionada[:n_elite]]

        pool = populacao_selecionada[n_elite:]
        random.shuffle(pool)

        # ---------------------------
        # CROSSOVER
        # ---------------------------
        prox_geracao = []
        for i in range(0, len(pool), 2):
            if i + 1 < len(pool):
                pai1, pai2 = pool[i], pool[i + 1]
                filho1, filho2 = crossover_uniforme(pai1, pai2)

                filho1 = filho1.clone()
                filho2 = filho2.clone()

                prox_geracao.extend([filho1, filho2])
            else:
                prox_geracao.append(pool[i].clone())

        nova_pop = elites + prox_geracao

        # Mecanismos de segurança para caso a população exceda ou seja menor que o ideal
        if len(nova_pop) > tamanho_populacao:
            nova_pop = nova_pop[:tamanho_populacao]
        while len(nova_pop) < tamanho_populacao:
            nova_pop.append(random.choice(populacao).clone())

        # ---------------------------
        # MUTAÇÃO
        # ---------------------------
        mutacao(nova_pop[n_elite:], prob=0.3)

        populacao = nova_pop

    # Limite de gerações, imprime o melhor encontrado
    print("\nLimite de gerações atingido, computando melhor resultado: ")
    pontuacoes = [calcular_fitness(ind, atividades, horas_semana) for ind in populacao]
    best_idx = pontuacoes.index(max(pontuacoes))
    salvar_horario(populacao[best_idx], atividades)


if __name__ == "__main__":
    main()

# salvar_horario.py
from model import Atividade, DiaSemana, Cromossomo


def salvar_horario(
    cromossomo: Cromossomo, atividades: list[Atividade], filename: str = "horario.txt"
):
    """
    Salva o horário de um cromossomo em um arquivo txt.
    Mostra primeiro o quadro de entregas da semana (prazos),
    depois o cronograma detalhado de alocação de horas.
    """
    dias = list(DiaSemana)
    mapa_atividades = {a.id: a for a in atividades}

    # --- Quadro de entregas (prazos das atividades) ---
    entregas_por_dia: dict[DiaSemana, list[str]] = {dia: [] for dia in dias}
    for a in atividades:
        entregas_por_dia[a.prazo].append(a.nome)

    # --- Agrupar alocações do cromossomo ---
    atividades_por_dia: dict[DiaSemana, list[str]] = {dia: [] for dia in dias}
    for gene in cromossomo.genes:
        atividade = mapa_atividades.get(gene.atividade_id)
        if atividade:
            atividades_por_dia[gene.dia].append(
                f"{atividade.nome} ({gene.horas_alocadas}h)"
            )

    # --- Escrever no arquivo ---
    with open(filename, "w", encoding="utf-8") as f:
        f.write("===== MELHOR HORÁRIO ENCONTRADO =====\n\n")

        f.write("📌 Quadro de entregas (prazos):\n")
        for dia in dias:
            nome_dia = dia.name.capitalize()
            entregas = entregas_por_dia[dia]
            if entregas:
                linha = f"   {nome_dia}: " + ", ".join(entregas)
            else:
                linha = f"   {nome_dia}: (nenhuma entrega)"
            f.write(linha + "\n")

        f.write("\n📅 Cronograma detalhado:\n")
        for dia in dias:
            nome_dia = dia.name.capitalize()
            atividades = atividades_por_dia[dia]
            if atividades:
                linha = f"   {nome_dia}: " + ", ".join(atividades)
            else:
                linha = f"   {nome_dia}: (nenhuma atividade)"
            f.write(linha + "\n")

        f.write("\n=====================================\n")

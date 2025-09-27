<img src="/images/gene.png" alt="Ícone de uma fita dupla de DNA, para exemplificar o genético" width=80/>

# Algoritmo Genético 

<p>Este repositório contém o código fonte para resolver um problema de busca a partir de um <strong>algoritmo genético</strong>. O problema escolhido para ser resolvido foi o problema de <strong>geração de grade horária</strong></p>

<p>Tomamos um caminho diferente para, ao invés de gerar a grade horária considerando salas de aula, professores e matérias, como exposto nos artigos de referência, gerar uma grade horária para otimizar resolução de tarefas, considerando a <strong>data de entrega, peso e horas disponíveis na semana</strong></p>

<p>Ao final, o algoritmo retornará um horário, que conterá a grade horária com todas as atividades cadastradas e o que realizar cada dia, para que, ao final da semana, não tenha nenhuma pendência, respeitando a prioridade de cada atividade</p>

## Regras
<ol>
    <li>Devem ser informadas as atividades, sendo que cada atividade contém uma prioridade (peso) associado, e deve ser entregue naquela semana</li>
    <li>Considera-se que cada atividade exige pelo menos uma hora para ser completa, sendo então uma hora o mínimo de horas alocadas para tal atividade</li>
    <li>O dia pode ter, no máximo, três horas totais alocadas, salvo se o número de horas livres ultrapassar esse limite para cada dia da semana, mas não é o recomendado</li>
    <!-- <li></li>
    <li></li>
    <li></li> -->
</ol>

## Planejamento
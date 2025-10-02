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

<p>Cada cromossomo (indivíduo) tem as seguintes características:</p>

<ul>
<li>Genes: Lista de cada um de seus genes, que correspondem ao tipo Alocacao. Esse, por sua vez, contém o id da atividade, o dia de prazo dela e a quantidade de horas alocadas para ela ser feita</li>
<li>Fitness: Valor que representa a qualidade do cromossomo. É peça fundamental nos cálculos de população para saber se aquele indivíduo é adequado para resolver o problema ou, ao menos, possui ferramentas importantes para tal e podem ser levadas para outras gerações. Detalhes da função fitness estão abaixo</li>
</ul>

<p>A função fitness avalia a qualidade de um cronograma levando em conta múltiplos fatores de desempenho. O indivíduo recebe bônus quando consegue entregar atividades dentro do prazo, refletindo a prioridade de cumprir compromissos na data correta. Também há bônus proporcional ao aproveitamento do tempo disponível, premiando cromossomos que deixam poucas horas livres na semana. Em contrapartida, o algoritmo aplica penalidades quando atividades não são concluídas, ponderadas pelo peso (importância) de cada tarefa. Além disso, para manter a viabilidade do cronograma, são aplicadas penalidades quando há sobrecarga diária acima de 3 horas ou quando o total de horas alocadas excede o limite informado. Dessa forma, a função equilibra prazos, aproveitamento do tempo e viabilidade prática, guiando a evolução para soluções otimizadas</p>

<p>Como vimos que estava havendo uma seleção arbitrária que poderia perder indivíduos com alto fitness em gerações menores, também implementamos um elitismo, consistindo em manter alguns dos indivíduos mais bem adaptados para a próxima geração, sem necessidade de crossover ou mutação. Para amostras maiores, isso se provou vantajoso, e permitiu realizar o trabalho em menos iterações. Em contrapartida, os mecanismos de seleção crossover e de mutação precisavam ser mais potentes, a fim de não perder a variabilidade genética e trazer mais opções às próximas gerações</p>

<p>Também implementamos mecanismos de segurança para criação das novas gerações, evitando que ela cresça ou seja diminuída para o menor que o ideal. Para isso, tiveram de ser clonados indivíduos, então o algoritmo se beneficiaria de populações maiores, caso esse seja o caso e a variabilidade genética se perca, mas evitando minar o desempenho</p>

<p>Constatamos que, através de testes com entradas, caso a entrada não seja capaz de seguir as regras (Ex: ter atividades que ultrapassem o limite de 3 horas diárias na segunda feira), a solução ótima não pode ser encontrada, ou, caso seja possível, leva muito mais que o limite de iterações</p>
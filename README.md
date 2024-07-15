# Contexto do problema

Londres é uma cidade global, uma das cidades mais importantes da região europeia e do mundo inteiro. Embora caótico, seus milhares de cidadãos e turistas utilizam diariamente da sua rede de metrôs para acessar as demais localidades e aproveitar tudo que a cidade tem a oferecer. Assim sendo, decidi utilizar uma base de dados referente à linha de metrôs datada do ano de 2012, que conta com 309 estações cadastradas na base. A base de dados, extraída do Wikimedia Commons, apresenta 4 diferentes conteúdos que são referentes ao sistema metroviário, sendo eles: Estações, Rotas, Definições de Linha e Coordenadas X e Y para as estações de zona 1. Entretanto, por motivos de relevância, foquei apenas em campos cujas bases de dados Estações (`Stations.csv`) e Definições de Linha (`Line_definitions.csv`) oferecem.

## Implementação

### Algoritmo utilizado

O algoritmo utilizado para desenvolver o projeto foi o Dijkstra, sendo muito eficiente para resolver questões que são relevantes à procura de trajetos mais rápidos.

### Desenvolvimento

Para que o projeto pudesse usar de uma ferramenta que implementasse pesos, decidi usar a função de haversine, equação matemática que ajuda a calcular a distância entre dois pontos na Terra, usando suas coordenadas de latitude e longitude. Assim, criei funções para extrair as informações necessárias de cada um dos arquivos CSV, a `load_stations` para as estações e a `load_connections` para as conexões dessas estações, para que em seguida elas pudessem ser usadas no algoritmo de Dijkstra de forma já filtrada.

A função `update_graph` executa o algoritmo de Dijkstra para encontrar o menor caminho entre as estações após obter os IDs das estações de partida e chegada nos inputs, outputando o menor caminho encontrado (o nome das estações seguido de todos os IDs e nomes de cada uma das estações pelo qual o usuário deve passar até chegar ao destino final), seguido do peso total do caminho, medido aproximadamente em quilômetros (arredondado por 2 casas decimais), seguido de um gráfico que mostra as estações de partida (em verde) e a estação de chegada (em vermelho) e uma linha mostrando cada uma das linhas em que o metrô passa. Além disso, essa função limpa o gráfico anteriormente exibido cada vez que uma nova consulta é feita, além de exibir as informações de menor caminho e o peso.

Por fim, a função `create_gui` é responsável por criar a interface gráfica do usuário que permite uma melhor visualização e experiência quando o código for executado.

## Bibliotecas utilizadas

Utilizei as seguintes bibliotecas:
- `csv` para ter uma melhor performance já que estamos trabalhando com dados no formato CSV.
- `math` para ajudar nos cálculos referentes ao teorema de haversine.
- `collections.defaultdict` para criar um valor padrão para as chaves ausentes, possibilitando a criação de grafos que representem a conexão entre estações de metrô.
- `matplotlib.pyplot` é usado para a criação das visualizações gráficas dos dados, como o mapa e as conexões entre as estações de metrô.
- `tkinter` é usada para criar a interface gráfica do usuário.

## Conclusão

Para rodar o arquivo, é necessário ter as bibliotecas `matplotlib` e `tk` instaladas. Ao executar o programa, você deverá digitar primeiramente a Estação de Partida e após isso a Estação de Chegada. Ao clicar em "Encontrar Rota", uma nova tela será automaticamente aberta mostrando o caminho do vértice de partida ao vértice de chegada, com o caminho grifado em vermelho e as linhas pelas quais ele passa. Na janela principal, após digitar os inputs necessários de Estação de partida e chegada, você irá encontrar também as informações referentes ao menor caminho da estação de partida até o destino, sendo listados todos os vértices que devem ser visitados (seguidos de seus respectivos nomes de estações entre parênteses), e por fim o peso total do caminho, representado pela distância em quilômetros (arredondado para duas casas decimais) entre eles. Ao clicar para rodar o arquivo, você será apresentado a essa tela. Ao digitar os números das estações e clicar em "Encontrar Rota", será mostrado um gráfico que indica a rota a ser seguida, bem como as informações do menor caminho e o peso total do caminho. Vale salientar que a base de dados aparentemente é datada de 2012, então acredito que mudanças no sistema metroviário da cidade de Londres tenham sido feitas desde então, assim, inconsistências podem ocorrer, e discrepâncias podem ocorrer entre os dados do programa e a realidade atual.

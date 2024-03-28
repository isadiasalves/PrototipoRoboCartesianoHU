# import
import random
import math
import itertools
from random import choices
import timeit

# definição das variáveis
dist = 0  # distância para coletar os medicamentos solicitados
# variáveis que armazenam as coordenadas dos medicamentos (usadas para calcular as distâncias entre eles)
x1 = 0
y1 = 0
x2 = 0
y2 = 0
med_pedidos = []  # lista de medicamentos solicitados pelo profissional da farmácia
coord_pedidos = []  # lista de coordenadas dos medicamentos solicitados
elemento = []  # lista criada para realizar a permutação e salvar todas as sequências de coleta possíveis
listas = []  # lista que irá conter as possíveis sequências-soluções de medicamentos
lista_dist = []  # lista que armazena as distâncias das sequências criadas
lista_dist_filhos = []  # lista que armazena as distâncias dos descendentes gerados
pais_selecionados = []  # lista das sequências selecionadas para gerar novos descendentes
dist_pais_selecionados = [] # lista que armazena as distâncias das sequências selecionadas para gerar novos descendentes
coordenadas_4coleta = [] # coordenadas da sequência que obteve menor distância
filhos = []  # lista dos descendentes obtidos após o cruzamento
# lista de medicamentos disponíveis nas prateleiras
lista_med = ['acetilcisteina', 'buscopan', 'diazepam', 'levotiroxina 25', 'levotiroxina 50',
             'levotiroxina 75', 'gardenal', 'tilenol', 'dorflex', 'alexofedrina', 'plasil', 'dramim', 'ibuprofeno', 'propanolol', 'captopril']
lista_med_solicitado = []  # lista dos medicamentos solicitados
# lista das coordenadas dos medicamentos disponíveis nas prateleiras
coord_med = [(1, 1), (1, 9), (1, 25), (1, 33), (2, 16),
             (2, 17), (2, 18), (2, 21), (3, 31), (3, 40), (3, 52), (3, 60), (2, 53), (1, 47), (3, 25)]

# cria a função fitness que será aplicada nas sequências geradas para verificar seus desempenhos (calcular a distância que o robô irá percorrer)
def dist(lista_indiv, coord_pedidos, qtd_medicamento):
    for j in range(len(lista_indiv)):
        seq = lista_indiv[j]
        # calcula a distância inicial do robô (0,0) até o primeiro medicamento
        x1, y1 = coord_pedidos[seq[0]-1]
        dist = math.sqrt((abs(x1 - 0)**2 + (abs(y1 - 0))**2))

        # calcula a distância entre os medicamentos definidos na sequência seq
        for i in range((qtd_medicamento-1)):
            x1, y1 = coord_pedidos[(seq[i]-1)]
            x2, y2 = coord_pedidos[(seq[i+1]-1)]
            dist = math.sqrt((abs(x2 - x1)**2 + (abs(y2 - y1))**2)) + dist

        # calcula a distância do último medicamento até o ponto inicial que o robô deverá retornar (0,0)
        x2, y2 = coord_pedidos[seq[-1]-1]
        dist = math.sqrt((abs(x2 - 0)**2 + (abs(y2 - 0))**2)) + dist

        lista_dist.append(dist)
    return lista_dist


# profissional define a quantidade de medicamentos a ser coletada
qtd_medicamento = int(
    input('Digite a quantidade de medicamentos a ser coletada: '))

# profissional informa quais os medicamentos deverão ser coletados
h = 1
qtd_medicamento_loop = qtd_medicamento
while h <= qtd_medicamento_loop:
    med = input('Medicamento: ')
    if med in lista_med:  # medicamento solicitado é procurado na lista de medicamentos disponíveis
        if med not in lista_med_solicitado:
            # recupera a poição do medicamento solicitado na lista dos disponíveis
            indice_lista_med = lista_med.index(med)
            # recupera a coordenada do medicamento solicitado na lista de coordenadas dos medicamentos disponíveis (mesmo índice da lista_med)
            coord_pedidos.append(coord_med[indice_lista_med])
            # armazena o medicamento solicitado numa lista
            lista_med_solicitado.append(med)
        # checa se o medicamento já foi solicitado
        else:
            print('{} já solicitado. Digite outro medicamento: ' .format(med))
            qtd_medicamento_loop += 1
    else:
        # se o medicamento não for encontrado na lista (por erro de digitação), é pedido ao profissional que digite novamente o nome do medicamento
        print('{} não encontrado. Digite novamente: ' .format(med))
        qtd_medicamento_loop += 1

    h += 1

# o programa foi alocado dentro de uma função para que se pudesse verificar o tempo de execução dele
def programa():
    listas = []
    lista_dist = []
    lista_dist_filhos = []
    elemento = []
    pais_selecionados = []
    filhos = []
    dist_pais_selecionados = []
    seq_menor_dist = []
    pai12 = []

    # se a quantidade de medicamento  solicitada for 1 ou 2, não é preciso realizar os processos do algoritmo genético.
    # se a quantidade de mediamento for igual a 1, o código retorna a distância para coletá-lo
    # se a quantidade de medicamento for igual a 2, o código calcula as duas distâncias e retorna a de menor valor com sua sequência e coordendas correspondentes
    if (qtd_medicamento == 1) or (qtd_medicamento == 2):
        for i in range(qtd_medicamento):
            pai12.append(i+1)
        pai12tupla = tuple(pai12)
        seq_menor_dist.append(pai12tupla)
        menor_dist = dist(seq_menor_dist, coord_pedidos, qtd_medicamento)
        for i in pai12:
            coordenadas_4coleta.append(coord_pedidos[i-1])
        print('A sequência {} obteve a menor distância de {}' .format(
            pai12, menor_dist[0]))
        print('Coordenadas finais: {}' .format(coordenadas_4coleta))

    # para quantidade de medicamento maior que 2:
    else:

        # se a quantidade de medicamento for igual a 3, serão obtidas as 6 possibilidades de sequência
        if (qtd_medicamento == 3):
            for i in range(qtd_medicamento):
                elemento.append(i+1)
            permutacoes = itertools.permutations(elemento)

            # recupera todas as possibilidades de sequência e as salva numa lista
            for permutacao in permutacoes:
                listas.append(permutacao)

            #calcula a distância de todas as possibilidades de sequência criadas
            lista_dist = dist(listas, coord_pedidos, qtd_medicamento)
            pais_selecionados = listas
            dist_pais_selecionados = lista_dist

        # paraquantidade de medicamento maior que 3:
        else:
            # cria várias soluções de sequência de medicamentos e as salva em uma lista (se for criada uma sequência já adicionada na lista, ela então é descartada)
            for i in range(15):
                elemento = random.sample(
                    range(1, (qtd_medicamento+1)), qtd_medicamento)
                if elemento not in listas:
                    listas.append(elemento)

            # para cada sequência que foi criada é calculada a distância total a ser percorrida (função fitness)
            lista_dist = dist(listas, coord_pedidos, qtd_medicamento)

            # realiza o torneio entre as sequências criadas por meio da comparação entre as distâncias delas
            # caso em que a quantidade de sequências é par (as sequências serão comparadas duas a duas)
            if (len(listas) % 2) == 0:
                i = 0
                while i <= (len(listas)-2):
                    if lista_dist[i] <= lista_dist[i+1]:
                        pais_selecionados.append(listas[i])
                        dist_pais_selecionados.append(lista_dist[i])
                    else:
                        pais_selecionados.append(listas[i+1])
                        dist_pais_selecionados.append(lista_dist[i+1])
                    i += 1

            # caso em que a quantidade de sequências é ímpar (as últimas três sequências são comparadas juntas)
            if (len(listas) % 2) != 0:
                i = 0
                while i <= (len(listas)-4):
                    if lista_dist[i] <= lista_dist[i+1]:
                        pais_selecionados.append(listas[i])
                        dist_pais_selecionados.append(lista_dist[i])
                    else:
                        pais_selecionados.append(listas[i+1])
                        dist_pais_selecionados.append(lista_dist[i+1])
                    i += 2
                tres_ultimos = [listas[-3], listas[-2], listas[-1]]
                pais_selecionados.append(min(tres_ultimos))
                dist_pais_selecionados.append(
                    lista_dist[listas.index(min(tres_ultimos))])

            # se a quantidade de sequências for ímpar, o código exclui a sequência com maior distância para que resulte num número par e possa ser realizado o cruzamento
            if (len(pais_selecionados) % 2) != 0:
                pais_selecionados.remove(
                    pais_selecionados[dist_pais_selecionados.index(max(dist_pais_selecionados))])
                dist_pais_selecionados.remove(max(dist_pais_selecionados))

        # armazena a menor distância e a sequência da menor distância selecionada
        menor_dist = min(dist_pais_selecionados)
        seq_menor_dist = pais_selecionados[dist_pais_selecionados.index(
            menor_dist)]

        # define a quantidade máxima de gerações que serão geradas
        max_geracao = 20000
        a = 0

        # realiza o processo de criação de descendentes
        while a <= (max_geracao):

            # separa as sequências selecionadas por pares para realizar o cruzamento
            w = 0
            for w in range(0, len(pais_selecionados)-1, 2):
                p1 = pais_selecionados[w]
                p2 = pais_selecionados[(w+1)]

                # cria o vetor dos descendentes
                f1 = [0]*qtd_medicamento
                f2 = [0]*qtd_medicamento

                # cria as variáveis que são utilizadas no processo de cruzamento e mutação a cada geração criada
                indices_string_bit_1 = []
                elementosp1_posicao_zeros_string_bit = []
                elementosp2_posicao_zeros_string_bit = []
                indices_elementosp1_ordem_p2 = []
                elementosp1_ordem_p2 = []
                indices_elementosp2_ordem_p1 = []
                elementosp2_ordem_p1 = []

                # cria uma lista com bits aleatórios. O tamanho da lista deve ser igual ao tamanho das sequências
                string_bit = random.choices(range(0, 2), k=qtd_medicamento)

                for i in range(len(string_bit)):
                    # recupera a posição dos 1s da lista criada
                    if string_bit[i] == 1:
                        indices_string_bit_1.append(i)

                    # cria uma lista com os elementos das sequências correspondentes aos 0s da lista de bits
                    if string_bit[i] == 0:
                        elementosp1_posicao_zeros_string_bit.append(p1[i])
                        elementosp2_posicao_zeros_string_bit.append(p2[i])

                # copia para os descendentes os elementos das sequências referentes às posições dos 1s da lista de bits criada
                for l in indices_string_bit_1:
                    f1[l] = p1[l]
                    f2[l] = p2[l]

                # cria uma lista dos índices em p2 dos elementos de p1 nas posições dos 0s
                for m in elementosp1_posicao_zeros_string_bit:
                    indices_elementosp1_ordem_p2.append(p2.index(m))

                # cria uma lista dos índices em p1 dos elementos de p2 nas posições dos 0s
                for q in elementosp2_posicao_zeros_string_bit:
                    indices_elementosp2_ordem_p1.append(p1.index(q))

                # cria uma lista de elementos de p1 nas posições dos 0s, mas na ordem em que aparecem em p2
                for r in range(len(indices_elementosp1_ordem_p2)):
                    elementosp1_ordem_p2.append(elementosp1_posicao_zeros_string_bit[indices_elementosp1_ordem_p2.index(
                        min(indices_elementosp1_ordem_p2))])
                    indices_elementosp1_ordem_p2[indices_elementosp1_ordem_p2.index(
                        min(indices_elementosp1_ordem_p2))] = 999

                # cria uma lista de elementos de p2 nas posições dos 0s, mas na ordem em que aparecem em p1
                for s in range(len(indices_elementosp2_ordem_p1)):
                    elementosp2_ordem_p1.append(elementosp2_posicao_zeros_string_bit[indices_elementosp2_ordem_p1.index(
                        min(indices_elementosp2_ordem_p1))])
                    indices_elementosp2_ordem_p1[indices_elementosp2_ordem_p1.index(
                        min(indices_elementosp2_ordem_p1))] = 999

                # adiciona em f1 os elementos de p1 nas posições dos 0s, mas na ordem que aparecem em p2 nas posições onde estão os 0s
                for t in range(len(f1)):
                    if f1[t] == 0:
                        f1[t] = elementosp1_ordem_p2[0]
                        elementosp1_ordem_p2.remove(elementosp1_ordem_p2[0])

                # adiciona em f2 os elementos de p2 nas posições dos 0s, mas na ordem que aparecem em p1 nas posições onde estão os 0s
                for u in range(len(f2)):
                    if f2[u] == 0:
                        f2[u] = elementosp2_ordem_p1[0]
                        elementosp2_ordem_p1.remove(elementosp2_ordem_p1[0])

                # processo de mutação (com taxa de ocorrência baixa na população)
                taxa_mutacao = 0.3
                sorteio_mutacao1 = random.random()
                sorteio_mutacao2 = random.random()

                # recupera um terço da quantidade de medicamentos contida nos descendentes. A mutação ocorre no terço do meio
                divisao = int(qtd_medicamento/3)

                if sorteio_mutacao1 <= taxa_mutacao:
                    # realiza mutação na parte do meio do f1 (embaralha)
                    lista_mutacao_f1 = f1[divisao:-divisao]
                    random.shuffle(lista_mutacao_f1)
                    f1[divisao:-divisao] = lista_mutacao_f1

                if sorteio_mutacao2 <= taxa_mutacao:
                    # realiza mutação na parte do meio do f2 (embaralha)
                    lista_mutacao_f2 = f2[divisao:-divisao]
                    random.shuffle(lista_mutacao_f2)
                    f2[divisao:-divisao] = lista_mutacao_f2

                # adiciona os descendentes gerados em uma lista
                filhos.append(f1)
                filhos.append(f2)

            #limpa a lista que contém as distâncias das sequências e de seus descendentes (para garantir que valores das gerações anteriores não estarão presentes)
            lista_dist_filhos.clear()
            lista_dist.clear()

            # calcula a distância de todos os descendentes gerados
            lista_dist_filhos = dist(filhos, coord_pedidos, qtd_medicamento)

            # Checa se algum descendente criado gerou uma distância menor do que a anterior armazenada em menor_dist (que pode ser de um dos pais selecionados ou de um descendente criado)
            for item in lista_dist_filhos:
                if item <= menor_dist:
                    menor_dist = item
                    seq_menor_dist = filhos[lista_dist_filhos.index(item)]

            # limpa as variáveis para que uma nova geração possa ser criada
            pais_selecionados.clear()
            pais_selecionados.extend(filhos)
            filhos.clear()

            # incrementa a variável para que uma nova geração possa ser criada
            a = a + 1

        # recupera as coordenadas da sequência que obteve a menor distância calculada
        for i in seq_menor_dist:
            coordenadas_4coleta.append(coord_pedidos[i-1])

        # informa ao usuário a menor distância, a sequência correspondente e as coordenadas dos medicamentos na sequência definida
        print('A sequência {} obteve a menor distância de {}' .format(
            seq_menor_dist, menor_dist))
        print('Coordenadas finais: {}' .format(coordenadas_4coleta))

# calcula e informa o tempo de execução do função que gerou todas as possíveis sequências e calculou suas distâncias
tempo_execucao = timeit.timeit(stmt=programa, number=1)
print("Tempo médio de execução: {} segundos" .format(tempo_execucao))

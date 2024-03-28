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
med_pedidos = []  # lista de medicamentos solicitados pelo profissional
coord_pedidos = []  # lista de coordenadas dos medicamentos solicitados
elemento = []  # lista criada para realizar a permutação e definir todas as sequências possíveis para o caso em que a qtd_medicamentos é menor ou igual a 9
listas = []  # lista que irá conter as possíveis sequências-soluções de medicamentos
lista_dist = []  # lista que armazena as distâncias dos pais
lista_dist_filhos = []  # lista que armazena as distâncias dos filhos gerados
pais_selecionados = []  # lista dos pais selecionados por ranking
# lista que armazena as distâncias dos pais selecionados para o cruzamento
dist_pais_selecionados = []
# coordenadas finais para realizar a coleta dos medicamentos solicitados
coordenadas_4coleta = []
filhos = []  # lista dos filhos obtidos no primeiro cruzamento
lista_med = ['acetilcisteina', 'buscopan', 'diazepam', 'levotiroxina 25', 'levotiroxina 50',
             # lista de medicamentos disponíveis nas prateleiras
             'levotiroxina 75', 'gardenal', 'tilenol', 'dorflex', 'alexofedrina', 'plasil', 'dramim', 'ibuprofeno', 'propanolol', 'captopril']
lista_med_solicitado = []  # lista dos medicamentos solicitados
coord_med = [(1, 1), (1, 9), (1, 25), (1, 33), (2, 16),
             # lista das coordenadas dos medicamentos disponíveis nas prateleiras
             (2, 17), (2, 18), (2, 21), (3, 31), (3, 40), (3, 52), (3, 60), (2, 53), (1, 47), (3, 25)]


def dist(lista_indiv, coord_pedidos, qtd_medicamento):
    for j in range(len(lista_indiv)):
        seq = lista_indiv[j]
        # calcula a distância inicial (0,0) até o primeiro ponto
        x1, y1 = coord_pedidos[seq[0]-1]
        dist = math.sqrt((abs(x1 - 0)**2 + (abs(y1 - 0))**2))

        # calcula a distância entre os medicamentos definidos na sequência seq
        for i in range((qtd_medicamento-1)):
            x1, y1 = coord_pedidos[(seq[i]-1)]
            x2, y2 = coord_pedidos[(seq[i+1]-1)]
            dist = math.sqrt((abs(x2 - x1)**2 + (abs(y2 - y1))**2)) + dist

        # calcula a distância do último ponto até o ponto inicial (0,0)
        x2, y2 = coord_pedidos[seq[-1]-1]
        dist = math.sqrt((abs(x2 - 0)**2 + (abs(y2 - 0))**2)) + dist

        lista_dist.append(dist)
    return lista_dist


# profissional define a quantidade de medicamentos a ser coletada
qtd_medicamento = int(
    input('Digite a quantidade de medicamentos a ser coletada: '))

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
        # se o medicamento não for encontrado na lista, é perguntado ao profissional se ele deseja continuar
        print('{} não encontrado. Digite novamente: ' .format(med))
        qtd_medicamento_loop += 1

    h += 1

# print('Coordenadas Medicamentos: {}' .format(coord_pedidos))

# se a quantidade de medicamentos informada pelo usuario for menor que 9, será encontrada a distância para cada solução possível e
# será retornada a sequência que obteve a menor distância
if qtd_medicamento <= 9:
    for i in range(qtd_medicamento):
        elemento.append(i+1)
    permutacoes = itertools.permutations(elemento)

    # recupera todas as possibilidades de sequência-solução
    for permutacao in permutacoes:
        listas.append(permutacao)

    lista_dist = dist(listas, coord_pedidos, qtd_medicamento)

    # armazena a menor distância e a sequência da menor distância selecionada
    menor_dist = min(lista_dist)
    seq_menor_dist = listas[lista_dist.index(menor_dist)]
    # recupera as coordenadas da sequência com menor distância
    for i in seq_menor_dist:
        coordenadas_4coleta.append(coord_pedidos[i-1])

    print('A sequência {} obteve a menor distância de {}' .format(
        seq_menor_dist, menor_dist))
    print('Coordenadas finais: {}' .format(coordenadas_4coleta))

# se a quantidade de medicamentos informada pelo usuário for maior que 9, então será aplicado o algoritmo genético para se obter uma solução ótima
else:
    # cria várias soluções de sequência de medicamentos e as salva em uma lista
    for i in range(15):
        elemento = random.sample(
            range(1, (qtd_medicamento+1)), qtd_medicamento)
        if elemento not in listas:
            listas.append(elemento)

    # para cada sequência-solução que foi criada é calculada a distância total a ser percorrida (função fitness)
    lista_dist = dist(listas, coord_pedidos, qtd_medicamento)

    # print('Pais criados: {}' .format(listas))
    # print('Distancias pais criados: {}' .format(lista_dist))

    # realiza o torneio entre os pais selecionados contidos na lista de pais por meio da comparação entre as distâncias deles
    # caso em que a quantidade de pais é par
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

    # caso em que a quantidade de pais é ímpar (os últimos três pais são comparados juntos)
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

    # print('Pais selecionados: {}' .format(pais_selecionados))
    # print('Dist pais selecionados: {}' .format(dist_pais_selecionados))

    # se a quantidade de pais for ímpar, ele exclui o pai com maior distância para que resulte num número par de pais para ocasionar o crossover
    if (len(pais_selecionados) % 2) != 0:
        pais_selecionados.remove(
            pais_selecionados[dist_pais_selecionados.index(max(dist_pais_selecionados))])
        dist_pais_selecionados.remove(max(dist_pais_selecionados))

    # armazena a menor distância e a sequência da menor distância selecionada
    menor_dist = min(dist_pais_selecionados)
    seq_menor_dist = pais_selecionados[dist_pais_selecionados.index(
        menor_dist)]

    # define a quantidade máxima de gerações
    max_geracao = 20000
    a = 0

    # realiza o processo de criação de filhos pela quantidade de gerações determinadas
    while a <= (max_geracao):

        # separa os pais selecionados por pares para realizar o cruzamento
        w = 0
        for w in range(0, len(pais_selecionados)-1, 2):
            p1 = pais_selecionados[w]
            p2 = pais_selecionados[(w+1)]

            # cria o vetor dos filhos
            f1 = [0]*qtd_medicamento
            f2 = [0]*qtd_medicamento

            # cria as variáveis que são utilizadas no processo de crossover e mutação a cada geração criada
            indices_string_bit_1 = []
            elementosp1_posicao_zeros_string_bit = []
            elementosp2_posicao_zeros_string_bit = []
            indices_elementosp1_ordem_p2 = []
            elementosp1_ordem_p2 = []
            indices_elementosp2_ordem_p1 = []
            elementosp2_ordem_p1 = []

            # cria uma lista com bits aleatórios. O tamanho da lista deve ser igual ao tamanho dos pais
            string_bit = random.choices(range(0, 2), k=qtd_medicamento)

            for i in range(len(string_bit)):
                # recupera a posição dos 1s da lista criada
                if string_bit[i] == 1:
                    indices_string_bit_1.append(i)

                # cria uma lista com os elementos dos pais correspondentes aos 0s da lista de bits
                if string_bit[i] == 0:
                    elementosp1_posicao_zeros_string_bit.append(p1[i])
                    elementosp2_posicao_zeros_string_bit.append(p2[i])

            # copia para os filhos os elementos dos pais referentes às posições dos 1s da lista de bits criada
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

            # processo de mutação
            taxa_mutacao = 0.3
            sorteio_mutacao1 = random.random()
            sorteio_mutacao2 = random.random()

            # recupera um terço da quantidade de medicamentos contida nos filhos. A mutação ocorre no terço do meio
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

            # adiciona os filhos gerados na lista de filhos
            filhos.append(f1)
            filhos.append(f2)

        # print('Filhos gerados: {}' .format(filhos))

        lista_dist_filhos.clear()
        lista_dist.clear()
        # print('Dist filhos gerados antes de gerar: {}' .format(lista_dist_filhos))

        # calcula a distância de todos os filhos gerados
        lista_dist_filhos = dist(filhos, coord_pedidos, qtd_medicamento)

        # print('Dist filhos gerados depois de gerar: {}' .format(lista_dist_filhos))

        # Checa se algum filho criado gerou uma distância menor do que a anterior aramzenada em menor_dist (que pode ser de um dos pais selecionados ou de um filho criado)
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

    for i in seq_menor_dist:
        coordenadas_4coleta.append(coord_pedidos[i-1])

    # print('Coordenadas medicamentos solicitados: {}' .format(coord_pedidos))
    # print('Distancia pais selecionados: {}' .format(dist_pais_selecionados))
    print('A sequência {} obteve a menor distância de {}' .format(
        seq_menor_dist, menor_dist))
    print('Coordenadas finais: {}' .format(coordenadas_4coleta))

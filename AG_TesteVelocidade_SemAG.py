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
lista_dist = []  # lista que armazena as distâncias de todas as possíveis sequências
coordenadas_4coleta = []  # coordenadas da sequência que obteve menor distância
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
    elemento = []
    coordenadas_4coleta = []

    # realiza permutação e gera todas as possibilidades de sequências de coleta de medicamentos
    for i in range(qtd_medicamento):
        elemento.append(i+1)
    permutacoes = itertools.permutations(elemento)

    # recupera e armazena todas as possíveis sequência de coleta em uma lista
    for permutacao in permutacoes:
        listas.append(permutacao)

    # calcula, usando a funçã fitness criada, e armazena as distâncias de cada sequência gerada anteriormente
    lista_dist = dist(listas, coord_pedidos, qtd_medicamento)

    # armazena a menor distância e a sequência da menor distância verificada
    menor_dist = min(lista_dist)
    seq_menor_dist = listas[lista_dist.index(menor_dist)]

    # recupera as coordenadas da sequência com menor distância
    for i in seq_menor_dist:
        coordenadas_4coleta.append(coord_pedidos[i-1])

    # informa ao usuário a menor distância, a sequência correspondente e as coordenadas dos medicamentos na sequência definida
    print('A sequência {} obteve a menor distância de {}' .format(
        seq_menor_dist, menor_dist))
    print('Coordenadas finais: {}' .format(coordenadas_4coleta))


# calcula e informa o tempo de execução do função que gerou todas as possíveis sequências e calculou suas distâncias
tempo_execucao = timeit.timeit(stmt=programa, number=1)
print("Tempo médio de execução: {} segundos" .format(tempo_execucao))

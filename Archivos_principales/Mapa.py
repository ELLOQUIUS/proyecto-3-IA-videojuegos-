import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import random
from Clases.funciones import pintar_mapa,movimiento_asig_vetadas,crearGrafo,crearGrafoTactico,rotate_polygon,dibujar_linea,nodo_actual
from Clases.Kinematic import Kinematic
from Grafo import Graph
from PathfindingAStar import pathfindAStar,Heuristic
from Clases.Seek import Seek
from Clases.Kinematic import Kinematic
from DecisionTree import DecisionTreeNodeLimpiador,ActionLimpiador,DecisionTreeNodeLadron,DecisionTreeNodeBailador

base = 15      # Parametro modificable
altura = 20    # Parametro modificable
arrow = [
    pygame.Vector2(0, -altura),  # Vértice superior
    pygame.Vector2(-base / 2, 0),  # Vértice inferior izquierdo
    pygame.Vector2(base / 2, 0)  # Vértice inferior derecho
]

tamaño_cuadricula = 40  # Parametro modificable

ancho = 0
alto = 0
pygame.init()
temp1 = int(input("Elije el ancho del mapa: "))
temp2 = int(input("Elije el alto del mapa: "))

radio_de_aceptacion = 20.5  # Parametro modificable. Aumentarlo si se aumenta la velocidad
nodos_bloqueados = [3,7,13,23,27,33,43,47,48,49,50,53,56,60,62,63,70,73,76,90,91,93,96,97,98,99,105,125,140,
                    141,142,145,146,147,148,150,151,153,156,157,158,162,176,182,185,186,187,188,190,191,192,
                    193,196,205,210,216,225,230,233,236,242,245,248,249,250,253,256,262,265,270,271,272,273,
                    276,277,278,285,305,306,307,320,321,322,327,330,334,336,337,338,339,347,350,354]

columnas = 0
filas = 0
while ancho < temp1:
    ancho += tamaño_cuadricula
    columnas += 1
while alto < temp2:
    alto += tamaño_cuadricula
    filas += 1

ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Mapa")
fuente = pygame.font.Font(None, 20)

# Eleccion de las posiciones iniciales del target, el personaje, la recarga, la zona de guardar E y la zona de baile. Cada una es diferente
numero_aleatorio_1 = random.randint(0, filas*columnas-1)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_1 == nodos_bloqueados[i]:
        numero_aleatorio_1 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_2 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_1)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_2 == nodos_bloqueados[i]:
        numero_aleatorio_2 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_3 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_2)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_3 == nodos_bloqueados[i]:
        numero_aleatorio_3 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_4 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_3)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_4 == nodos_bloqueados[i]:
        numero_aleatorio_4 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_5 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_4)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_5 == nodos_bloqueados[i]:
        numero_aleatorio_5 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

# Voy a querer tambien 12 puntos ventajosos y 12 puntos desventajosos
# Ventajosos:
numero_aleatorio_6 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_5)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_6 == nodos_bloqueados[i]:
        numero_aleatorio_6 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_7 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_6)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_7 == nodos_bloqueados[i]:
        numero_aleatorio_7 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_8 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_7)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_8 == nodos_bloqueados[i]:
        numero_aleatorio_8 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

# Desventajosos
numero_aleatorio_9 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_8)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_9 == nodos_bloqueados[i]:
        numero_aleatorio_9 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_10 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_9)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_10 == nodos_bloqueados[i]:
        numero_aleatorio_10 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_11 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_10)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_11 == nodos_bloqueados[i]:
        numero_aleatorio_11 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_12 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_11)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_12 == nodos_bloqueados[i]:
        numero_aleatorio_12 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_13 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_12)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_13 == nodos_bloqueados[i]:
        numero_aleatorio_13 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_14 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_13)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_14 == nodos_bloqueados[i]:
        numero_aleatorio_14 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_15 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_14)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_15 == nodos_bloqueados[i]:
        numero_aleatorio_15 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_16 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_15)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_16 == nodos_bloqueados[i]:
        numero_aleatorio_16 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_17 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_16)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_17 == nodos_bloqueados[i]:
        numero_aleatorio_17 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_18 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_17)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_18 == nodos_bloqueados[i]:
        numero_aleatorio_18 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_19 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_18)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_19 == nodos_bloqueados[i]:
        numero_aleatorio_19 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_20 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_19)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_20 == nodos_bloqueados[i]:
        numero_aleatorio_20 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_21 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_20)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_21 == nodos_bloqueados[i]:
        numero_aleatorio_21 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_22 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_21)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_22 == nodos_bloqueados[i]:
        numero_aleatorio_22 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_23 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_22)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_23 == nodos_bloqueados[i]:
        numero_aleatorio_23 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_24 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_23)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_24 == nodos_bloqueados[i]:
        numero_aleatorio_24 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_25 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_24)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_25 == nodos_bloqueados[i]:
        numero_aleatorio_25 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_26 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_25)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_26 == nodos_bloqueados[i]:
        numero_aleatorio_26 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_27 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_26)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_27 == nodos_bloqueados[i]:
        numero_aleatorio_27 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_28 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_27)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_28 == nodos_bloqueados[i]:
        numero_aleatorio_28 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

numero_aleatorio_29 = random.randint(0, filas*columnas-1)
nodos_bloqueados.append(numero_aleatorio_28)
i = 0
while i < len(nodos_bloqueados):
    if numero_aleatorio_29 == nodos_bloqueados[i]:
        numero_aleatorio_29 = random.randint(0, filas*columnas-1)
        i = -1
    i += 1

nodos_bloqueados.pop()
nodos_bloqueados.pop()
nodos_bloqueados.pop()    
nodos_bloqueados.pop()
nodos_bloqueados.pop()
nodos_bloqueados.pop()    
nodos_bloqueados.pop()
nodos_bloqueados.pop()
nodos_bloqueados.pop()    
nodos_bloqueados.pop()
nodos_bloqueados.pop()
nodos_bloqueados.pop()    
nodos_bloqueados.pop() 
nodos_bloqueados.pop()
nodos_bloqueados.pop()    
nodos_bloqueados.pop()  
nodos_bloqueados.pop()
nodos_bloqueados.pop()    
nodos_bloqueados.pop() 
nodos_bloqueados.pop()
nodos_bloqueados.pop()    
nodos_bloqueados.pop() 
nodos_bloqueados.pop()
nodos_bloqueados.pop()    
nodos_bloqueados.pop() 
nodos_bloqueados.pop()
nodos_bloqueados.pop()    
nodos_bloqueados.pop() 

nodo_objetivo = numero_aleatorio_1    # Parametro modificable
nodo_inicial = numero_aleatorio_2    # Parametro modificable
nodo_recarga = numero_aleatorio_3    # Parametro modificable'''
nodo_guardar_E = numero_aleatorio_4    # Parametro modificable'''
nodo_zona_baile = numero_aleatorio_5    # Parametro modificable'''

# Agrego los nodos ventajosos y desventajosos
nodos_ventajosos = []
nodos_ventajosos.append(numero_aleatorio_6)
nodos_ventajosos.append(numero_aleatorio_7)
nodos_ventajosos.append(numero_aleatorio_8)
nodos_ventajosos.append(numero_aleatorio_21)
nodos_ventajosos.append(numero_aleatorio_22)
nodos_ventajosos.append(numero_aleatorio_23)
nodos_ventajosos.append(numero_aleatorio_24)
nodos_ventajosos.append(numero_aleatorio_25)
nodos_ventajosos.append(numero_aleatorio_26)
nodos_ventajosos.append(numero_aleatorio_27)
nodos_ventajosos.append(numero_aleatorio_28)
nodos_ventajosos.append(numero_aleatorio_29)
nodos_ventajosos.sort()
nodos_ventajosos.append(-1) # Agrego un ultimo valor para que cuando pinte el mapa no tenga problema al evaluar el len del arreglo
nodos_desventajosos = []
nodos_desventajosos.append(numero_aleatorio_9)
nodos_desventajosos.append(numero_aleatorio_10)
nodos_desventajosos.append(numero_aleatorio_11)
nodos_desventajosos.append(numero_aleatorio_12)
nodos_desventajosos.append(numero_aleatorio_13)
nodos_desventajosos.append(numero_aleatorio_14)
nodos_desventajosos.append(numero_aleatorio_15)
nodos_desventajosos.append(numero_aleatorio_16)
nodos_desventajosos.append(numero_aleatorio_17)
nodos_desventajosos.append(numero_aleatorio_18)
nodos_desventajosos.append(numero_aleatorio_19)
nodos_desventajosos.append(numero_aleatorio_20)
nodos_desventajosos.sort()
nodos_desventajosos.append(-1) # Agrego un ultimo valor para que cuando pinte el mapa no tenga problema al evaluar el len del arreglo

'''nodo_objetivo = 21    
nodo_inicial = 121    
nodo_recarga = 61 '''

temp = 0
pos_i_personaje = 0
pos_j_personaje = 0
pos_i_objetivo = 0
pos_j_objetivo = 0
pos_i_recarga = 0
pos_j_recarga = 0
pos_i_guardar = 0
pos_j_guardar = 0
pos_i_baile = 0
pos_j_baile = 0
# Busco automaticamente la posicion i,j del personaje
pos_j_personaje = nodo_inicial % columnas;
while temp + pos_j_personaje != nodo_inicial:
    temp += columnas
    pos_i_personaje += 1

# Busco automaticamente la posicion i,j del objetivo
temp = 0
pos_j_objetivo = nodo_objetivo % columnas;
while temp + pos_j_objetivo != nodo_objetivo:
    temp += columnas
    pos_i_objetivo += 1

# Busco automaticamente la posicion i,j de la recarga
temp = 0
pos_j_recarga = nodo_recarga % columnas;
while temp + pos_j_recarga != nodo_recarga:
    temp += columnas
    pos_i_recarga += 1

# Busco automaticamente la posicion i,j de la zona de guardar E
temp = 0
pos_j_guardar = nodo_guardar_E % columnas;
while temp + pos_j_guardar != nodo_guardar_E:
    temp += columnas
    pos_i_guardar += 1

# Busco automaticamente la posicion i,j de la zona de baile
temp = 0
pos_j_baile = nodo_zona_baile % columnas;
while temp + pos_j_baile != nodo_zona_baile:
    temp += columnas
    pos_i_baile += 1

# Agente que limpia
posicion_x_objetivo = pos_j_objetivo
posicion_y_objetivo = pos_i_objetivo
posicion_x_personaje = pos_j_personaje
posicion_y_personaje = pos_i_personaje
posicion_x_recarga = pos_j_recarga
posicion_y_recarga = pos_i_recarga

# Agente que roba (la posicion inicial del ladron y la zona de guardar energia seran iguales)
posicion_x_ladron = pos_j_guardar
posicion_y_ladron = pos_i_guardar
posicion_x_guardar = pos_j_guardar
posicion_y_guardar = pos_i_guardar

# Agente que baila (la posicion inicial del bailador y la zona de baile seran iguales)
posicion_x_bailador = pos_j_baile
posicion_y_bailador = pos_i_baile
posicion_x_zona_baile = pos_j_baile
posicion_y_zona_baile = pos_i_baile

# Agente que limpia 
limpiador = Kinematic([(tamaño_cuadricula*posicion_x_personaje)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_personaje)+tamaño_cuadricula/2],[0,0],0,0) # Personaje (Seek) 
target = Kinematic([(tamaño_cuadricula*posicion_x_objetivo)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_objetivo)+tamaño_cuadricula/2],[0,0],0,0) # Target (Seek)
target_aux = Kinematic([0,0],[0,0],0,0) # Target (Seek)
targetRecarga = Kinematic([(tamaño_cuadricula*posicion_x_recarga)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_recarga)+tamaño_cuadricula/2],[0,0],0,0)

# Agente que roba
ladron = Kinematic([(tamaño_cuadricula*posicion_x_ladron)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_ladron)+tamaño_cuadricula/2],[0,0],0,0) # ladron (Seek)
targetLadron = Kinematic([(tamaño_cuadricula*posicion_x_personaje)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_personaje)+tamaño_cuadricula/2],[0,0],0,0) # Target (Seek)
targetLadron_aux = Kinematic([0,0],[0,0],0,0) # Target (Seek)
targetGuardarE = Kinematic([(tamaño_cuadricula*posicion_x_guardar)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_guardar)+tamaño_cuadricula/2],[0,0],0,0)
energiaGuardadaEnZ = [0]

# Agente que roba
bailador = Kinematic([(tamaño_cuadricula*posicion_x_bailador)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_bailador)+tamaño_cuadricula/2],[0,0],0,0) # bailador (Seek)
targetBailador = Kinematic([(tamaño_cuadricula*posicion_x_personaje)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_personaje)+tamaño_cuadricula/2],[0,0],0,0) # Target (Seek)
targetBailador_aux = Kinematic([0,0],[0,0],0,0) # Target (Seek)
targetZonaBaile = Kinematic([(tamaño_cuadricula*posicion_x_zona_baile)+tamaño_cuadricula/2,(tamaño_cuadricula*posicion_y_zona_baile)+tamaño_cuadricula/2],[0,0],0,0)
energiaBailador = [0]

ite = 0
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    ventana.fill((211, 211, 211))

    velocity = 7

    # Descomentar estas tres lineas si se quiere mover el cuadrado 
    #keys = pygame.key.get_pressed() # Para agarrar las teclas del teclado y mover el objetivo
    #vetadas = [False,False,False,False] # Vector auxiliar para cuando choque con un borde
    #movimiento_asig_vetadas(keys,vetadas,ancho,alto,target,velocity)

    num = pintar_mapa(ventana,ancho,alto,tamaño_cuadricula,nodos_bloqueados,nodos_ventajosos,nodos_desventajosos,1)

    ite += 1
    # Creo el grafo asociado:
    if ite == 1:
        grafo = Graph()
        grafo = crearGrafo(grafo,num[0],num[1],nodos_bloqueados)

        grafoTactico = Graph()
        grafoTactico = crearGrafoTactico(grafoTactico,num[0],num[1],nodos_bloqueados,nodos_ventajosos,nodos_desventajosos)

        # Limpiador Normal
        heuristicaLimpiador = Heuristic(grafo.vectorGrafo[nodo_objetivo])
        resultLimpiador = pathfindAStar(grafo,grafo.vectorGrafo[nodo_inicial],grafo.vectorGrafo[nodo_objetivo],heuristicaLimpiador)

        # Ladron. El nodo objetivo de el sera en el primer frame el nodo inicial del limpiador
        heuristicaLadron = Heuristic(grafo.vectorGrafo[nodo_inicial])
        resultLadron = pathfindAStar(grafo,grafo.vectorGrafo[nodo_guardar_E],grafo.vectorGrafo[nodo_inicial],heuristicaLadron) 
        # Ladron Tactico. El nodo objetivo de el sera en el primer frame el nodo inicial del limpiador
        heuristicaLadronTac = Heuristic(grafoTactico.vectorGrafo[nodo_inicial])
        resultLadronTac = pathfindAStar(grafoTactico,grafoTactico.vectorGrafo[nodo_guardar_E],grafoTactico.vectorGrafo[nodo_inicial],heuristicaLadronTac) 


        # Bailador. El nodo objetivo de el sera en el primer frame la zona de guardado de energia
        heuristicaBailador = Heuristic(grafo.vectorGrafo[nodo_guardar_E])
        resultBailador = pathfindAStar(grafo,grafo.vectorGrafo[nodo_zona_baile],grafo.vectorGrafo[nodo_guardar_E],heuristicaBailador) 
        # Bailador Tactico. El nodo objetivo de el sera en el primer frame la zona de guardado de energia
        heuristicaBailadorTac = Heuristic(grafoTactico.vectorGrafo[nodo_guardar_E])
        resultBailadorTac = pathfindAStar(grafoTactico,grafoTactico.vectorGrafo[nodo_zona_baile],grafoTactico.vectorGrafo[nodo_guardar_E],heuristicaBailadorTac) 

        
        # Limpiador
        if len(resultLimpiador) > 0:
            target_aux.position[0] = (resultLimpiador[0].toNode.vectorPosicion[1] * tamaño_cuadricula) + tamaño_cuadricula/2
            target_aux.position[1] = (resultLimpiador[0].toNode.vectorPosicion[0] * tamaño_cuadricula) + tamaño_cuadricula/2
        klimpiador = Seek(limpiador,target_aux,0.03) # Busqueda del personaje al target (Seek)
        
        # Ladron. Creo que esto nunca va a pasar para el ladron, ya que las posiciones iniciales de él 
        # y el limpiador siempre seran distintas, con lo cual el path resultado sera de len > 0 siempre
        if len(resultLadron) > 0:
            targetLadron_aux.position[0] = (resultLadron[0].toNode.vectorPosicion[1] * tamaño_cuadricula) + tamaño_cuadricula/2
            targetLadron_aux.position[1] = (resultLadron[0].toNode.vectorPosicion[0] * tamaño_cuadricula) + tamaño_cuadricula/2
        kladron = Seek(ladron,targetLadron_aux,0.03) # Busqueda del personaje al target (Seek)

        # Bailador.
        if len(resultBailador) > 0:
            targetBailador_aux.position[0] = (resultBailador[0].toNode.vectorPosicion[1] * tamaño_cuadricula) + tamaño_cuadricula/2
            targetBailador_aux.position[1] = (resultBailador[0].toNode.vectorPosicion[0] * tamaño_cuadricula) + tamaño_cuadricula/2
        kbailador = Seek(bailador,targetBailador_aux,0.03) # Busqueda del personaje al target (Seek)


        # Arbol de desicion del limpiador
        enerLimpiador = 40 
        energiaLimpiador = [enerLimpiador]
        ir_a_recargar = [False]
        camino_actual_limpiador = [0]
        nodo_inicial_vec = [nodo_inicial]
        arbolDelLimpiador = DecisionTreeNodeLimpiador(limpiador,target,nodo_inicial_vec,klimpiador,target_aux,energiaLimpiador,radio_de_aceptacion,tamaño_cuadricula,resultLimpiador,camino_actual_limpiador,grafo.vectorGrafo,enerLimpiador,ir_a_recargar)        
        accionLimpiador = arbolDelLimpiador.makeDecision()
        if accionLimpiador.opcion == 0:
            nodo_inicial = accionLimpiador.nodo_inicial[0]
            accionLimpiador.camino_actual[0] = 0
            resultLimpiador = pathfindAStar(grafo,grafo.vectorGrafo[nodo_inicial],grafo.vectorGrafo[nodo_objetivo],heuristicaLimpiador)
            arbolDelLimpiador.path_result = resultLimpiador
        
        # Arbol de desicion del ladron (en este caso no me importa ya que el 
        # importante es el tactico)
        '''enerLadron = 0
        energiaLadron = [enerLadron]
        ir_a_guardar = [False]
        camino_actual_ladron = [0] # En este caso solo lo uso para dibujar a linea
        moverse = [0]
        arbolDelLadron = DecisionTreeNodeLadron(ladron,limpiador,kladron,targetLadron_aux,energiaLadron,radio_de_aceptacion,tamaño_cuadricula,resultLadron,grafo,ir_a_guardar,arbolDelLimpiador,columnas,targetGuardarE,energiaGuardadaEnZ,moverse)                   
        '''# Arbol de desicion del ladron Tactico
        enerLadronTac = 0
        energiaLadronTac = [enerLadronTac]
        ir_a_guardarTac = [False]
        camino_actual_ladronTac = [0] # En este caso solo lo uso para dibujar a linea
        moverseTac = [0]
        arbolDelLadronTac = DecisionTreeNodeLadron(ladron,limpiador,kladron,targetLadron_aux,energiaLadronTac,radio_de_aceptacion,tamaño_cuadricula,resultLadronTac,grafoTactico,ir_a_guardarTac,arbolDelLimpiador,columnas,targetGuardarE,energiaGuardadaEnZ,moverseTac)               
        

        # Arbol de desicion del bailador (en este caso no me importa ya que el 
        # importante es el tactico)
        '''enerBailador = 0
        esperando = [0]
        energiaBailador = [enerBailador]
        camino_actual_Bailador = [0] # En este caso solo lo uso para dibujar a linea
        arbolDelBailador = DecisionTreeNodeBailador(bailador,kbailador,targetBailador_aux,energiaBailador,radio_de_aceptacion,tamaño_cuadricula,resultBailador,grafo,columnas,targetGuardarE,targetZonaBaile,camino_actual_Bailador,energiaGuardadaEnZ,esperando)               
        '''# Arbol de desicion del bailador tactico
        enerBailadorTac = 0
        esperandoTac = [0]
        energiaBailadorTac = [enerBailadorTac]
        camino_actual_BailadorTac = [0] # En este caso solo lo uso para dibujar a linea
        arbolDelBailadorTac = DecisionTreeNodeBailador(bailador,kbailador,targetBailador_aux,energiaBailadorTac,radio_de_aceptacion,tamaño_cuadricula,resultBailadorTac,grafoTactico,columnas,targetGuardarE,targetZonaBaile,camino_actual_BailadorTac,energiaGuardadaEnZ,esperandoTac)               
        
    
    # -------------------------------------------------------------------------------------------
    # Evaluo que decision debo tomar para el limpiador
    accionLimpiador = arbolDelLimpiador.makeDecision()

    # Si estoy en el objetivo, me tepeo
    if accionLimpiador.opcion == 0:
        nodo_inicial = accionLimpiador.nodo_inicial[0]
        heuristicaLimpiador = heuristicaLimpiador = Heuristic(grafo.vectorGrafo[nodo_objetivo])
        resultLimpiador = pathfindAStar(grafo,grafo.vectorGrafo[nodo_inicial],grafo.vectorGrafo[nodo_objetivo],heuristicaLimpiador)
        try:
            target_aux.position[0] = (resultLimpiador[0].toNode.vectorPosicion[1] * tamaño_cuadricula) + tamaño_cuadricula/2
            target_aux.position[1] = (resultLimpiador[0].toNode.vectorPosicion[0] * tamaño_cuadricula) + tamaño_cuadricula/2
        except:
            #resultLimpiador = []
            print(len(resultLimpiador))
            print("Reinicie el programa")
            exit
             
        camino_actual_limpiador = [0]
        nodo_inicial_vec = [nodo_inicial]
        # Creo otro arbol para p1, ahora con otro pathfinding
        arbolDelLimpiador = DecisionTreeNodeLimpiador(limpiador,target,nodo_inicial_vec,klimpiador,target_aux,energiaLimpiador,radio_de_aceptacion,tamaño_cuadricula,resultLimpiador,camino_actual_limpiador,grafo.vectorGrafo,enerLimpiador,ir_a_recargar)
    # Si no estoy en el objetivo, hago path al objetivo
    
    # Si no tengo energia, mi objetivo sera el nodo de recarga y voy a recargar la energia.
    elif accionLimpiador.opcion == 2:
        # Calculo el nodo actual donde p1 se quedó sin energia
        nodo_actual_p1 = nodo_actual(limpiador.position[0],limpiador.position[1],columnas,tamaño_cuadricula)
        # Calculo el pathfinding entre el nodo actual de p1 y el nodo de recarga
        heuristicaLimpiador = heuristicaLimpiador = Heuristic(grafo.vectorGrafo[nodo_recarga]) 
        resultLimpiador = pathfindAStar(grafo,grafo.vectorGrafo[nodo_actual_p1],grafo.vectorGrafo[nodo_recarga],heuristicaLimpiador)

        # En caso de que justo pase que se me acabe la energia cuando estoy en el nodo de recargar energia
        if len(resultLimpiador) > 0:
            target_aux.position[0] = (resultLimpiador[0].toNode.vectorPosicion[1] * tamaño_cuadricula) + tamaño_cuadricula/2
            target_aux.position[1] = (resultLimpiador[0].toNode.vectorPosicion[0] * tamaño_cuadricula) + tamaño_cuadricula/2
            klimpiador = Seek(limpiador,target_aux,0.03) # Busqueda del personaje al target (Seek)
        camino_actual_limpiador = [0]
        nodo_inicial_vec = [nodo_actual_p1]
        arbolDelLimpiador = DecisionTreeNodeLimpiador(limpiador,targetRecarga,nodo_inicial_vec,klimpiador,target_aux,energiaLimpiador,radio_de_aceptacion,tamaño_cuadricula,resultLimpiador,camino_actual_limpiador,grafo.vectorGrafo,enerLimpiador,ir_a_recargar)        
    # -------------------------------------------------------------------------------------------
    

    # -------------------------------------------------------------------------------------------
    # Evaluo que decision debo tomar para el ladron
    # accionLadron = arbolDelLadron.makeDecision()

    # Evaluo que decision debo tomar para el ladron tactico
    accionLadronTac = arbolDelLadronTac.makeDecision()

    # Evaluo el camino normal del ladron para poder dibujarlo luego
    resultLadron = []
    if len(accionLadronTac.path_result) > 0:
        if accionLadronTac.moverse[0] == 0:
            if accionLadronTac.path_result[len(accionLadronTac.path_result)-1].toNode.nombre == nodo_guardar_E:
                nod_actual = nodo_actual(accionLadronTac.personaje.position[0],accionLadronTac.personaje.position[1],columnas,tamaño_cuadricula)
                heuristicaLadron = Heuristic(grafo.vectorGrafo[nodo_guardar_E])
                resultLadron = pathfindAStar(grafo,grafo.vectorGrafo[nod_actual],grafo.vectorGrafo[nodo_guardar_E],heuristicaLadron) 
            else:
                nod_actual = nodo_actual(accionLadronTac.personaje.position[0],accionLadronTac.personaje.position[1],columnas,tamaño_cuadricula)
                nod_limp = nodo_actual(accionLimpiador.personaje.position[0],accionLimpiador.personaje.position[1],columnas,tamaño_cuadricula)
                heuristicaLadron = Heuristic(grafo.vectorGrafo[nod_limp])
                resultLadron = pathfindAStar(grafo,grafo.vectorGrafo[nod_actual],grafo.vectorGrafo[nod_limp],heuristicaLadron) 
        
           
    # -------------------------------------------------------------------------------------------
    # Evaluo que decision debo tomar para el bailador
    # accionBailador = arbolDelBailador.makeDecision()

    # Evaluo que decision debo tomar para el bailador tactico
    accionBailadorTac = arbolDelBailadorTac.makeDecision()

    # Evaluo el camino normal del bailador para poder dibujarlo luego
    resultBailador = []
    if len(accionBailadorTac.path_result) > 0:
        if accionBailadorTac.esperando[0] == 0:
            if accionBailadorTac.path_result[len(accionBailadorTac.path_result)-1].toNode.nombre == nodo_guardar_E:
                nod_actual = nodo_actual(accionBailadorTac.personaje.position[0],accionBailadorTac.personaje.position[1],columnas,tamaño_cuadricula)
                heuristicaBailador= Heuristic(grafo.vectorGrafo[nodo_guardar_E])
                resultBailador = pathfindAStar(grafo,grafo.vectorGrafo[nod_actual],grafo.vectorGrafo[nodo_guardar_E],heuristicaBailador) 
            else:
                nod_actual = nodo_actual(accionBailadorTac.personaje.position[0],accionBailadorTac.personaje.position[1],columnas,tamaño_cuadricula)
                heuristicaBailador = Heuristic(grafo.vectorGrafo[nodo_zona_baile])
                resultBailador = pathfindAStar(grafo,grafo.vectorGrafo[nod_actual],grafo.vectorGrafo[nodo_zona_baile],heuristicaBailador) 
    
    
    # Limpiador
    rotated_arrow4 = rotate_polygon(arrow, klimpiador.character.orientation + 90) # Seek '''   
    arrow_points4 = [([limpiador.position[0],limpiador.position[1]] + point) for point in rotated_arrow4] # Seek'''    
    pygame.draw.polygon(ventana, (0, 0, 255), arrow_points4) # Seek '''  
    pygame.draw.rect(ventana, (255, 100, 10), (target.position[0]-15, target.position[1]-15, 30, 30)) # Seek '''
    pygame.draw.rect(ventana, (0, 150, 205), (targetRecarga.position[0]-15, targetRecarga.position[1]-15, 30, 30)) # Seek '''
    
    # Ladron
    rotated_arrowLadronTac = rotate_polygon(arrow, accionLadronTac.kin.character.orientation + 90) # Seek '''   
    arrow_pointsLadronTac = [([ladron.position[0],ladron.position[1]] + point) for point in rotated_arrowLadronTac] # Seek'''    
    pygame.draw.polygon(ventana, (35, 18, 21), arrow_pointsLadronTac) # Seek ''' 
    pygame.draw.rect(ventana, (100, 8, 28), (targetGuardarE.position[0]-15, targetGuardarE.position[1]-15, 30, 30)) # Seek '''

    # Bailador
    rotated_arrowBailadorTac = rotate_polygon(arrow, accionBailadorTac.kin.character.orientation + 90) # Seek '''   
    arrow_pointsBailadorTac = [([bailador.position[0],bailador.position[1]] + point) for point in rotated_arrowBailadorTac] # Seek'''    
    pygame.draw.polygon(ventana, (105, 180, 21), arrow_pointsBailadorTac) # Seek ''' 
    pygame.draw.rect(ventana, (100, 80, 200), (targetZonaBaile.position[0]-15, targetZonaBaile.position[1]-15, 30, 30)) # Seek '''


    # Limpiador
    if accionLimpiador.energia[0] < enerLimpiador/3:
        energiaLimpiadorText = fuente.render(str(accionLimpiador.energia[0]), True, (255, 0, 0))
    elif accionLimpiador.energia[0] > enerLimpiador/3 and accionLimpiador.energia[0] < enerLimpiador/3 + enerLimpiador/3:
        energiaLimpiadorText = fuente.render(str(accionLimpiador.energia[0]), True, (255, 165, 0))
    else:
        energiaLimpiadorText = fuente.render(str(accionLimpiador.energia[0]), True, (0, 255, 0))
    ventana.blit(energiaLimpiadorText, (limpiador.position[0]-15, limpiador.position[1]-25))

    # Ladron
    if accionLadronTac.energia[0] == 0:
        if accionLadronTac.moverse[0] == 0:
            energiaLadronTacText = fuente.render(str(accionLadronTac.energia[0]), True, (255, 0, 0))
        else:
            energiaLadronTacText = fuente.render("Esperando...", True, (120, 120, 120))
    else:
        energiaLadronTacText = fuente.render(str(accionLadronTac.energia[0]), True, (0, 255, 0))    
    ventana.blit(energiaLadronTacText, (ladron.position[0]-15, ladron.position[1]-25))
    
    # Bailador
    if accionBailadorTac.energia[0] <= 0:
        if accionBailadorTac.esperando[0] == 0:           
            energiaBailadorTacText = fuente.render(str(round(accionBailadorTac.energia[0])), True, (255, 0, 0))
        else:
            energiaBailadorTacText = fuente.render("Esperando...", True, (120, 120, 120))
    else:
        if accionBailadorTac.esperando[0] == 0:
            energiaBailadorTacText = fuente.render(str(round(accionBailadorTac.energia[0])), True, (0, 255, 0))
        else:
            energiaBailadorTacText = fuente.render("Esperando...", True, (120, 120, 120))
    ventana.blit(energiaBailadorTacText, (bailador.position[0]-15, bailador.position[1]-25))

    # Energia en la zona de guardado
    if energiaGuardadaEnZ[0] == 0:
        energiaGuardadaEnZText = fuente.render(str(energiaGuardadaEnZ[0]), True, (255, 0, 0))
    else:
        energiaGuardadaEnZText = fuente.render(str(energiaGuardadaEnZ[0]), True, (0, 255, 0))
    ventana.blit(energiaGuardadaEnZText, (targetGuardarE.position[0]-5, targetGuardarE.position[1]-5))

    # Limpiador
    dibujar_linea(ventana,resultLimpiador,camino_actual_limpiador[0],tamaño_cuadricula,0)
    
    # Ladron
    dibujar_linea(ventana,resultLadron,0,tamaño_cuadricula,1)
    # Ladron Tactico
    dibujar_linea(ventana,accionLadronTac.path_result,camino_actual_ladronTac[0],tamaño_cuadricula,3)
    

    # Bailador
    dibujar_linea(ventana,resultBailador,0,tamaño_cuadricula,2)
    # Bailador Tactico
    dibujar_linea(ventana,accionBailadorTac.path_result,camino_actual_BailadorTac[0],tamaño_cuadricula,4)


    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

import random
from Clases.funciones import nodo_actual
from PathfindingAStar import pathfindAStar,Heuristic
from Clases.Seek import Seek

# -----------------------------------------------------------------------------------------------
# Limpiador
class ActionLimpiador:
    def __init__(self,personaje,objetivo,nodo_inicial,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,camino_actual,vectorGrafo,recarga,ir_a_recargar,opcion):
        self.personaje = personaje
        self.objetivo = objetivo
        self.nodo_inicial = nodo_inicial
        self.kin = kin
        self.objetivoAUX = objetivoAUX
        self.energia = energia
        self.radio_de_aceptacion = radio_de_aceptacion
        self.tamaño_cuadricula = tamaño_cuadricula
        self.path_result = path_result
        self.camino_actual = camino_actual
        self.vectorGrafo = vectorGrafo
        self.recarga = recarga # Entero
        self.ir_a_recargar = ir_a_recargar
        self.opcion = opcion
        # Si ya llegue al nodo objetivo, cambio la posicion del personaje de manera aleatoria
        if opcion == 0:
            numero_aleatorio = random.randint(0, len(self.vectorGrafo)-1)
            while self.vectorGrafo[numero_aleatorio].tipo == 1:
                numero_aleatorio = random.randint(0, len(self.vectorGrafo)-1)
            self.personaje.position[0] = (self.tamaño_cuadricula * self.vectorGrafo[numero_aleatorio].vectorPosicion[1]) + self.tamaño_cuadricula/2
            self.personaje.position[1] = (self.tamaño_cuadricula * self.vectorGrafo[numero_aleatorio].vectorPosicion[0]) + self.tamaño_cuadricula/2 
            self.nodo_inicial[0] = numero_aleatorio
            self.camino_actual[0] = 0
            # Si ya estoy en el nodo para recargar y tengo que recargar, recargo la energia
            if self.ir_a_recargar[0] == True:
                self.energia[0] = recarga
                self.ir_a_recargar[0] = False

        # Si aun no llegue al nodo objetivo y aun tengo energia, hago el pathfinding a el nodo objetivo
        elif opcion == 1:
            if (self.personaje.position[0] <= self.objetivoAUX.position[0] + self.radio_de_aceptacion and self.personaje.position[0] >= self.objetivoAUX.position[0] - self.radio_de_aceptacion) and (self.personaje.position[1] >= self.objetivoAUX.position[1] - self.radio_de_aceptacion and self.personaje.position[1] <= self.objetivoAUX.position[1] + self.radio_de_aceptacion):
                self.objetivoAUX.position[0] = (self.tamaño_cuadricula * self.path_result[self.camino_actual[0]].toNode.vectorPosicion[1]) + self.tamaño_cuadricula/2
                self.objetivoAUX.position[1] = (self.tamaño_cuadricula * self.path_result[self.camino_actual[0]].toNode.vectorPosicion[0]) + self.tamaño_cuadricula/2
                self.kin.target = objetivoAUX
                self.camino_actual[0] += 1
                if self.energia[0] > 0:    
                    self.energia[0] -= 1       
            seek = self.kin.getSteering() # Me da un SteeringOutput. Realiza la busqueda (Seek) del personaje al target
            self.personaje.update(seek,0.4,2)
        else:
            self.ir_a_recargar[0] = True

    def makeDecision(self): # -> DecisionTreeNode:
        return self
    
class Limpiador_decision:
    def __init__(self,personaje,objetivo,nodo_inicial,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,camino_actual,vectorGrafo,recarga,ir_a_recargar):
        self.personaje = personaje # Personaje
        self.objetivo = objetivo # Objetivo
        self.nodo_inicial = nodo_inicial # entero
        self.kin = kin # SteringOutput  
        self.objetivoAUX = objetivoAUX # Objetivo
        self.energia = energia # Entero 
        self.radio_de_aceptacion = radio_de_aceptacion # float
        self.tamaño_cuadricula = tamaño_cuadricula # entero
        self.path_result = path_result # Vector de posiciones
        self.camino_actual = camino_actual # numero de la posicion actual de result
        self.vectorGrafo = vectorGrafo # Vector de Nodos
        self.recarga = recarga # Entero
        self.ir_a_recargar = ir_a_recargar # Vector de bool
    # Defined in subclasses, with the appropriate type.
    def testValue(self):# -> any
        return
    
    # Perform the test.
    def getBranch(self):# -> DecisionTreeNode
        # Si ya llegue al nodo objetivo, cambio la posicion del personaje de manera aleatoria
        #print(self.personaje.position[0],self.personaje.position[1],"  ",self.objetivo.position[0] + self.radio_de_aceptacion,self.objetivo.position[0] - self.radio_de_aceptacion,self.objetivo.position[1] - self.radio_de_aceptacion,self.objetivo.position[1] + self.radio_de_aceptacion)
        if (self.personaje.position[0] <= self.objetivo.position[0] + self.radio_de_aceptacion and self.personaje.position[0] >= self.objetivo.position[0] - self.radio_de_aceptacion) and (self.personaje.position[1] >= self.objetivo.position[1] - self.radio_de_aceptacion and self.personaje.position[1] <= self.objetivo.position[1] + self.radio_de_aceptacion):
            action1 = ActionLimpiador(self.personaje,self.objetivo,self.nodo_inicial,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.camino_actual,self.vectorGrafo,self.recarga,self.ir_a_recargar,0) 
            return action1.makeDecision()
        else:
            # Si aun no llegue al nodo objetivo y aun tengo energia, hago el pathfinding a el nodo objetivo
            if self.energia[0] > 0:
                action2 = ActionLimpiador(self.personaje,self.objetivo,self.nodo_inicial,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.camino_actual,self.vectorGrafo,self.recarga,self.ir_a_recargar,1) 
                return action2.makeDecision()
            else:
                if self.ir_a_recargar[0]:
                    action2 = ActionLimpiador(self.personaje,self.objetivo,self.nodo_inicial,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.camino_actual,self.vectorGrafo,self.recarga,self.ir_a_recargar,1) 
                    return action2.makeDecision()
                else:
                    action3 = ActionLimpiador(self.personaje,self.objetivo,self.nodo_inicial,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.camino_actual,self.vectorGrafo,self.recarga,self.ir_a_recargar,2) 
                    return action3.makeDecision() 

    # Recursively walk through the tree.
    def makeDecision(self):# -> DecisionTreeNode
        # Make the decision and recurse based on the result.
        branch = self.getBranch() # DecisionTreeNode o Accion
        if str(type(branch)) == "<class 'DecisionTree.ActionLimpiador'>":
            return branch
        else:
            return branch.makeDecision()
    
class DecisionTreeNodeLimpiador:
    def __init__(self,personaje,objetivo,nodo_inicial,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,camino_actual,vectorGrafo,recarga,ir_a_recargar):
        self.personaje = personaje
        self.objetivo = objetivo
        self.kin = kin
        self.nodo_inicial = nodo_inicial
        self.objetivoAUX = objetivoAUX
        self.energia = energia
        self.radio_de_aceptacion = radio_de_aceptacion
        self.tamaño_cuadricula = tamaño_cuadricula
        self.path_result = path_result
        self.camino_actual = camino_actual
        self.vectorGrafo = vectorGrafo
        self.recarga = recarga # Entero
        self.ir_a_recargar = ir_a_recargar # Vector de bool
        self.decision = Limpiador_decision(personaje,objetivo,nodo_inicial,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,camino_actual,vectorGrafo,recarga,ir_a_recargar)
        
    # Recursively walk through the tree.
    def makeDecision(self):
        return self.decision.makeDecision() # -> DecisionTreeNode
    

# -----------------------------------------------------------------------------------------------
# Ladron
class DecisionTreeNodeLadron:
    def __init__(self,personaje,objetivo,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,grafo,ir_a_guardar,arbolLimpiador,columnas,targetGuardarE,energiaGuardadaEnZ,moverse):
        self.personaje = personaje
        self.objetivo = objetivo
        self.kin = kin
        self.objetivoAUX = objetivoAUX
        self.energia = energia
        self.radio_de_aceptacion = radio_de_aceptacion
        self.tamaño_cuadricula = tamaño_cuadricula
        self.path_result = path_result
        self.grafo = grafo
        self.ir_a_guardar = ir_a_guardar # Vector de bool
        self.arbolLimpiador = arbolLimpiador
        self.columnas = columnas
        self.targetGuardarE = targetGuardarE
        self.energiaGuardadaEnZ = energiaGuardadaEnZ
        self.moverse = moverse
        self.decision = Ladron_decision(self.personaje,self.objetivo,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.ir_a_guardar,self.arbolLimpiador,self.columnas,self.targetGuardarE,self.energiaGuardadaEnZ,self.moverse)
        
    # Recursively walk through the tree.
    def makeDecision(self):
        return self.decision.makeDecision() # -> DecisionTreeNode

class Ladron_decision:
    def __init__(self,personaje,objetivo,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,grafo,ir_a_guardar,arbolLimpiador,columnas,targetGuardarE,energiaGuardadaEnZ,moverse):
        self.personaje = personaje # Personaje
        self.objetivo = objetivo # Objetivo
        self.kin = kin # SteringOutput  
        self.objetivoAUX = objetivoAUX # Objetivo
        self.energia = energia # Entero 
        self.radio_de_aceptacion = radio_de_aceptacion # float
        self.tamaño_cuadricula = tamaño_cuadricula # entero
        self.path_result = path_result # Vector de posiciones
        #self.vectorGrafo = vectorGrafo # Vector de Nodos
        self.grafo = grafo
        self.ir_a_guardar = ir_a_guardar # Vector de bool
        self.arbolLimpiador = arbolLimpiador
        self.columnas = columnas
        self.targetGuardarE = targetGuardarE
        self.energiaGuardadaEnZ = energiaGuardadaEnZ
        self.moverse = moverse
    
    # Perform the test.
    def getBranch(self):# -> DecisionTreeNode
        # Las acciones se aplican si me puedo mover, si no, debo espero unos 5sg (accion ejecutada para esperar que el limpiador recargue energia)
        # Si ya alcancé al nodo del limpiador, veo si tiene energía
        if (self.personaje.position[0] <= self.objetivo.position[0] + self.radio_de_aceptacion and self.personaje.position[0] >= self.objetivo.position[0] - self.radio_de_aceptacion) and (self.personaje.position[1] >= self.objetivo.position[1] - self.radio_de_aceptacion and self.personaje.position[1] <= self.objetivo.position[1] + self.radio_de_aceptacion):
            # Si el limpiador no tiene energia
            if (self.arbolLimpiador.energia[0] == 0): 
                # Si tengo que ir a guardar, hago el pathfinding a la zona de guardado y descargo la energia cuando llegue
                if self.ir_a_guardar[0]:
                    action5 = ActionLadron(self.personaje,self.objetivo,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.ir_a_guardar,self.arbolLimpiador,self.columnas,self.targetGuardarE,self.energiaGuardadaEnZ,self.moverse,4) 
                    return action5.makeDecision()
                # Si no tengo que ir a guardar, espero unos 5sg a ver si cuando lo vuelva a alcanzar tiene energia
                else:
                    action1 = ActionLadron(self.personaje,self.objetivo,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.ir_a_guardar,self.arbolLimpiador,self.columnas,self.targetGuardarE,self.energiaGuardadaEnZ,self.moverse,0)
                    return action1.makeDecision()
            # Si el limpiador tiene energia, le robo la energia y hago pathfinding a la zona de guardado de energia
            else:
                action2 = ActionLadron(self.personaje,self.objetivo,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.ir_a_guardar,self.arbolLimpiador,self.columnas,self.targetGuardarE,self.energiaGuardadaEnZ,self.moverse,1) 
                return action2.makeDecision() 
        # Si no estoy en la posicion del limpiador
        else:
            # Si tengo que ir a guardar hago pathfinding a la zona de guardado y descargo la energia cuando llegue
            if self.ir_a_guardar[0]:
                action3 = ActionLadron(self.personaje,self.objetivo,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.ir_a_guardar,self.arbolLimpiador,self.columnas,self.targetGuardarE,self.energiaGuardadaEnZ,self.moverse,2) 
                return action3.makeDecision()
            # Si no tengo que ir a guardar, hago pathfinding al limpiador
            else:
                action4 = ActionLadron(self.personaje,self.objetivo,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.ir_a_guardar,self.arbolLimpiador,self.columnas,self.targetGuardarE,self.energiaGuardadaEnZ,self.moverse,3) 
                return action4.makeDecision()

    # Recursively walk through the tree.
    def makeDecision(self):# -> DecisionTreeNode
        # Make the decision and recurse based on the result.
        branch = self.getBranch() # DecisionTreeNode o Accion
        if str(type(branch)) == "<class 'DecisionTree.ActionLadron'>":
            return branch
        else:
            return branch.makeDecision()
        
class ActionLadron:
    def __init__(self,personaje,objetivo,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,grafo,ir_a_guardar,arbolLimpiador,columnas,targetGuardarE,energiaGuardadaEnZ,moverse,opcion):
        self.personaje = personaje
        self.objetivo = objetivo
        self.kin = kin
        self.objetivoAUX = objetivoAUX
        self.energia = energia
        self.radio_de_aceptacion = radio_de_aceptacion
        self.tamaño_cuadricula = tamaño_cuadricula
        self.path_result = path_result
        #self.vectorGrafo = vectorGrafo
        self.grafo = grafo
        self.ir_a_guardar = ir_a_guardar
        self.arbolLimpiador = arbolLimpiador
        self.columnas = columnas
        self.targetGuardarE = targetGuardarE
        self.opcion = opcion
        self.energiaGuardadaEnZ = energiaGuardadaEnZ
        self.moverse = moverse

        # Si ya llegue al nodo del limpiador, no tiene energia y no tengo que ir a guardar me quedo quieto unos 5sg a ver si luego el limpiador tiene energia
        if opcion == 0:
            self.moverse[0] = 150 # Contador que voy a ir disminuyendo hasta que me pueda mover (cuando llegue a 0)    

        # Si ya llegue al nodo limpiador y tiene energia, se la robo y hago pathfinding a la zona de guardado de energia. Solo si me puedo mover
        elif opcion == 1:
            if self.moverse[0] == 0:
                self.energia[0] += self.arbolLimpiador.energia[0] # Sumo en caso de que durante el recorrido a la zona de guardado se encuentra al limpiador
                self.arbolLimpiador.energia[0] = 0 
                self.ir_a_guardar[0] = True
                # Primero veo en que nodo esta la zona de guardado, el cual sera mi objetivo
                nodo_zona_guardar = nodo_actual(self.targetGuardarE.position[0],self.targetGuardarE.position[1],self.columnas,self.tamaño_cuadricula)
                heuristicaLadron = Heuristic(self.grafo.vectorGrafo[nodo_zona_guardar])
                # Veo en que nodo está el ladron, el cual sera el nodo de partida
                nodo_ladron = nodo_actual(self.personaje.position[0],self.personaje.position[1],self.columnas,self.tamaño_cuadricula)
                # Pathfinding del ladron a la zona de guardado. Modifico por referencia el arreglo
                temp_path_result = pathfindAStar(self.grafo,self.grafo.vectorGrafo[nodo_ladron],self.grafo.vectorGrafo[nodo_zona_guardar],heuristicaLadron)
                for i in range(len(self.path_result)): # Hago esto para modificar por referencia el arreglo 
                    self.path_result.pop()
                for i in range(len(temp_path_result)):
                    self.path_result.append(temp_path_result[i])

                # Realizo el seek del ladron a la zona de guardado. Solo actualizo objetivoAUX si el path tiene longitud mayor a 0
                if len(self.path_result) > 0:
                    self.objetivoAUX.position[0] = (self.path_result[0].toNode.vectorPosicion[1] * self.tamaño_cuadricula) + self.tamaño_cuadricula/2
                    self.objetivoAUX.position[1] = (self.path_result[0].toNode.vectorPosicion[0] * self.tamaño_cuadricula) + self.tamaño_cuadricula/2
                self.kin = Seek(self.personaje,self.objetivoAUX,0.03) # Busqueda del personaje al target (Seek)
                seekladron = self.kin.getSteering() # Me da un SteeringOutput. Realiza la busqueda (Seek) del personaje al target
                self.personaje.update(seekladron,0.5,2) # Se actualiza la posicion del personaje
            else:
                self.moverse[0] -= 1

        # Si no estoy en la posicion del limpiador y tengo que ir a guardar hago hago pathfinding a la zona de guardado y descargo la energia cuando llegue a la zona de guardado
        # o Si estoy en la posicion del limpiador, no tiene energia y tengo que ir a guardar, hago el pathfinding a la zona de guardado y descargo la energia cuando llegue
        # (Solo si puedo moverme)
        elif opcion == 2 or opcion == 4: 
            if self.moverse[0] == 0:       
                # Primero veo en que nodo esta la zona de guardado, el cual sera mi objetivo
                nodo_zona_guardar = nodo_actual(self.targetGuardarE.position[0],self.targetGuardarE.position[1],self.columnas,self.tamaño_cuadricula)
                # Veo en que nodo está el ladron, el cual sera el nodo de partida
                nodo_ladron = nodo_actual(self.personaje.position[0],self.personaje.position[1],self.columnas,self.tamaño_cuadricula)
                # En caso de que ya esté en la zona:
                if nodo_ladron == nodo_zona_guardar:
                    self.energiaGuardadaEnZ[0] += self.energia[0]
                    self.energia[0] = 0
                    self.ir_a_guardar[0] = False
                # En caso de que aun no este en la zona
                else:
                    # Pathfinding del ladron a la zona de guardado. Modifico por referencia el arreglo
                    heuristicaLadron = Heuristic(self.grafo.vectorGrafo[nodo_zona_guardar])
                    temp_path_result = pathfindAStar(self.grafo,self.grafo.vectorGrafo[nodo_ladron],self.grafo.vectorGrafo[nodo_zona_guardar],heuristicaLadron)
                    for i in range(len(self.path_result)): # Hago esto para modificar por referencia el arreglo 
                        self.path_result.pop()
                    for i in range(len(temp_path_result)):
                        self.path_result.append(temp_path_result[i])

                    # Realizo el seek del ladron a la zona de guardado. Solo actualizo objetivoAUX si el path tiene longitud mayor a 0
                    if len(self.path_result) > 0:
                        self.objetivoAUX.position[0] = (self.path_result[0].toNode.vectorPosicion[1] * self.tamaño_cuadricula) + self.tamaño_cuadricula/2
                        self.objetivoAUX.position[1] = (self.path_result[0].toNode.vectorPosicion[0] * self.tamaño_cuadricula) + self.tamaño_cuadricula/2
                    self.kin = Seek(self.personaje,self.objetivoAUX,0.03) # Busqueda del personaje al target (Seek)
                    seekladron = self.kin.getSteering() # Me da un SteeringOutput. Realiza la busqueda (Seek) del personaje al target
                    self.personaje.update(seekladron,0.5,2) # Se actualiza la posicion del personaje
            else:
                self.moverse[0] -= 1    
       
        # Si no estoy en la posicion del limpiador y no tengo que ir a guardar, hago pathfinding al limpiador
        # (Solo si puedo moverme)
        else: # Opcion 3
            if self.moverse[0] == 0:
                # Configuro y calculo el pathfinding del ladron al limpiador. Se hace en cada iteracion ya que el limpiador cambia de posicion
                # Primero veo en que nodo esta el limpiador, el cual sera mi objetivo
                nodo_limpiador = nodo_actual(self.objetivo.position[0],self.objetivo.position[1],self.columnas,self.tamaño_cuadricula)
                heuristicaLadron = Heuristic(self.grafo.vectorGrafo[nodo_limpiador])
                # Veo en que nodo está el ladron, el cual sera el nodo de partida
                nodo_ladron = nodo_actual(self.personaje.position[0],self.personaje.position[1],self.columnas,self.tamaño_cuadricula)
                # Pathfinding del ladron al limpiador. Modifico por referencia el arreglo
                temp_path_result = pathfindAStar(self.grafo,self.grafo.vectorGrafo[nodo_ladron],self.grafo.vectorGrafo[nodo_limpiador],heuristicaLadron)
                for i in range(len(self.path_result)): # Hago esto para modificar por referencia el arreglo 
                    self.path_result.pop()
                for i in range(len(temp_path_result)):
                    self.path_result.append(temp_path_result[i])

                # Realizo el seek del ladron al limpiador. Solo actualizo objetivoAUX si el path tiene longitud mayor a 0
                if len(self.path_result) > 0:
                    self.objetivoAUX.position[0] = (self.path_result[0].toNode.vectorPosicion[1] * self.tamaño_cuadricula) + self.tamaño_cuadricula/2
                    self.objetivoAUX.position[1] = (self.path_result[0].toNode.vectorPosicion[0] * self.tamaño_cuadricula) + self.tamaño_cuadricula/2
                self.kin = Seek(self.personaje,self.objetivoAUX,0.03) # Busqueda del personaje al target (Seek)
                seekladron = self.kin.getSteering() # Me da un SteeringOutput. Realiza la busqueda (Seek) del personaje al target
                self.personaje.update(seekladron,0.5,2) # Se actualiza la posicion del personaje
            else:
                self.moverse[0] -= 1

    def makeDecision(self): # -> DecisionTreeNode:
        return self
    

# -----------------------------------------------------------------------------------------------
 
# Bailador
class DecisionTreeNodeBailador:
    def __init__(self,personaje,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,grafo,columnas,targetGuardarE,targetZonaBaile,camino_actual,energiaGuardadaEnZ,esperando):
        self.personaje = personaje
        self.kin = kin
        self.objetivoAUX = objetivoAUX
        self.energia = energia
        self.radio_de_aceptacion = radio_de_aceptacion
        self.tamaño_cuadricula = tamaño_cuadricula
        self.path_result = path_result
        self.grafo = grafo
        self.columnas = columnas
        self.targetGuardarE = targetGuardarE
        self.targetZonaBaile = targetZonaBaile
        self.camino_actual = camino_actual
        self.energiaGuardadaEnZ = energiaGuardadaEnZ
        self.esperando = esperando
        self.decision = Bailador_decision(self.personaje,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.columnas,self.targetGuardarE,self.targetZonaBaile,self.camino_actual,self.energiaGuardadaEnZ,self.esperando)
        
    # Recursively walk through the tree.
    def makeDecision(self):
        return self.decision.makeDecision() # -> DecisionTreeNode

class Bailador_decision:
    def __init__(self,personaje,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,grafo,columnas,targetGuardarE,targetZonaBaile,camino_actual,energiaGuardadaEnZ,esperando):
        self.personaje = personaje
        self.kin = kin
        self.objetivoAUX = objetivoAUX
        self.energia = energia
        self.radio_de_aceptacion = radio_de_aceptacion
        self.tamaño_cuadricula = tamaño_cuadricula
        self.path_result = path_result
        self.grafo = grafo
        self.columnas = columnas
        self.targetGuardarE = targetGuardarE
        self.targetZonaBaile = targetZonaBaile
        self.camino_actual = camino_actual
        self.energiaGuardadaEnZ = energiaGuardadaEnZ
        self.esperando = esperando

    # Perform the test.
    def getBranch(self):# -> DecisionTreeNode
        
        # Si estoy en la zona de baile
        if (self.personaje.position[0] <= self.targetZonaBaile.position[0] + self.radio_de_aceptacion and self.personaje.position[0] >= self.targetZonaBaile.position[0] - self.radio_de_aceptacion) and (self.personaje.position[1] >= self.targetZonaBaile.position[1] - self.radio_de_aceptacion and self.personaje.position[1] <= self.targetZonaBaile.position[1] + self.radio_de_aceptacion):
            # Si tengo energía bailo y voy disminuyendo energia en 2
            if (self.energia[0] > 0):        
                action1 = ActionBailador(self.personaje,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.columnas,self.targetGuardarE,self.targetZonaBaile,self.camino_actual,self.energiaGuardadaEnZ,self.esperando,1) 
                return action1.makeDecision()
            
            # Si no tengo energia, hago pathfinding a la zona de guardado de energia para recargar
            else:
                action2 = ActionBailador(self.personaje,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.columnas,self.targetGuardarE,self.targetZonaBaile,self.camino_actual,self.energiaGuardadaEnZ,self.esperando,2) 
                return action2.makeDecision() 
        
        # Si no estoy en la zona de baile
        else:
            # Si estoy en la zona de guardado de energia 
            if (self.personaje.position[0] <= self.targetGuardarE.position[0] + self.radio_de_aceptacion and self.personaje.position[0] >= self.targetGuardarE.position[0] - self.radio_de_aceptacion) and (self.personaje.position[1] >= self.targetGuardarE.position[1] - self.radio_de_aceptacion and self.personaje.position[1] <= self.targetGuardarE.position[1] + self.radio_de_aceptacion):
                # Si hay energia en la zona de guardado, recargo y hago pathfinding a la zona de baile
                if (self.energiaGuardadaEnZ[0] > 0):                
                    action3 = ActionBailador(self.personaje,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.columnas,self.targetGuardarE,self.targetZonaBaile,self.camino_actual,self.energiaGuardadaEnZ,self.esperando,3) 
                    return action3.makeDecision()
                # Si no hay energia en la zona de guardado, espero hasta que haya energia
                else:
                    action4 = ActionBailador(self.personaje,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.columnas,self.targetGuardarE,self.targetZonaBaile,self.camino_actual,self.energiaGuardadaEnZ,self.esperando,4) 
                    return action4.makeDecision()
            # Si no estoy en la zona de guardado de energia
            else:
                # Si tengo energia, hago pathfinding a la zona de baile
                if (self.energia[0] > 0):
                    action5 = ActionBailador(self.personaje,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.columnas,self.targetGuardarE,self.targetZonaBaile,self.camino_actual,self.energiaGuardadaEnZ,self.esperando,5) 
                    return action5.makeDecision()
                # Si no tengo energia, hago pathfinding a la zona de guardado de energia
                else:
                    action6 = ActionBailador(self.personaje,self.kin,self.objetivoAUX,self.energia,self.radio_de_aceptacion,self.tamaño_cuadricula,self.path_result,self.grafo,self.columnas,self.targetGuardarE,self.targetZonaBaile,self.camino_actual,self.energiaGuardadaEnZ,self.esperando,6) 
                    return action6.makeDecision()

    # Recursively walk through the tree.
    def makeDecision(self):# -> DecisionTreeNode
        # Make the decision and recurse based on the result.
        branch = self.getBranch() # DecisionTreeNode o Accion
        if str(type(branch)) == "<class 'DecisionTree.ActionBailador'>":
            return branch
        else:
            return branch.makeDecision()
        
class ActionBailador:
    def __init__(self,personaje,kin,objetivoAUX,energia,radio_de_aceptacion,tamaño_cuadricula,path_result,grafo,columnas,targetGuardarE,targetZonaBaile,camino_actual,energiaGuardadaEnZ,esperando,opcion):
        self.personaje = personaje
        self.kin = kin
        self.objetivoAUX = objetivoAUX
        self.energia = energia
        self.radio_de_aceptacion = radio_de_aceptacion
        self.tamaño_cuadricula = tamaño_cuadricula
        self.path_result = path_result
        self.grafo = grafo
        self.columnas = columnas
        self.targetGuardarE = targetGuardarE
        self.targetZonaBaile = targetZonaBaile
        self.camino_actual = camino_actual
        self.energiaGuardadaEnZ = energiaGuardadaEnZ
        self.esperando = esperando
        self.opcion = opcion

        # Si estoy en la zona de baile y tengo energía, bailo y voy disminuyendo energia en 2
        if opcion == 1:
            self.energia[0] -= 0.1
            kin.character.orientation += 2 # Para hacer ver que esta dando vueltas como si bailara        
                             
        # Si estoy en la zona de baile y no tengo energia, hago pathfinding a la zona de guardado de energia para recargar
        elif opcion == 2:
            self.esperando[0] = 0
            self.camino_actual[0] = 0
            # Primero veo en que nodo esta la zona de guardado, el cual sera mi objetivo
            nodo_zona_guardar = nodo_actual(self.targetGuardarE.position[0],self.targetGuardarE.position[1],self.columnas,self.tamaño_cuadricula)
            heuristicaBailador = Heuristic(self.grafo.vectorGrafo[nodo_zona_guardar])
            # Veo en que nodo está el bailador, el cual sera el nodo de partida
            nodo_bailador = nodo_actual(self.personaje.position[0],self.personaje.position[1],self.columnas,self.tamaño_cuadricula)
            # Pathfinding del bailador a la zona de guardado. Modifico por referencia el arreglo
            temp_path_result = pathfindAStar(self.grafo,self.grafo.vectorGrafo[nodo_bailador],self.grafo.vectorGrafo[nodo_zona_guardar],heuristicaBailador)
            for i in range(len(self.path_result)): # Hago esto para modificar por referencia el arreglo 
                self.path_result.pop()
            for i in range(len(temp_path_result)):
                self.path_result.append(temp_path_result[i])

            # Realizo el seek del bailador a la zona de guardado. Solo actualizo objetivoAUX si el path tiene longitud mayor a 0
            if len(self.path_result) > 0:
                self.objetivoAUX.position[0] = (self.path_result[0].toNode.vectorPosicion[1] * self.tamaño_cuadricula) + self.tamaño_cuadricula/2
                self.objetivoAUX.position[1] = (self.path_result[0].toNode.vectorPosicion[0] * self.tamaño_cuadricula) + self.tamaño_cuadricula/2
            self.kin = Seek(self.personaje,self.objetivoAUX,0.03) # Busqueda del personaje al target (Seek)
            seekbailador = self.kin.getSteering() # Me da un SteeringOutput. Realiza la busqueda (Seek) del personaje al target
            self.personaje.update(seekbailador,0.45,2) # Se actualiza la posicion del personaje

        # Si no estoy en la zona de baile, estoy en la zona de guardado de energia y 
        # hay energia en la zona de guardado, recargo y hago pathfinding a la zona
        # de baile
        elif opcion == 3:     
            self.esperando[0] = 0 # Dejo de esperar 
            # Recargo   
            self.energia[0] = self.energiaGuardadaEnZ[0]
            self.energiaGuardadaEnZ[0] = 0

            # Pathfinding a la zona de guardado
            self.camino_actual[0] = 0
            # Primero veo en que nodo esta la zona de guardado, el cual sera mi objetivo
            nodo_zona_baile = nodo_actual(self.targetZonaBaile.position[0],self.targetZonaBaile.position[1],self.columnas,self.tamaño_cuadricula)
            # Veo en que nodo está el bailador, el cual sera el nodo de partida
            nodo_bailador = nodo_actual(self.personaje.position[0],self.personaje.position[1],self.columnas,self.tamaño_cuadricula)

            # Pathfinding del bailador a la zona de baile. Modifico por referencia el arreglo
            heuristicaBailador = Heuristic(self.grafo.vectorGrafo[nodo_zona_baile])
            temp_path_result = pathfindAStar(self.grafo,self.grafo.vectorGrafo[nodo_bailador],self.grafo.vectorGrafo[nodo_zona_baile],heuristicaBailador)
            for i in range(len(self.path_result)): # Hago esto para modificar por referencia el arreglo 
                self.path_result.pop()
            for i in range(len(temp_path_result)):
                self.path_result.append(temp_path_result[i])

            # Realizo el seek del bailador a la zona de baile. Solo actualizo objetivoAUX si el path tiene longitud mayor a 0
            if len(self.path_result) > 0:
                self.objetivoAUX.position[0] = (self.path_result[0].toNode.vectorPosicion[1] * self.tamaño_cuadricula) + self.tamaño_cuadricula/2
                self.objetivoAUX.position[1] = (self.path_result[0].toNode.vectorPosicion[0] * self.tamaño_cuadricula) + self.tamaño_cuadricula/2
            self.kin = Seek(self.personaje,self.objetivoAUX,0.03) # Busqueda del personaje al target (Seek)
            seekbailador = self.kin.getSteering() # Me da un SteeringOutput. Realiza la busqueda (Seek) del personaje al target
            self.personaje.update(seekbailador,0.45,2) # Se actualiza la posicion del personaje
      
        # Si no estoy en la zona de baile, estoy en la zona de guardado de energia y 
        # no hay energia en la zona de guardado, espero hasta que haya energia
        elif opcion == 4: 
            
            if self.energia[0] <= 0:
                self.esperando[0] = 1
            # En caso de que tenga energia (haya recargado), pero aun estoy en la zona de guardado
            # de energia, tengo que dejar de esperar y avanzar
            else:
                self.esperando[0] = 0
                # Para avanzar paso por paso, sin tener que recalcular el camino
                if (self.personaje.position[0] <= self.objetivoAUX.position[0] + self.radio_de_aceptacion and self.personaje.position[0] >= self.objetivoAUX.position[0] - self.radio_de_aceptacion) and (self.personaje.position[1] >= self.objetivoAUX.position[1] - self.radio_de_aceptacion and self.personaje.position[1] <= self.objetivoAUX.position[1] + self.radio_de_aceptacion):
                    self.objetivoAUX.position[0] = (self.tamaño_cuadricula * self.path_result[self.camino_actual[0]].toNode.vectorPosicion[1]) + self.tamaño_cuadricula/2
                    self.objetivoAUX.position[1] = (self.tamaño_cuadricula * self.path_result[self.camino_actual[0]].toNode.vectorPosicion[0]) + self.tamaño_cuadricula/2
                    self.kin.target = objetivoAUX
                    self.camino_actual[0] += 1 # Avanzo una posicion

                seekbailador = self.kin.getSteering() # Me da un SteeringOutput. Realiza la busqueda (Seek) del personaje al target
                self.personaje.update(seekbailador,0.45,2)
        
        # Si no estoy en la zona de baile, no estoy en la zona de guardado de energia 
        # y tengo energia, hago pathfinding a la zona de baile. 
        # Igualmente: 
        # Si no estoy en la zona de baile, no estoy en la zona de guardado de energia
        # y no tengo energia, hago pathfinding a la zona de guardado de energia
        elif opcion == 5 or opcion == 6:
            # Para avanzar paso por paso, sin tener que recalcular el camino
            if (self.personaje.position[0] <= self.objetivoAUX.position[0] + self.radio_de_aceptacion and self.personaje.position[0] >= self.objetivoAUX.position[0] - self.radio_de_aceptacion) and (self.personaje.position[1] >= self.objetivoAUX.position[1] - self.radio_de_aceptacion and self.personaje.position[1] <= self.objetivoAUX.position[1] + self.radio_de_aceptacion):
                self.objetivoAUX.position[0] = (self.tamaño_cuadricula * self.path_result[self.camino_actual[0]].toNode.vectorPosicion[1]) + self.tamaño_cuadricula/2
                self.objetivoAUX.position[1] = (self.tamaño_cuadricula * self.path_result[self.camino_actual[0]].toNode.vectorPosicion[0]) + self.tamaño_cuadricula/2
                self.kin.target = objetivoAUX
                self.camino_actual[0] += 1 # Avanzo una posicion

            seekbailador = self.kin.getSteering() # Me da un SteeringOutput. Realiza la busqueda (Seek) del personaje al target
            self.personaje.update(seekbailador,0.45,2)

    def makeDecision(self): # -> DecisionTreeNode:
        return self
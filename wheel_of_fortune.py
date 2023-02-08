import json
import random
import time
import ast


letras= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
vocales= "AEIOU"
valor_vocal= 250


#(1) Clase jugador
class jugador:

    #Constructor de la clase jugador
    def __init__(self , nombre):
        self.nombre = nombre
        self.dinero_premio = 0
        self.premios = []


    #metodo de jugador
    def dinero_obtenido(self, extra):
        self.dinero_premio += extra


    #metodo de jugador
    def bancarrota(self):
        self.dinero_premio = 0


    #metodo de jugador
    def adicionar_premios(self, premio):
        (self.premios).append(premio)


    #lo que deseamos obtener al realizar un print de un objeto de nuestra clase (instancia)
    def __str__(self):
        return f"{self.nombre} (${self.dinero_premio})"





#(2) subclase de jugador
class jugador_humano(jugador):

    #Constructor de la clase jugador_humano
    def __init(self, nombre):
        jugador.__ini__(self, nombre)


    #metodo = en este metodo se realiza el adivina una letra de la frase oculta
    def realizar_movimiento(self, categoria, frase_oculta, adivinado):
        print("***********************************************************************")
        print("")
        print(f"{self.nombre} tiene (${self.dinero_premio})")
        print("")
        print("Categoria:",categoria)
        print("")
        print("Frase:", frase_oculta)
        print("")
        print("Letras descubiertas:", adivinado)
        print("")
        print("************************")
        print("")
        time.sleep(5)
        movimiento = str(input("Escoger una de las siguientes acciones:\n\n(1) Adivinar una letra ó una frase \n\n(2) Escribir  'salida' ó 'paso': \n\n"))
        return movimiento




#(3) subclase de jugador
class jugador_maquina(jugador):

    #Estas son las letras del inglés ordenadas de menor ocurrencia a mayor ocurrencia
    frecuencia_letras = "ZQXJKVBPYGFWMUCLDRHSNIOATE"


    # constructor de la subclase jugador_robot
    def __init__(self, nombre, dificultad):
        jugador.__init__(self,nombre)
        self.dificultad = dificultad
        self.premios = []
        self.dinero_premio = 0


    #metodo del jugador_robot= lanzamiento_inteligente_monedas
    def lanzamiento_inteligente_monedas(self):
        numero_aleatorio = random.randint(1, 10)
        if numero_aleatorio > self.dificultad:
            return True
        else:
            return False


    #metodo del jugador_robot = lista_letras_utiles. Este metodo nos brinda una lista de letras utiles para jugar. Este es el metodo que usaria una persona inteligente para realizar una escogencia apropiada de letras
    def lista_letras_utiles(self, adivinado):
        lista_adivinar = []
        for x in letras:
            if x in adivinado:
                continue
            elif (x not in adivinado) and (x not in vocales):
                lista_adivinar.append(x)
            elif (x not in adivinado) and (x in vocales):
                if self.dinero_premio >= valor_vocal:
                    lista_adivinar.append(x)
                elif self.dinero_premio < valor_vocal:
                    continue
        return lista_adivinar


    #metodo del jugador_robot = en este metodo adivinamos una letra de manera inteligente (computadora). la estupida moneda hace que la escogencia no sea la mas audaz
    def realizar_movimiento(self, categoria, frase_oculta, adivinado):
        lista_adivinar = self.lista_letras_utiles(adivinado)
        if lista_adivinar == []:
            return "paso"
        else:
            valor = self.lanzamiento_inteligente_monedas()
            if valor == True:
                n = len(self.frecuencia_letras)
                while 1 <= n <= len(self.frecuencia_letras):
                    m = self.frecuencia_letras[n-1]
                    if m in lista_adivinar:
                        return self.frecuencia_letras[n-1]
                    else:
                        n=n-1
                        continue
            elif valor == False:
                letra_arbitraria = random.choice(lista_adivinar)
                return letra_arbitraria




#--------------------------------------------------------------------------------------------------------------------------------------------------------
# funcion = esta funcion devuelve un numero entre minimo y maximo
def obtener_un_numero_en_intervalo(entrada, minimo, maximo):
    entrada_usuario = input(entrada)
    while True:
        try:
            n = int(entrada_usuario)
            if n < minimo:
                mensaje_de_error = f"Debes tomar un numero que sea mayor o igual a {minimo}"
            elif n > maximo:
                mensaje_de_error = f"Debes tomar un numero que sea menor o igual a {maximo}"
            else:
                return n
        except ValueError:
            mensaje_de_error = f"{entrada_usuario} no es un numero."

        entrada_usuario = input(f"{mensaje_de_error}. Vuelve a intentarlo.\n{entrada}")




# funcion = esta funcion nos brinda un premio aleatorio en forma de diccionario como se muestra a continuacion
# Ejemplos:
#    { "type": "cash", "text": "$950", "value": 950, "prize": "A trip to Ann Arbor!" },
#    { "type": "bankrupt", "text": "Bankrupt", "prize": false },
#    { "type": "loseturn", "text": "Lose a turn", "prize": false }
def rueda_giratoria():
    with open("wheel.txt", "r") as f:
        rueda = ast.literal_eval(f.read())
        return random.choice(rueda)




# Funcion: esta funcion devuelve una categoria y una frase aleatoria como una tupla para adivinar
# Ejemplo:
# ("Artist & Song", "Whitney Houston's I Will Always Love You")
def categoria_y_frase_aleatoria():
    with open("phrases.txt", "r") as f:
        frases = ast.literal_eval(f.read())
        categoria = random.choice(list(frases.keys()))
        frase   = random.choice(frases[categoria])
        return (categoria, frase.upper())




# funcion = recibe como entrada una frase y una lista de letras(adivinadas) y devuelve una version oculta de la frase
# Example:
#     adivinado: ['L', 'B', 'E', 'R', 'N', 'P', 'K', 'X', 'Z']
#     frase:     "GLACIER NATIONAL PARK"
#     return:    "_L___ER N____N_L P_RK"
def frase_oculta(frase, adivinado):
    oculta = ""
    for x in frase:
        if (x in letras) and (x in adivinado):
            oculta = oculta+x
        elif (x in letras) and (x not in adivinado):
            oculta = oculta+"_"
    return oculta




# funcion = esta funcion devuelve una cadena de texto que representa el estado actual del juego
def mostrar_tablero(categoria, frase_oculta, adivinado):
    return f"""
            Categoria: {categoria} \n
            Frase:   {frase_oculta} \n
            Letras descubiertas:  {", ".join(sorted(adivinado))}"""






# Presentacion del juego (portada)
print("="*70)
print(" Rueda de la fortuana de Python - Frases en inglés \n\n Presentado por el matemático Julián Uribe Castañeda  \n\n Programación en Python | English - School.")
print("="*70)
print("")
print("")

#-------------------------------------------------------------------------------------------------------------------------------



#variable = esta variable nos dice el numero de jugadores humanos que tendremos en el juego
numero_humanos = obtener_un_numero_en_intervalo(" ¿Cuántos jugadores (humanos) tendremos en el juego?:   ", 0, 10)
print("")


#variable =  Esta variable es una lista que nos muestra el nombre de los jugadores humanos
jugadores_humanos = [jugador_humano(input(f"  Describir el nombre del jugador humano #{x+1}:      ")) for x in range(numero_humanos)]
print("")


#variable = esta variable nos dice el numero de jugadores maquina que tendremos en el juego
numero_maquinas = obtener_un_numero_en_intervalo(" ¿Cuántos jugadores robots tendremos en el juego?:   ", 0, 10)
print("")


# variable = dificultad es una variable que nos dice cual será el nivel de dificultad de los jugadores maquina
if numero_maquinas >= 1:
    dificultad = obtener_un_numero_en_intervalo(" ¿Cuál será la dificultad de los robots? (mínimo=1----máximo=10):   ", 1, 10)



#variable = esta variable es una lista que contiene los nombres de los computadores maquina
jugadores_maquinas = [jugador_maquina(f"Robot #{x+1}", dificultad) for x in range(numero_maquinas)]



#variable = esta variable nos cuenta el numero completo de jugadores (humanos y maquinas).
total_jugadores = jugadores_humanos + jugadores_maquinas



#IMPORTANTE. Sin jugadores no hay juego.
#La palabra clave raise de Python se utiliza para generar excepciones o errores. La palabra clave raise genera un error y detiene el flujo de control del programa.
#ejemplo: raise Exception(“user text”) es la excepcion mas usada
if len(total_jugadores) == 0:
    print("Necesitamos que hallan jugadores para poder iniciar el juego!")
    raise Exception("No hay suficientes jugadores")



#ULTRA IMPORTANTE: AQUI SE DICE CUAL ES LA FRASE-------tupla = categoria y frase aleatoria
categoria, frase = categoria_y_frase_aleatoria()



# variable = la variable adivinado es una lista de letras que han sido adivinadas
adivinado = []



# variable = indice_de_jugador es una variable que realiza un seguimiento de los indices de los jugadores (0 to len(players)-1)
indice_de_jugador = 0



# variable = la variable ganador nos dira si algun jugador gana el juego (cuando ganador == True)
ganador = False



# funcion = esta funcion obtiene como resultado un buen movimiento del jugador. Debido a que el anterior puede tener errores. Los resultados posibles son "paso", "l"-letra y None
def peticion_movimiento_jugador(jugador, categoria, adivinado):
    while True:
        time.sleep(2)
        movimiento = jugador.realizar_movimiento(categoria, frase_oculta(frase, adivinado), adivinado)
        movimiento = movimiento.upper()

        #(a) Problema(1) en la peticion de datos
        if movimiento == "SALIDA" or movimiento == "PASO":
            return movimiento

        #(b) Problema(2) en la peticion de datos
        elif len(movimiento) == 1:
            if movimiento not in letras:
                print("Los movimientos deben ser letras. Intentalo de nuevo.")
                time.sleep(2)
                continue
            elif movimiento in adivinado:
                print(f"La letra {movimiento} ya ha sido adivinada. Intenta de nuevo.")
                time.sleep(2)
                continue
            elif (movimiento in vocales) and (jugador.dinero_premio < valor_vocal):
                print(f"Debes tener al menos ${valor_vocal} para adivinar una vocal. Intenta de nuevo.")
                time.sleep(2)
                continue
            else:
                return movimiento #solo aqui no tenemos problemas en la peticion de datos.

        #(c) frase adivinada
        else: # este caso es un poco dificil de interpretar, ya que el metodo realizar_movimiento obtiene 3 posibles resultados ("paso", "l"-letra o None). Cuando obtiene None es precisamente que hemos adivinado
            return movimiento





while True:

    #recordar que indice_de_jugador empieza en cero
    jugador = total_jugadores[indice_de_jugador]

    premio_rueda = rueda_giratoria()

    print("")
    print("***********************************************************************")
    print(mostrar_tablero(categoria, frase_oculta(frase, adivinado), adivinado))
    print("")

    #Inicio del juego
    #(a) El jugador correspondiente gira la rueda
    print(f"{jugador.nombre} gira la rueda de la fortuna de Python...\n ")
    time.sleep(4)

    #(b) Se mira cual es el premio de la rueda
    print(f"""Y el premio obtenido de la rueda de la fortuna de  Python es  {premio_rueda["text"]}! \n""")
    time.sleep(2)

    #(c) se mira el "type" (tipo) de premio de la rueda

    #(c.1) bancarrota
    if premio_rueda["type"] == "bankrupt":
        jugador.bancarrota()
        time.sleep(2)

    #(c.2) perder el turno
    elif premio_rueda['type'] == "loseturn":
        time.sleep(2)
        pass


    #(c.3)
    elif premio_rueda["type"] == "cash":
        movimiento = peticion_movimiento_jugador(jugador, categoria, adivinado)

        #(c.3.1)
        if  movimiento == "SALIDA":
            print("Hasta la próxima vez")
            break

        #(c.3.2)
        elif movimiento == "PASO":
            print(f"{jugador.nombre} pasa el turno")
            time.sleep(2)

        #(c.3.3)
        elif len(movimiento) == 1:
            print("")
            adivinado.append(movimiento)
            print(f'{jugador.nombre} ha adivinado la letra "{movimiento}" \n')
            time.sleep(2)

            if movimiento in vocales:
                jugador.dinero_premio = jugador.dinero_premio - valor_vocal

            conteo = frase.count(movimiento) # devuelve un número entero con la cantidad de veces que aparece "movimiento"

            #------------------------------inicio conteo-----------------------------------------------------------------------
            if conteo > 0:
                if conteo == 1:
                    print(f"Solo hay una letra {movimiento} \n")
                    time.sleep(2)
                else:
                    print(f"Hay {conteo} {movimiento}'s")
                    time.sleep(2)

                # Se le da a los jugadores el dinero  obtenido
                jugador.dinero_obtenido(conteo * premio_rueda["value"])

                # Se le da a los jugadores el premio obtenido
                if premio_rueda["prize"]:
                    jugador.adicionar_premios(premio_rueda["prize"])

                # si todas las letras son adivinadas, entonces es declarado un ganador
                if frase_oculta(frase, adivinado) == frase:
                    ganador = jugador
                    time.sleep(2)
                    break


                continue # este jugador obtiene un nuevo intento


            elif conteo == 0:
                print(f"No está la letra {movimiento} \n")
            #------------------------------fin conteo-----------------------------------------------------------------------

        # se ha adivinado la frase completa
        else:
            if movimiento == frase: # han adivinado la frase correctamente. Se dice quien es el ganador
                ganador = jugador

                # Se da el dinero
                jugador.dinero_obtenido(premio_rueda["value"])

                # Se dan los  premios
                if premio_rueda["prize"]:
                    jugador.adicionar_premios(premio_rueda["prize"])
                break

            else:
                print(f"{movimiento} no era la frase")

    # Se continua en el siguiente turno----cambio de turno
    if indice_de_jugador < len(total_jugadores)-1:
        indice_de_jugador = indice_de_jugador + 1
    elif indice_de_jugador == len(total_jugadores)-1:
        indice_de_jugador = 0



#-----------------------------------------------------------------------------------------------------------------------

if ganador:

    #se dice que jugador gano el juego y se declara cual era la frase
    print(f"{ganador.nombre} ganó el juego y la frase era {frase} \n")

    #se dice la cantidad de dinero que gano el jugador ganador
    print(f"{ganador.nombre} ganó ${ganador.dinero_premio} \n")

    #se dice cuales premios adicionales gano el jugador victorioso
    if len(ganador.premios) > 0:
        print(f"{ganador.nombre} también ganó las siguientes cosas: \n")
        for x in ganador.premios:
            print(f"    - {x}")
else:
    print(f"Nadie ganó. La frase era {frase}")

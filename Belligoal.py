import pandas as pd
import tkinter.filedialog as filedialog

def Best_FIT ():
    ## aca arranca best fit
    parti = []  # Lista para almacenar las fragmentaciones internas positivas
    names = []  # Lista para almacenar los nombres correspondientes a las particiones
    
    rest1 = mem[1].tam - entra_a_listo.tam
    rest2 = mem[2].tam - entra_a_listo.tam 
    rest3 = mem[3].tam - entra_a_listo.tam


    if rest1 > 0 :
        parti.append(rest1)
        names.append("part1")
        

    if rest2 > 0 :
        parti.append(rest2)
        names.append("part2")
        

    if rest3 > 0  :
        parti.append(rest3)
        names.append("part3")
    minimo = min(parti)  # Buscar la mínima fragmentación interna
    
    posm = parti.index(minimo)  # Obtener la posición de la mínima fragmentación interna en parti
    pos = names[posm]  # Obtener el nombre de la partición correspondiente

    if pos == "part1":
        posn = 1  # Índice de la partición p1 en la lista particiones_mem
    elif pos == "part2":
        posn = 2  # Índice de la partición p2 en la lista particiones_mem
    else:
        posn = 3  # Índice de la partición p3 en la lista particiones_mem

    
    if (mem[posn].bloq == 0): #no esta bloqueada la mejor particion
        
        resta = (mem[posn].tam - mem[posn].tam)+ minimo
        mem[posn].FI = resta
        mem[posn].bloq = 1 
        mem[posn].proc = entra_a_listo.id  #cargo el id del proceso cargado en esa parti, importante para el cuadro
        list_listo.append (entra_a_listo)
        print(f"El proceso de id: {mem[posn].proc}, entro en memoria, se encuentra en la particion {posn}")  #info innecesaria quizas
        list_nuevo.pop(0) 
    else: #buscar la primera libre que entre el proceso 
        cargado = "no"
        for i in range (1,4):
            if (mem[i].bloq == 0):#particion libre
                resta = mem[i].tam - entra_a_listo.tam
                if resta > 0 : # puede entrar el loko porque da una fragmentacion mayor a 0
                    
                    mem[i].FI = resta
                    mem[i].bloq = 1
                    mem[i].proc = entra_a_listo.id
                    print(f"El proceso de id: {mem[i].proc}, entro en memoria, se encuentra en la particion {i}")
                    list_listo.append (entra_a_listo)
                    list_nuevo.pop(0)
                    cargado = "si"
                    break #rompo el for 
        if cargado == "no" :
            if (len(list_listo_susp)<3):  #salio del for, no encontro ninguna particion disponible, lo mando a list y susp
                a_listo_susp = list_nuevo.pop(0)
                print (f"entra a susp:{a_listo_susp.id}")
                list_listo_susp.append (a_listo_susp)
            else:
                print (f"Proceso {a_listo_susp}, sigue en cola de nuevos")  #si en la lista de suspendidos hay mas de 2, va a seguir en nuevo

class Particiones (object):
    def __init__(self,tam,bloq,FI,proc) :
        self.tam = int(tam)  #tamaño parti 
        self.bloq = bloq # esta usada o no
        self.FI = int(FI) # frag interna
        self.proc = str (proc)
    

class Proceso (object):
    def __init__(self,id,ta,ti,tam) :
        self.id = str (id)
        self.ta = int (ta)
        self.ti = int (ti)
        self.tam = int (tam)

class Info_irrupcion (object):
    def __init__(self,id,ti):
        self.id = str (id)
        self.ti = int (ti)
        

bandera = 0
file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
if file_path:
        try:
            # Cargar el archivo CSV usando pandas con el delimitador correcto (;)
            df = pd.read_csv(file_path, delimiter=';')
            # Ordenar el DataFrame por la columna "TA" de menor a mayor
            df_ordenado = df.sort_values(by='TA')
            
            # Contar el número de filas en el DataFrame ordenado
            num_filas = df_ordenado.shape[0]
            

            # Verificar si el número de filas supera las 10
            if df_ordenado['TAM'].max() > 250:
                print("Error: Al menos un proceso tiene un tamaño mayor a  250.")
                bandera = 0  # Establecer la bandera en 0
            elif num_filas > 10:
                print("Error: El número de procesos supera los 10.")
                bandera = 0  # Establecer la bandera en 0
            else:
                
                bandera = 1  # Establecer la bandera en 1 si todo está en orden
                
                list_nuevo = []
                tiempo_irrupciones = []
                acumulador_ti = 0
                nro_proc = 0
                # Recorrer el DataFrame y agregar IDs de procesos a la lista de nuevos procesos
                for index, row in df_ordenado.iterrows():
                    nro_proc = nro_proc + 1
                    id = str(row['ID'])
                    ta = int(row['TA'])
                    ti = int(row['TI'])
                    tam = int(row['TAM'])
                    acumulador_ti += ti
                    proceso = Proceso(id,ta,ti,tam)
                    list_nuevo.append(proceso)
                    irrupcion = Info_irrupcion (id,ti)
                    tiempo_irrupciones.append (irrupcion)

                info = []
                for i in range (0, len(list_nuevo)):
                    info.append(list_nuevo[i].id)
                print (f"cola de nuevos {info}")
                print("\n")

                
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            bandera = 0  # Establecer la bandera en 0 en caso de error

#colas
list_listo = []
list_listo_susp = []
list_termi = []
list_ejec = []
tiempo = list_nuevo[0].ta
acumtrp = 0  #para trp
acumEspera = 0 #para tiempo de espera promedio
#memoria
so = 100  #sist op
part1 = Particiones(60,0,0,"")
part2 = Particiones(120,0,0,"")
part3 = Particiones(250,0,0,"")
mem = [so,part1,part2,part3] 
if bandera ==1: 
    while (len(list_termi)!= nro_proc):  #ciclo principal
        print (f"Tiempo: {tiempo}")  #informe de tiempo
        if (len(list_nuevo)>0):  #si hay alguno en la cola de nuevo
            if tiempo == list_nuevo[0].ta:  #si su tiempo de arribo es igual a mi tiempo actual veo que onda
                if (len(list_listo)<4):  #espacio en cola de listos
                    entra_a_listo = list_nuevo[0] # no hago pop todavia, si el proceso puede entrar a una particion, recien hace pop en el procedimiento linea 48 y 60
                    Best_FIT ()
                else:  #si no hay espacio en listos, a ver q onda susp
                    if (len(list_listo_susp)<3): #hay espacio
                        a_listo_susp = list_nuevo.pop(0)  #ahi si hago pop y lo mando a susp
                        list_listo_susp.append (a_listo_susp)

            #si no entro por ningun lado sigue en nuevo
        ejecutar = list_listo[0]  #no hago pop de lista de listo por algo
        ti_aux = ejecutar.ti 
        quantum = 0  #es el quantum de round robin
        print (f"Proceso: {ejecutar.id} entra a ejecucion")
        while (ti_aux > 0 and quantum !=4):
            if (len(list_nuevo)>0):  #si en el mismo tiempo que el loko entra a ejecutar, puede ser el TA de un proceso nuevo, hace lo mismo q lin 152
                if tiempo == list_nuevo[0].ta: #arribo un nuevo proceso
                    if (len(list_listo)<4):
                        entra_a_listo = list_nuevo[0]
                        Best_FIT ()

                    else:
                        if (len(list_listo_susp)<3):
                            a_listo_susp = list_nuevo.pop(0)
                            print (f"entra susp:{a_listo_susp.id}")
                            list_listo_susp.append (a_listo_susp)
            
            quantum = quantum+1  #cosas obvias las que hago aca
            ti_aux = ti_aux - 1
            ejecutar.ti = ti_aux
            tiempo = tiempo + 1

        
        if (ti_aux==0): #el loko se termino de ejecutar, libero memoria y cola de listo
            print (f"Tiempo: {tiempo}")
            print (f"El proceso {ejecutar.id} termino de ejecutarse")
            calculoR = tiempo - ejecutar.ta  #calculo de TR
            print (f"Tiempo de retorno del proceso {ejecutar.id} es: {calculoR}")
            acumtrp= calculoR + acumtrp  #para TRP
            for i in range (0,len (tiempo_irrupciones)):
                if tiempo_irrupciones[i].id == ejecutar.id :
                    calculoE = calculoR - tiempo_irrupciones[i].ti
                    break
            
            
            acumEspera = calculoE + acumEspera  #calculo de TEP
            list_listo.pop(0)  #aca recien hago el pop , no lo hago en la 161
            for j in range (1,4):  #busco en las particiones para liberarlo
                
                if mem[j].proc == ejecutar.id: # libero la particion, pq encontro al proceso
                    mem[j].proc = ""
                    mem[j].bloq = 0
                    mem[j].FI = 0
                    print (f"Se libero particion {j}")
                    list_termi.append (ejecutar.id)  #lo mando a terminado
                    
                    
                    if len(list_listo_susp) > 0: # me fijo si hay alguno en listo y susp
                        sale_de_susp = list_listo_susp[0] #saco al primero de listo y susp y lo mando a listo (no hago pop tdv pq debo buscar particion)
                        
                        ###best fit pero jugando con lista de listos_susp <- IMPORTANTE

                        parti = []  # Lista para almacenar las fragmentaciones internas positivas
                        names = []  # Lista para almacenar los nombres correspondientes a las particiones
            
                        rest1 = mem[1].tam - sale_de_susp.tam
                        rest2 = mem[2].tam - sale_de_susp.tam 
                        rest3 = mem[3].tam - sale_de_susp.tam
                        if rest1 > 0 :
                            parti.append(rest1)
                            names.append("part1")
                        if rest2 > 0 :
                            parti.append(rest2)
                            names.append("part2")
                        if rest3 > 0  :
                            parti.append(rest3)
                            names.append("part3")
                        minimo = min(parti)  # Buscar la mínima fragmentación interna
                        posm = parti.index(minimo)  # Obtener la posición de la mínima fragmentación interna en parti
                        pos = names[posm]  # Obtener el nombre de la partición correspondiente

                        if pos == "part1":
                            posn = 1  # Índice de la partición p1 en la lista particiones_mem
                        elif pos == "part2":
                            posn = 2  # Índice de la partición p2 en la lista particiones_mem
                        else:
                            posn = 3  # Índice de la partición p3 en la lista particiones_mem

                        
                        if (mem[posn].bloq == 0): #no hay nada  
                            
                            resta = (mem[posn].tam - mem[posn].tam)+ minimo
                            mem[posn].FI = resta
                            mem[posn].bloq = 1
                            mem[posn].proc = sale_de_susp.id
                            list_listo.append (sale_de_susp)#al que salio de list y susp lo mando a listo, pq encontro particion
                            print(f"El proceso de id: {mem[posn].proc}, entro en memoria, se encuentra en la particion {posn}")
                            list_listo_susp.pop(0)  #aca recien hago pop pq encontro particion
                        else: #buscar una libre y chau
                            for i in range (1,4):
                                if (mem[i].bloq == 0): #particion libre
                                    
                                    resta = mem[i].tam - sale_de_susp.tam
                                    if resta > 0 : # puede entrar el loko
                                        mem[i].FI = resta
                                        mem[i].bloq = 1
                                        mem[i].proc = sale_de_susp.id
                                        print(f"El proceso de id: {mem[i].proc}, entro en memoria, se encuentra en la particion {i}")
                                        list_listo.append (sale_de_susp)
                                        list_listo_susp.pop(0)  
                                        break #rompo el for 
                        #####
                        info = []  #info al pedo cpz
                        for i in range (0, len(list_listo_susp)):
                            info.append(list_listo_susp[i].id)
                        print (f"cola de listos suspendidos {info}")
                        print("\n")
        else: #el loko no termino su irrupcion lo mando al final de la cola de listo 
            list_listo.pop(0)
            print (f"Al proceso {ejecutar.id} le queda {ejecutar.ti} para terminar su ejecucion")
            list_listo.append (ejecutar)  #lo mando al final de cola de listos
            info = []
            for i in range (0, len(list_listo)):
                info.append(list_listo[i].id)
            print (f"cola de listos {info}")
        

        #tiempo de retorno y espera para cada proceso y los respectivos tiempos promedios.
    
    print (nro_proc)
    trp = acumtrp / nro_proc 
    print (f"Tiempo de retorno promedio: {trp} unidades de tiempo")
    tep = acumEspera / nro_proc
    print (f"Tiempo de espera promedio: {tep} unidades de tiempo")
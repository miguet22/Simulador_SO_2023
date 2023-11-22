


import pandas as pd
import tkinter.filedialog as filedialog
import time
import os 

dir_part1 = "0x7F2A9C203C10"
dir_part2 = "0xABF8D764EEF2"
dir_part3 = "0x215B3F8A72C5"

def print_procesos(id_pros,parti,tam,direc,FI):
    print('| {:<15} | {:<15}   | {:<15}    |   {:<15}|  {:<15}|'.format(id_pros,parti,direc,tam,FI))
    print("-------------------------------------------------------------------------------------------------")
    
def print_listos ():
    info = []
    for i in range (0, len(list_listo)):
        info.append(list_listo[i].id)
    print("----------------------------")
    print("ESTADO DE LA COLA DE LISTO |")
    print("----------------------------")
    print (f"{info}")    

def print_titulo_mem ():
    print("*  -------------------------------------------------------------------------------------------- *")
    print('|                                     - MEMORIA -                                               |')
    print('*  -------------------------------------------------------------------------------------------- *')
    print('| {:<15} |  {:<15}  | {:<15}    |  {:<15} | {:<15} |'.format('Id Proceso','Particion', 'Tamaño (kb)',"Dir de inicio",'Frag. Int (kb)'))
    print("-------------------------------------------------------------------------------------------------")
    print_procesos (mem[1].proc,1,dir_part1,mem[1].tam,mem[1].FI)
                
    print_procesos (mem[2].proc,2,dir_part2,mem[2].tam,mem[2].FI)
    
    print_procesos (mem[3].proc,3,dir_part3,mem[3].tam,mem[3].FI)
    print("\n")


def print_cola_list_susp ():
    info = []
    for i in range (0, len(list_listo_susp)):
        info.append(list_listo_susp[i].id)
    print("---------------------------------------")
    print("ESTADO DE LA COLA DE LISTO/SUSPENDIDO |")
    print("---------------------------------------")
    print (f"{info}")
    print("\n")

def print_procesador ():
    print("\n")
    print("-----------------------")
    print("ESTADO DEL PROCESADOR |")
    print("-----------------------")
    print(f"El proceso {ejecutar.id} entra a ejecucion")
    print("\n")

def Best_FIT ():
    global salio_de_nuevo, entro_el_proceso
    salio_de_nuevo ="si"
    ## aca arranca best fit
    parti = []  # Lista para almacenar las fragmentaciones internas positivas
    names = []  # Lista para almacenar los nombres correspondientes a las particiones
    
    rest1 = mem[1].tam - entra_a_listo.tam
    rest2 = mem[2].tam - entra_a_listo.tam 
    rest3 = mem[3].tam - entra_a_listo.tam


    if rest1 >= 0 :
        parti.append(rest1)
        names.append("part1")
        

    if rest2 >= 0 :
        parti.append(rest2)
        names.append("part2")
        

    if rest3 >= 0  :
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
        
        entro_el_proceso = "si"
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
                    
                    list_listo.append (entra_a_listo)
                    list_nuevo.pop(0)
                    entro_el_proceso = "si"
                    
                    cargado = "si"
                    break #rompo el for 
        if cargado == "no" :
            if (len(list_listo_susp)<2):  #salio del for, no encontro ninguna particion disponible, lo mando a list y susp si es que hay espacio
                a_listo_susp = list_nuevo.pop(0)
                list_listo_susp.append (a_listo_susp)
                print (f"Proceso {a_listo_susp.id} entro a cola de listo/suspendido")
                print("\n")
                print_cola_list_susp ()
            else:
                print (f"El proceso {entra_a_listo.id} no entro ni a memoria ni a cola de listo/susp, queda en cola de nuevos")
                salio_de_nuevo = "no"

             #si en la lista de suspendidos hay mas de 2, va a seguir en nuevo, nunca hace el pop
            

def Best_Fit_listysusp ():
    global entro_uno_de_susp, cargado
    parti = []  # Lista para almacenar las fragmentaciones internas positivas
    names = []  # Lista para almacenar los nombres correspondientes a las particiones

    rest1 = mem[1].tam - sale.tam
    rest2 = mem[2].tam - sale.tam 
    rest3 = mem[3].tam - sale.tam
    if rest1 >= 0 :
        parti.append(rest1)
        names.append("part1")
    if rest2 >= 0 :
        parti.append(rest2)
        names.append("part2")
    if rest3 >= 0  :
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
        mem[posn].proc = sale.id
        list_listo.append (sale)#al que salio de list y susp lo mando a listo, pq encontro particion

        
        if susp == 1:
            
            list_listo_susp.pop(cont)  #aca recien hago pop pq encontro particion
            entro_uno_de_susp = "si"
            cargado = "si"
        else:
            if nuevo ==1:
                list_nuevo.pop (0)
                cargado = "si"

        if (len(list_listo_susp)<3):  # si en mi lista de susp hay 0 o 1 proceso 
            
            if (len(list_nuevo)>0): #si queda alguno en nuevos lo mando a listo_susp
                entra_a_susp = list_nuevo.pop (0)  #aca hago el pop
                list_listo_susp.append (entra_a_susp)
                print (f"Proceso {entra_a_susp.id} entro a cola de listo/suspendido")
                print("\n")
                print_cola_list_susp ()
             
    else: #buscar una libre y chau
        for i in range (1,4):
            if (mem[i].bloq == 0): #particion libre
                
                resta = mem[i].tam - sale.tam
                if resta > 0 : # puede entrar el loko
                    mem[i].FI = resta
                    mem[i].bloq = 1
                    mem[i].proc = sale.id
                    
                    
                    list_listo.append (sale)

                    if susp == 1:
                        list_listo_susp.pop(0)  #aca recien hago pop pq encontro particion , banderas para ver en cual hago el pop
                        entro_uno_de_susp = "si"
                        cargado = "si"
                    else:
                        if nuevo ==1:
                            list_nuevo.pop (0)
                            cargado = "si"

                    if (len(list_listo_susp)<2):  
                        if (len(list_nuevo)>0):
                            entra_a_susp = list_nuevo.pop (0)
                            list_listo_susp.append (entra_a_susp)
                            print (f"Proceso {entra_a_susp.id} entro a cola de listo/suspendido")
                            print("\n")
                            print_cola_list_susp ()
                        
                    break #rompo el for 
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
        

class Info_irrupcion (object):  #lo creo para calcular TE
    def __init__(self,id,ti):
        self.id = str (id)
        self.ti = int (ti)

print ("                     SIMULADOR DE ASIGNACION DE MEMORIA         ")
print ("                        Y PLANIFICACION DE PROCESOS        ")
print ("                      ++Hecho por el grupo SI3M.exe++        ")
print ("\n")
print ("A continuacion se abrira su explorador de archivos...")
print ("Solo apareceran los archivos .csv")
time.sleep (1.2)
    ## aca arranca el programa realizando la carga del archvio

bandera=0    
file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  #solo busca uno que termina en .csv
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
            print("Error: Al menos un proceso tiene un tamaño mayor a  250k.")
            bandera = 0  # Establecer la bandera en 0
        elif num_filas > 10:
            print("Error: El número de procesos supera los 10.")
            bandera = 0  # Establecer la bandera en 0
        else:
            
            bandera = 1  # Establecer la bandera en 1 si todo está en orden
            
            list_nuevo = []
            tiempo_irrupciones = []
            info_procesos_te_y_tr = []
            acumulador_ti = 0
            nro_proc = 0
            tiempos_espera = []
            tiempos_retorno = []

            # Recorrer el DataFrame y agregar IDs de procesos a la lista de nuevos procesos
            for index, row in df_ordenado.iterrows():
                nro_proc = nro_proc + 1
                id = str(row['ID'])
                ta = int(row['TA'])
                ti = int(row['TI'])
                tam = int(row['TAM'])
                acumulador_ti += ti
                info_procesos_te_y_tr.append (id)
                tiempos_espera.append (0)
                tiempos_retorno.append (0)
                proceso = Proceso(id,ta,ti,tam)
                list_nuevo.append(proceso)
                irrupcion = Info_irrupcion (id,ti)  #creo una clase con id y tiempo de irrupcion del proceso
                tiempo_irrupciones.append (irrupcion) # guardo la clase en un array
           

            info = []
            print('\n')
            print('* ----------------------------------------------------------------------- *')
            print('|          - Procesos cargados para realizar la simulacion -              |')
            print('* ----------------------------------------------------------------------- *')
            print('| {:<15} | {:<15}| {:<15} | {:<15}    | '.format('ID','TA','TI', 'TAM (kb)'))
            for i in range (0, len(list_nuevo)):
                info.append(list_nuevo[i].id)
                print('| {:<15} | {:<15}| {:<15} | {:<15}    | '.format(list_nuevo[i].id, list_nuevo[i].ta, list_nuevo[i].ti, list_nuevo[i].tam))
            print('* ----------------------------------------------------------------------- *')
            print("\n")
            print("----------------------------")
            print("ESTADO DE LA COLA DE NUEVO |")
            print("----------------------------")
            print (f"{info}")
            input("\nPresione enter para continuar...") #este si va bien
            os.system('cls')
            tiempo = list_nuevo[0].ta  #tiempo de inicio del programa


            
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        bandera = 0  # Establecer la bandera en 0 en caso de error

#colas
list_listo = []
list_listo_susp = []
list_termi = []
list_ejec = []

acumtrp = 0  #para trp
acumEspera = 0 #para tiempo de espera promedio
procesos_termi = 0 #esto es para la matriz de  informes
#memoria
so = 100  #sist op
part1 = Particiones(60,0,0,"")
part2 = Particiones(120,0,0,"")
part3 = Particiones(250,0,0,"")
mem = [so,part1,part2,part3]  #array de memoria

#banderas para informaciones
mostre_al_final = "no"

if bandera ==1:
    
    while (len(list_termi)!= nro_proc):  #ciclo principal
        
        if mostre_al_final == "no" :  #si no lo mostre al fina lo muestro
            print('------------')
            print (f"Tiempo: {tiempo}  |")  #informe de tiempo
            print('------------')
            print("\n")
            mostre_al_inicio = "si"
        
        if (len(list_nuevo)>0):  #si hay alguno en la cola de nuevo 
            
            
            while tiempo == list_nuevo[0].ta:  #si su tiempo de arribo es igual a mi tiempo actual veo que hacer, con el ciclo proceso todos los procesos los cuales sus TA = tiempo actual
                
                if (len(list_listo)<3):  # hay espacio en cola de listos
                    entra_a_listo = list_nuevo[0] # no hago pop todavia, si el proceso puede entrar a una particion, recien hace pop en el procedimiento BEST FIT linea 48 y 60
                    salio_de_nuevo = "si"
                    
                    entro_el_proceso = "no"
                    Best_FIT ()
                    
                    
                    if entro_el_proceso == "si":
                        print (f"El proceso {entra_a_listo.id} se cargo en memoria")
                        print ("\n")
                        print_titulo_mem ()
                    
                    if (len(list_nuevo)==0):  #si hizo un pop en el best fit, y nuevos quedo a 0 rompemos el ciclo de la linea 170
                        break
                    if (salio_de_nuevo == "no"):
                        break
                else:
                    if (len(list_listo_susp)<2):  
                        a_listo_susp = list_nuevo.pop(0)
                        list_listo_susp.append (a_listo_susp)
                        
                        if mostre_al_inicio != "si" :
                            print("-------------------")
                            print (f"Tiempo: {tiempo} |")
                            print("-------------------")
                            print("\n")
                        
                        print (f"Proceso : {a_listo_susp.id} entra a listo y suspendido")
                        print_cola_list_susp ()
                    else:
                        break
        
        if (len (list_listo) > 0):   #si hay alguno en listos lo ejecutamos
            ejecutar = list_listo[0]  #no hago pop de lista de listo todavia, OJO: EN LA TEORIA SI UNO SE EJECUTA SALE DE LISTO, pero a fines practicos nosotros lo mantenemos
            ti_aux = ejecutar.ti   
            quantum = 0  #es el quantum de round robin
            print_procesador ()
            while (ti_aux > 0 and quantum !=2):
                if (len(list_nuevo)>0):  #si en el mismo tiempo que el  entra a ejecutar, puede ser el TA de un proceso nuevo, hace lo mismo q lin 152
                    entro_al_while = "no"
                    while tiempo == list_nuevo[0].ta: #arriba uno o varios proceso
                        entro_al_while = "si"
                        if (len(list_listo)<3):  
                            entra_a_listo = list_nuevo[0]
                            if mostre_al_inicio != "si" :
                                print('------------')
                                print (f"Tiempo : {tiempo}  |")  #informe de tiempo
                                print('------------')
                                print("\n")

                            entro_el_proceso = "no"    
                            Best_FIT ()
                            
                            if entro_el_proceso == "si":
                                print (f"El proceso {entra_a_listo.id} se cargo en memoria")
                                print_titulo_mem ()

                            if (len(list_nuevo) == 0):
                                break
                            if (salio_de_nuevo == "no"):
                                break
                        else:
                            if (len(list_listo_susp)<2):  
                                a_listo_susp = list_nuevo.pop(0)
                                list_listo_susp.append (a_listo_susp)
                                
                                if mostre_al_inicio != "si" :
                                    print("-------------------")
                                    print (f"Tiempoxxx: {tiempo} |")
                                    print("-------------------")
                                    print("\n")
                                
                                print (f"Proceso : {a_listo_susp.id} entra a listo y suspendido")
                                print_cola_list_susp ()

                                
                                if len (list_nuevo) == 0:  #si ya me comi todos los proceso rompo el while
                                    break
                            
                            else:  #si no entro x ningun lado rompo el while pq sino entra en bucle infinito, 
                                break
                quantum = quantum+1  #cosas obvias las que hago aca
                ti_aux = ti_aux - 1
                ejecutar.ti = ti_aux
                tiempo = tiempo + 1
                input ("Presione enter para continuar...")
                os.system ("cls")
                print('------------')
                print (f"Tiempo: {tiempo}  |")  #informe de tiempo
                print('------------')
                print("\n")
                mostre_al_final = "si"
                mostre_al_inicio = "si"

            if (ti_aux==0): #el PROCESO se termino de ejecutar, libero memoria y cola de listo
                print("-----------------------")
                print("ESTADO DEL PROCESADOR |")
                print("-----------------------")
                print(f"El proceso {ejecutar.id} termino de ejecutarse") 
                print("\n")
                
                calculoR = tiempo - ejecutar.ta  #calculo de TR
                
                acumtrp= calculoR + acumtrp  #para TRP
                for i in range (0,len (tiempo_irrupciones)):  #busco en mi array de irrupciones el TI de este proceso
                    if tiempo_irrupciones[i].id == ejecutar.id :  #si los id coinciden estoy en ese proceso
                        calculoE = calculoR - tiempo_irrupciones[i].ti  #hago el calculo de Espera
                        break
                
                for j in range (0,len (info_procesos_te_y_tr)):
                    if (info_procesos_te_y_tr [j] == ejecutar.id):
                        resg = j
                        break
                
                tiempos_espera [j] = str (calculoE) 
                tiempos_retorno [j] = str (calculoR) 
                    
                
                acumEspera = calculoE + acumEspera  #calculo de TEP
                list_listo.pop(0)  #aca recien hago el pop , no lo hago en la 161

                for j in range (1,4):  #busco en las particiones para liberarlo
                    
                    if mem[j].proc == ejecutar.id: # libero la particion, pq encontro al proceso
                        mem[j].proc = ""
                        mem[j].bloq = 0
                        mem[j].FI = 0
                        list_termi.append (ejecutar.id)  #lo mando a terminado
                        salio = "no"
                        susp = 0
                        nuevo = 0
                        entro_uno_de_susp = "no"
                        print_titulo_mem ()
                        print ("\n")
                        if (len(list_listo_susp)>0):   #si hay alguno en listo y susp, lo saco de ahi PRIORIDAD TOMADA X EL GRUPO
                            cont = 0
                            while (cont < len (list_listo_susp)):
                                sale = list_listo_susp[cont] #saco al primero de listo y susp y lo mando a listo (no hago pop tdv pq debo buscar particion)
                                susp = 1
                                nuevo =0
                                cargado = "no"
                                Best_Fit_listysusp ()  #Deberia informar algo  #si ya entro deberia romper el bucle
                                cont = cont + 1
                                if cargado == "si":
                                    break
                            
                        if (entro_uno_de_susp == "no"):
                            if (len(list_nuevo)>0 ) and (list_nuevo[0].ta == tiempo):
                                susp = 0
                                sale = list_nuevo[0]
                                nuevo = 1
                                cargado = "no"
                                Best_Fit_listysusp ()  #informar algo
                        #else:
                            #if (len(list_nuevo)> 0 and (len (list_listo_susp)<3)):
                               # x = list_nuevo.pop (0)
                                #list_listo_susp.append (x)

                        
                        if cargado == "si":
                            print (f"Proceso {sale.id} cargado a memoria")
                            print_titulo_mem ()
                            cargado = "no"
                            break                        
                        ###best fit pero jugando con lista de listos_susp <- IMPORTANTE
            else:
                
                list_listo.pop(0)

                if mostre_al_inicio != "si" :
                    print('------------')
                    print (f"Tiempo: {tiempo}  |")  #informe de tiempo
                    print('------------')
                    print("\n")

                print("---------------------------------------------")
                print("ESTADO DEL PROCESO QUE SE ESTABA EJECUTANDO |")
                print("---------------------------------------------")
                if (ejecutar.ti == 1):
                    print (f"Al proceso {ejecutar.id} le queda {ejecutar.ti} unidad de tiempo para terminar su ejecucion")
                else: 
                    print (f"Al proceso {ejecutar.id} le queda {ejecutar.ti} unidades de tiempo para terminar su ejecucion")   
                print("\n")
                list_listo.append (ejecutar)  #lo mando al final de cola de listos
                print_listos ()

        else :
            if (len(list_nuevo) >0): # corremos el tiempo hasta que arribe uno
                while (list_nuevo[0].ta != tiempo):
                    tiempo = tiempo + 1
        
    input("\nPresione enter para mostrar informes finales...")
    os.system('cls')
    print('\n')

    print("*----------------------------------------------------------------------- *")
    print("| INFORMACION ESTADISTICA DE TIEMPOS DE ESPERA Y RETORNO DE LOS PROCESOS |")
    print("*----------------------------------------------------------------------- *")
    aa = []
    for i in range (0,len (info_procesos_te_y_tr)):
        aa.append ('')
    datos = {'   Proceso   ': info_procesos_te_y_tr,'   Tiempo de Espera (u.t)   ': tiempos_espera, '   Tiempo de Retorno (u.t)   ': tiempos_retorno}
    matriz = pd.DataFrame(data=datos, index= aa)
    print(matriz.to_string(justify='center'))
    print("--------------------------------------------------------------------------")
    print ('\n')
    trp = acumtrp / nro_proc 
    print("----------------------------")
    print("TIEMPO DE RETORNO PROMEDIO |")
    print("----------------------------")
    print (f"{round(trp,2)} unidades de tiempo")
    print("\n")
    tep = acumEspera / nro_proc
    print("----------------------------")
    print("TIEMPO DE ESPERA PROMEDIO |")
    print("----------------------------")
    print (f"{round(tep,2)} unidades de tiempo")
    print("\n")
    print('Simulacion finalizada.')
    input("\nPresione enter para continuar...")
    
    
else:
    input("Hubo error, presione enter para finalizar...")
    print("\n")
    os.system('cls')
                    
                    
            
                
        

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

    
    if (mem[posn].bloq == 0): #no hay nada  
        
        resta = (mem[posn].tam - mem[posn].tam)+ minimo
        mem[posn].FI = resta
        mem[posn].bloq = 1
        mem[posn].proc = entra_a_listo.id
        list_listo.append (entra_a_listo)
        print(f"El proceso de id: {mem[posn].proc}, entro en memoria, se encuentra en la particion {posn}")
    else: #buscar una libre y chau
        for i in range (1,4):
            if (mem[i].bloq == 0):#particion libre
                resta = mem[i].tam - entra_a_listo.tam
                if resta > 0 : # puede entrar el loko
                    
                    mem[i].FI = resta
                    mem[i].bloq = 1
                    mem[i].proc = entra_a_listo.id
                    print(f"El proceso de id: {mem[i].proc}, entro en memoria, se encuentra en la particion {posn}")
                    list_listo.append (entra_a_listo)
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
gant = []
tiempo = list_nuevo[0].ta

#memoria
so = 100  #sist op
part1 = Particiones(60,0,0,"")
part2 = Particiones(120,0,0,"")
part3 = Particiones(250,0,0,"")
mem = [so,part1,part2,part3] 
entro = "no"
if bandera ==1: 
    while (len(list_termi)!= nro_proc):
        if (len(list_nuevo)>0):
            if tiempo == list_nuevo[0].ta:
                if (len(list_listo)<4):
                    entra_a_listo = list_nuevo.pop(0)
                    Best_FIT ()
                else:
                    if (len(list_listo_susp)<3):
                        a_listo_susp = list_nuevo.pop(0)
                        list_listo_susp.append (a_listo_susp)

            #si no entro por ningun lado sigue en nuevo
        ejecutar = list_listo.pop(0)
        ti_aux = ejecutar.ti
        quantum = 0  #es el quantum de round robin
        print (f"Tiempo: {tiempo}, proceso: {ejecutar.id} entra a ejecucion")
        while (ti_aux > 0 and quantum !=2):
            if (len(list_nuevo)>0):
                if tiempo == list_nuevo[0].ta: #arribo un nuevo proceso
                    if (len(list_listo)<4):
                        entra_a_listo = list_nuevo.pop(0)
                        Best_FIT ()
                    else:
                        if (len(list_listo_susp)<3):
                            a_listo_susp = list_nuevo.pop(0)
                            list_listo_susp.append (a_listo_susp)
            
            quantum = quantum+1
            ti_aux = ti_aux - 1
            ejecutar.ti = ti_aux
            tiempo = tiempo + 1

        
        if (ti_aux==0): #el loko se termino de ejecutar libero memoria y cola de listo
            print (f"Tiempo {tiempo} el proceso {ejecutar.id} termino de ejecutarse")
            for j in range (1,4):
                if mem[j].proc == ejecutar.id: # libero la particion
                    mem[j].proc = ""
                    mem[j].bloq = 0
                    mem[j].FI = 0
                    list_termi.append (ejecutar.id)  #lo mando a terminado
                    print (f"lista terminados {len(list_termi)}")
                    
                    if len(list_listo_susp) > 0:
                        sale_de_susp = list_listo_susp.pop(0) #saco uno de listo y susp y lo mando a listo
                        list_listo.append (sale_de_susp)
                        info = []
                        for i in range (0, len(list_listo_susp)):
                            info.append(list_listo_susp[i].id)
                        print (f"cola de listos suspendidos {info}")
                        print("\n")
        else: #el loko no termino su irrupcion lo mando al final de la cola de listo 
            print (f"Al proceso {ejecutar.id} le queda {ejecutar.ti} para terminar su ejecucion")
            list_listo.append (entra_a_listo)
            info = []
            for i in range (0, len(list_listo)):
                info.append(list_listo[i].id)
            print (f"cola de listos {info}")
        
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
        
        mem2.insert (posn,proceso) #lo meto en mi arreglo aux

        print(f"El proceso de id: {id}, entro en memoria, se encuentra en la particion {posn}")

    else:  #hay que hacer un swap
        a_list_susp = mem2.pop(posn)  #arreglo auxiliar
        list_listo_susp.append (a_list_susp)

        resta = (mem[posn].tam - mem[posn].tam)+ minimo
        mem[posn].FI = resta
        mem[posn].bloq = 1

    
        print (f"Proceso {a_list_susp.id} a cola de listos_suspendidos")

        #deberiamos pregutnar si de verdad quiere esto
        print ("INFORMACION DE LAS PARTICIONES")
        for i in range(1, 4):  
            print (f"Particion {i}")

            if (mem[i].FI > 0) :
                print (f"Tiene fragmentacion interna de: {mem[i].FI}")
            else:
                print ("Esta libre")

class Particiones (object):
    def __init__(self,tam,bloq,FI) :
        self.tam = int(tam)  #tamaño parti 
        self.bloq = bloq # esta usada o no
        self.FI = int(FI) # frag interna
    

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
                list_nuevo2 = []
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
                    list_nuevo2.append (proceso)

                info = []
                for i in range (0, len(list_nuevo2)):
                    info.append(list_nuevo2[i].id)
                print (f"cola de nuevos2 {info}")
                print("\n")

                print (nro_proc)
                
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            bandera = 0  # Establecer la bandera en 0 en caso de error


#colas
list_listo = []
list_listo_susp = []
list_termi = []
list_ejec = []
gant = []
tiempo = list_nuevo2[0].ta
cargue = "NO"



#memoria
so = 100  #sist op
part1 = Particiones(60,0,0)
part2 = Particiones(120,0,0)
part3 = Particiones(250,0,0)
mem = [so,part1,part2,part3] 
mem2=[so," "," "," "]

if bandera ==1:
    while (len (list_termi) != nro_proc):
        if (len(list_listo) <6):  # respetar multiprog
            if (len(list_nuevo)!=0): # lo saco de lista de nuevos
                if cargue == "NO" :
                    entra_a_listo = list_nuevo.pop(0)
                    id= entra_a_listo.id
                    ta = entra_a_listo.ta
                    ti = entra_a_listo.ti
                    tam= entra_a_listo.tam
                    proceso = Proceso(id,ta,ti,tam)
                    list_listo.append(proceso)  #aca una vez que entro a cola de listos, veo si lo ejecuto, entra a mem
                    Best_FIT()          
            
            proceso_cargar = list_listo.pop (0)
            q = tiempo  #tiempo es mi reloj general
            ti_aux = proceso_cargar.ti
            quantum = 0  #es el quantum de round robin
            print (f"Tiempo: {q}, proceso: {proceso_cargar.id} entra a ejecucion")
            while (ti_aux> 0 and quantum !=2):
                quantum = quantum+1
                ti_aux = ti_aux - 1
                proceso_cargar.ti = ti_aux
                print (f"Meto a gant: {proceso_cargar.id}")
                gant.insert(q,proceso_cargar)
                 # debo ver si en este q no ingresa es TA de alguno, como para informar su arribo a cola de listo

                if (len(list_nuevo) > 0):
                    if (q == list_nuevo[0].ta) : #hago append del proceso en list_nuevo y dsp el append del otro que termino su ejec pero falta ti
                        cargue = "SI"  #bandera para no volver cargarlo arriba
                        entra_a_listo = list_nuevo.pop(0)
                        id= entra_a_listo.id
                        ta = entra_a_listo.ta
                        ti = entra_a_listo.ti
                        tam= entra_a_listo.tam
                        proceso = Proceso(id,ta,ti,tam)
                        print (f"tiempo {q}, {proceso.id} entra a cola de listos")
                        list_listo.append(proceso)  
                        Best_FIT ()
                    else: 
                        cargue = "NO" #significa que no cargue nada
                q=q+1
            
            if (ti_aux == 0): #lo mando a terminado
                print (f"Tiempo: {q}, {proceso_cargar.id} termino ejecucion")
                list_termi.append (proceso_cargar)  
                info = []
                for i in range (0,len (list_listo)):
                    info.append (list_listo[i].id)
                
                print (f"Cola de listos: {info}")
                info = []
                for i in range (0,len (list_termi)):
                    info.append (list_termi[i].id)
                
               
                    
                print (f"Cola de terminados: {info}")
                print ("\n")
                
            else:                             
                proceso_cargar.ti = ti_aux
                print (f"Tiempo: {q}")
                print (f"Al proceso {proceso_cargar.id} le quedan {ti_aux} para terminar su ejec")
                if (len(list_nuevo)>0):
                    if (q == list_nuevo[0].ta) : #hago append del proceso en list_nuevo y dsp el append del otro que termino su ejec pero falta ti
                        cargue = "SI"  #bandera para no volver cargarlo arriba
                        entra_a_listo = list_nuevo.pop(0)
                        id= entra_a_listo.id
                        ta = entra_a_listo.ta
                        ti = entra_a_listo.ti
                        tam= entra_a_listo.tam
                        proceso = Proceso(id,ta,ti,tam)
                        list_listo.append(proceso)  
                        Best_FIT ()
                    else: 
                        cargue = "NO" #significa que no cargue nada

                list_listo.append (proceso_cargar)  #mando el proceso q termino su ejec al final de la cola
                info=[]
                for i in range (0,len(list_listo)):
                    info.append(list_listo[i].id)
                print ("Cola de listos:", info)
                print ("\n")
            
            tiempo = q
    info=[]
    for j in range (0,len (gant)):
        info.append (gant[j].id)
    print (f"GANT: {info}")
else:
    print("como hubo un problema finaliza el simulador")
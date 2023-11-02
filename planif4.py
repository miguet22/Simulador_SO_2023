import pandas as pd
import tkinter.filedialog as filedialog
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
                arch = df_ordenado
                bandera = 1  # Establecer la bandera en 1 si todo está en orden
                list_nuevo = []
                list_nuevo2 = []
                
                # Acceder a la columna 'TA' de la primera fila
                
                acumulador_ti = 0
                # Recorrer el DataFrame y agregar IDs de procesos a la lista de nuevos procesos
                for index, row in df_ordenado.iterrows():
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
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            bandera = 0  # Establecer la bandera en 0 en caso de error


#colas
list_listo = []
list_listo_susp = []
list_termi = []
list_ejec = []
gant = []
 


if bandera ==1:
    while (len (list_termi) != len(list_nuevo2)):
        if (len(list_listo) <6):
            if (len(list_nuevo)!=0):
                entra_a_listo = list_nuevo.pop(0)
                id= entra_a_listo.id
                ta = entra_a_listo.ta
                ti = entra_a_listo.ti
                tam= entra_a_listo.tam
                proceso = Proceso(id,ta,ti,tam)
                list_listo.append(proceso)
                print (f"proceso {proceso.id} agregado a cola de listos")
            else:  
                tiempo = list_listo[0]
                while (len(list_termi) != len (list_nuevo2)):
                    prox = list_listo[1]
                    proceso_cargar = list_listo.pop (0)
                    hago = 1
                    if (proceso_cargar.ta == tiempo): #perfecto damos prioridad
                        q = tiempo  #tiempo es mi reloj general
                        ti_aux = proceso_cargar.ti
                        if ((q+1) != prox.ta): # si corro un tiempo y en ese tiempo llegue a un proceso que tiene ese ta, solamente ejecuto un tiemp
                            quantum = 0  #es el quantum de round robin
                            while (ti_aux> 0 and quantum !=2):
                                quantum = quantum+1
                                ti_aux = ti_aux - 1
                                proceso_cargar.ti = ti_aux
                                gant.insert (q,proceso_cargar)
                                q=q+1
                                

                            if (ti_aux == 0): #lo mando a terminado
                                print (f"Tiempo: {quantum}, {proceso_cargar.id} termino ejecucion")
                                list_termi.append (proceso_cargar)   
                                print (f"siguiente {prox.id}")
                            else:                             
                                proceso_cargar.ti = ti_aux
                                print (f"Al proceso {proceso_cargar.id} le quedan {ti_aux} para terminar su ejec")
                                list_listo.append (proceso_cargar)
                                info=[]
                                for i in range (0,len(list_listo)):
                                    info.append(list_listo[i].id)
                                print ("cola de listos", info)
                        else:
                            # lo corro una sola vez
                            if (ti_aux > 0):  #si tiene al menos un tiempo a ejecutar lo ejecuto
                                ti_aux = ti_aux - 1
                                q=q+1
                                gant.insert (q,proceso_cargar)
                                
                            if (ti_aux == 0) :
                                print (f"Tiempo: {q}, {proceso_cargar.id} termino ejecucion")
                                list_termi.append (proceso_cargar)   
                                print (f"siguiente {prox.id}")
                            else:
                                # lo debo meter al fin de listo
                                proceso_cargar.ti = ti_aux
                                print (f"Al proceso {proceso_cargar.id} le quedan {ti_aux} para terminar su ejec")
                                list_listo.append (proceso_cargar)
                            
                        tiempo = q 
                    else:
                        #debo buscar uno para darle prioridad 

                        print (f"lala {proceso_cargar.id}")
                        list_listo.append (proceso_cargar)
                        info=[]
                        for i in range (0,len(list_listo)):
                            info.append(list_listo[i].id)
                        print ("cola de listos", info)
                        ## aca deberia de recorrer la cola y ver si no hay ta siguiente igual a mi q actual
                        hago = 1
                        print ("ya entre al else")
                        for m in range (tiempo,acumulador_ti,2):
                            
                            for i in range (0,len(list_listo)):
                                if (tiempo == list_listo[i].ta) :
                                    hago = 0  #significa que NO HAGO lo de abajo, ya que en la cola hay alguno que tenga un ta igual mi q actual

                        #if (hago == 1):  #no hay ninguno con ta = tiemp actual

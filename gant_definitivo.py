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
        while (len(list_listo) <6):
            if (len(list_nuevo)!=0):
                entra_a_listo = list_nuevo.pop(0)
                id= entra_a_listo.id
                ta = entra_a_listo.ta
                ti = entra_a_listo.ti
                tam= entra_a_listo.tam
                proceso = Proceso(id,ta,ti,tam)
                list_listo.append(proceso)
            else:  
                tiempo = list_listo[0].ta
                while (len(list_termi) != len (list_nuevo2)):
                    proceso_cargar = list_listo.pop (0)
                    q = tiempo  #tiempo es mi reloj general
                    ti_aux = proceso_cargar.ti
                    quantum = 0  #es el quantum de round robin
                    print (f"Tiempo: {q}, proceso: {proceso_cargar.id} entra a ejecucion")
                    while (ti_aux> 0 and quantum !=2):
                        quantum = quantum+1
                        ti_aux = ti_aux - 1
                        proceso_cargar.ti = ti_aux
                        gant.insert (q,proceso_cargar)
                        q=q+1 # debo ver si en este q no ingresa es TA de alguno, como para informar su arribo

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
                        
                        if (len(list_listo) < 6):
                            band = 1 #activo bandera para poder luego cargar un proceso mas en cola de listo, respetar multiprog = 5
                            # ver esto que onda como implementarlo
                            
                        print (f"Cola de terminados: {info}")
                        print ("\n")
                        
                    else:                             
                        proceso_cargar.ti = ti_aux
                        print (f"Tiempo: {q}")
                        print (f"Al proceso {proceso_cargar.id} le quedan {ti_aux} para terminar su ejec")
                        list_listo.append (proceso_cargar)
                        info=[]
                        for i in range (0,len(list_listo)):
                            info.append(list_listo[i].id)
                        print ("Cola de listos:", info)
                        print ("\n")
                    
                    tiempo = q
                
                gant_info = []
                for i in range (0,len(gant)):
                    gant_info.append (gant[i].id)

                print ("Este diagrama solo tiene las id, lo interesante lo tiene el otro")
                print ("Diag de gant", gant_info) 
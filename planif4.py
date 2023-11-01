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
 
tiempo= list_nuevo2[0].ta
agarre = "no"
while (len (list_termi)< len (list_nuevo2)):
    while (len (list_listo)<6):
        if agarre != "si":
            a_listo = list_nuevo[0]
        if (tiempo == a_listo.ta):  #si mi proceso que arribo, no tiene un ta correspondiente al quantum deberia darle prioridad a otro
            if agarre != "si":
                a_listo = list_nuevo.pop(0)
            q= 0
            ti_aux = a_listo.ti

            while (q<2 and ti_aux >0):
                ti_aux= ti_aux-1
                a_listo.ti = ti_aux
                gant.insert (tiempo,a_listo)
                q = q+1
                
            
            if (ti_aux == 0):
                tiempo = tiempo+q
                print (f"Tiempo {tiempo}, {a_listo.id} termino su ejecucion, se va a cola de terminados")
                list_termi.append(a_listo)
                for j in range (0,len(list_nuevo2)):  #lo saco de nuevo
                    if (list_nuevo2[j].id == a_listo.id):
                        list_nuevo2.pop (j)
                        break
            else:
                a_listo.ti = ti_aux
                list_listo.append (a_listo)
                print (f"El proceso {a_listo.id}, todavia no termino de ejecutarse, le faltan {ti_aux} unidades de tiempo")
                tiempo = tiempo + q
               
        else:
            hago = 1
            print (tiempo)
            
            print(acumulador_ti)
            for m in range (tiempo,acumulador_ti,2):    #tengo que buscar en la cola de nuevos algun proceso que si tenga un ta = actual tiempo de arribo
                for i in range (0,len(list_nuevo2)):
                    print (f"tiempos de arribo {list_nuevo2[i].ta}")
                    if (m == list_nuevo2[i].ta) :
                        print (f"agarre{list_nuevo2[i].id}")
                        a_listo = list_nuevo2[i]
                        hago = 0  #significa que NO HAGO lo de abajo, ya que en la cola hay alguno que tenga un ta igual mi q actual"""
                        break
            
            if (hago ==1):

                while (len (list_termi)< len (list_nuevo2)):
                    if (len(list_nuevo) > 0):
                        a_listo = list_nuevo.pop(0)
                    q= 0
                    ti_aux = a_listo.ti

                    while (q<2 and ti_aux >0):
                        ti_aux= ti_aux-1
                        a_listo.ti = ti_aux
                        gant.insert (tiempo,a_listo)
                        q = q+1
                        
                    
                    if (ti_aux == 0):
                        tiempo = tiempo + q
                        print (f"Tiempo {tiempo}, {a_listo.id} termino su ejecucion, se va a cola de terminados")
                        list_termi.append(a_listo)
                        for j in range (0,len(list_nuevo2)):  #lo saco de nuevo
                            if (list_nuevo2[j].id == a_listo.id):
                                list_nuevo2.pop (j)
                                break
                    else:
                        tiempo = tiempo + q
                        a_listo.ti = ti_aux
                        list_listo.append (a_listo)
                        print (f"El proceso {a_listo.id}, todavia no termino de ejecutarse, le faltan {ti_aux} unidades de tiempo")
                    
                    
                
for i in range (0,len (gant)):
    print (gant[i].id)
            

            


        
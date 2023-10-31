import tkinter as tk
from tkinter import filedialog
import pandas as pd
class Particiones (object):
    def __init__(self,tam,bloq,FI) :
        self.tam = int (tam)
        self.bloq = int (bloq)
        self.FI = int (FI)

class Proceso (object):
    def __init__(self,id,ta,ti,tam) :
        self.id = str (id)
        self.ta = int (ta)
        self.ti = int (ti)
        self.tam = int (tam)
# Función para abrir el buscador de archivos y cargar el archivo .csv
def cargar_csv():
    global arch  # Acceder a la variable global arch
    global bandera  # Acceder a la variable global bandera
    global nuevo
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
                nuevo = []
                
                # Acceder a la columna 'TA' de la primera fila
                

                # Recorrer el DataFrame y agregar IDs de procesos a la lista de nuevos procesos
                for index, row in df_ordenado.iterrows():
                    nuevo.append(row['ID'])

        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            bandera = 0  # Establecer la bandera en 0 en caso de error
        finally:
            # Cerrar la ventana de tkinter después de cargar y ordenar el archivo
            root.destroy()




# Crear una ventana de tkinter
root = tk.Tk()
root.title("Cargar archivo CSV ")

# Botón para abrir el buscador de archivos
button = tk.Button(root, text="Cargar archivo CSV ", command=cargar_csv)
button.pack(pady=20)

# Iniciar el bucle principal de tkinter
root.mainloop()

# La lista de procesos está disponible en la variable 'arch'
if (bandera == 1):  #si el csv tiene menos de 10 
   
    num_filas = arch.shape[0]  #guardo el numero de filas del csv en esta variable

    #colas
    listo = []
    listo_susp = []
    terminado = []
    #memoria
    so = 100
    p1 = Particiones (60,0,0)
    p2 = Particiones (120,0,0)
    p3 = Particiones (250,0,0)
    mem = [so,p1,p2,p3] 


    cont = 0 
    
    
    while (list < num_filas):   # para procesar todos los procesos del csv  CICLO PRINCIPAL

        
        procesos_carg = []
        print (f"Cola de nuevos: {nuevo}")

        for index, row in arch.iterrows():
            
            if len(listo) < 5:  # solamente vamos a poder meter 5 en el array con el cual nos iremos manejando
                id = str(row['ID'])
                ta = int(row['TA'])
                ti = int(row['TI'])
                tam = int(row['TAM'])
                
                proceso = Proceso (id,ta,ti,tam)

                ## aca arranca best fit
                parti = []  # Lista para almacenar las fragmentaciones internas positivas
                names = []  # Lista para almacenar los nombres correspondientes a las particiones

                rest1 = mem[1].tam - tam
                rest2 = mem[2].tam - tam 
                rest3 = mem[3].tam - tam


                if rest1 > 0 and (mem[1].bloq == 0):
                    parti.append(rest1)
                    names.append("p1")

                if rest2 > 0 and (mem[2].bloq == 0):
                    parti.append(rest2)
                    names.append("p2")

                if rest3 > 0 and (mem[3].bloq == 0) :
                    parti.append(rest3)
                    names.append("p3")

                if len(parti) != 0:  #si no hubo particiones va a cola de listo/susp
                    minimo = min(parti)  # Buscar la mínima fragmentación interna
                    posm = parti.index(minimo)  # Obtener la posición de la mínima fragmentación interna en parti
                    pos = names[posm]  # Obtener el nombre de la partición correspondiente

                    if pos == "p1":
                        posn = 1  # Índice de la partición p1 en la lista particiones_mem
                    elif pos == "p2":
                        posn = 2  # Índice de la partición p2 en la lista particiones_mem
                    else:
                        posn = 3  # Índice de la partición p3 en la lista particiones_mem

                    if (mem[posn].bloq == 0):
                        resta = (mem[posn].tam - mem[posn].tam)+ minimo
                        mem[posn].bloq = 1
                        mem[posn].FI = resta


                        listo.append (proceso)
                        print (f"TIEMPO:{proceso.ta}")
                        print (f"El proceso de id: {id}, entro en memoria, se encuentra en la particion {posn}")
                        
                        
                    else:  
                        listo_susp.append (proceso)
                        print (f"cola de listos suspendidos {listo_susp}")   
                else:
                    listo_susp.append (proceso)
                    

                ## fin best fit 

               
                ## informaciones 
                
                
                print ("INFORMACION DE LAS PARTICIONES")
                for i in range(1, 4):  
                    print (f"Particion {i}")

                    if (mem[i].bloq == 1) :
                        print (f"Tiene fragmentacion interna de: {mem[i].FI}, por lo que esta bloqueada")
                    else:
                        print ("Esta libre")


               
                ## aca viene round robin q = 2

                if listo: 
                    entra = listo.pop(0)
                    print (f"El proceso {entra.id} entro en ejecucion")
                    resta = entra.ti - 2
                    if (resta <= 0): 
                        
                        print (f"proceso {entra.id} terminado")
                    else:
                        proceso = Proceso (entra.id,entra.ta,(entra.ti)-2,entra.tam)
                        print (f"Al prroceso {proceso.id} le queda {proceso.ti} de tiempo para terminar su ejecucion")
                        listo.append(proceso) 
           
                ## fin round robin 
                info = []
                for i in range (0,len(listo)):
                    info.append (listo[i].id)
                print (f"Cola de listos")
                print (info)
                
                print (f"cola de listos suspendidos {listo_susp}")


            else:
                minimo = -1
                
            cont = cont + 1
        #salgo del for con 5 procesos en el array
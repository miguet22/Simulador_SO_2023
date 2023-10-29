class Proceso (object):
    def __init__(self,id,ta,ti,tam) :
        self.id = str (id)
        self.ta = int (ta)
        self.ti = int (ti)
        self.tam = int (tam)


id = 'p1'
ta = 0
ti = 5
tam = 200
proceso = Proceso (id,ta,ti,tam)


id2="p2"
ta2=0
ti2=4
tam2=100
proceso2= Proceso (id2,ta2,ti2,tam2)


listo = []
listo.append (proceso)
listo.append (proceso2)

tiem = 2
while (listo) : 
    if listo :
        print (f"Tiempo: {tiem}")
        entra = listo.pop(0)
        print (f"El proceso {entra.id} entro en ejecucion")
        resg= entra.ti
        resta = entra.ti - 2
        if (resta <= 0): 
            tiem = tiem + 1
            print (f"proceso {entra.id} terminado")
        else:
            proceso = Proceso (entra.id,entra.ta,(entra.ti)-2,entra.tam)
            print (f"Al prroceso {proceso.id} le queda {proceso.ti} de tiempo para terminar su ejecucion")
            tiem = tiem + 2
            listo.append(proceso)

    info = []

    for i in range (0,len(listo)):
            info.append (listo[i].id)
    

    print (f"Cola de listos: {info}")
        



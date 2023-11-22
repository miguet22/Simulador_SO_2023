|* -  GUÍA DE UTILIZACIÓN DEL SIMULADOR DEL GRUPO SI3M.EXE - *|
---------------------------------------------------------------

CONSIDERACIONES: #Se ejecuta en Windows.
		 #las columnas de los procesos en los archivos .csv deben ir en el siguiente orden:
					ID TA TI TAM
			ID: id del proceso, puede ser cualquier nombre.
			TA: Tiempo de arribo.
			TI: Tiempo de irrucion.
			TAM: Tamaño del proceso.
			
		¡¡Si se modifica el orden de las columnas el simulador NO funcionara!!


EJECUCION POR EJECUTABLE:
	1) EL EJECUTABLE SE ENCUENTRA EN Simulador_SO_2023_Grupo_SI3M.exe\dist\ --> EL EJECUTABLE SE LLAMA main.exe
	2) LE ABRIRÁ LA CONSOLA DONDE LUEGO PODRA ELEGIR EN EL EXPLORADOR DE ARCHIVO EL ARCHIVO .CSV.
	3) LUEGO DE ELEGIR EL MISMO EMPIEZA LA SIMULACIÓN DE PROCESOS.

EJECUCION POR CÓDIGO:
	1) INSTALAR PYTHON
	2) INSTALAR LA LIBRERIA PANDAS --> pip install pandas <-- por consola.
	3) ABRIR EL CODIGO main.py(se encuentra en Simulador_SO_2023_Grupo_SI3M.exe) en su IDLE.
	4) EJECUTARLO Y SE INICIA LA SIMULACION
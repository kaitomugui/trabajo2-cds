from multiprocessing import Process, Lock, Semaphore, Value
from time import sleep
import time



inicio = time.time()

candado = Lock()
db = Semaphore(1)

nLectores = Value("i", 0)


def leerBD(i):
    print("Lector " + str(i) + " Leyendo...\n")
    sleep(3)

def usarBasedeDatos(i):
    print("Lector " + str(i) + " Usando Lectura\n")
    sleep(4)

def lector(can, bd, nLect, i):
    estado = True
    while (estado):
        can.acquire()
        nLect.value += 1

        if nLect.value == 1:
            bd.acquire()

        can.release()

        leerBD(i)

        can.acquire()

        nLect.value -= 1

        if nLect.value == 0:
            bd.release()

        can.release()
        usarBasedeDatos(i)
        estado = False


##################
def pensarQueEscribir(i):
    print("Escritor " + str(i) + " Pensando que Escribir...\n")
    sleep(3)


def escribir(i):
    print("Escritor " + str(i) + " Escribiendo...\n")
    sleep(5)


def escritor(bd, i):
    estado = True
    while (estado):
        pensarQueEscribir(i)

        bd.acquire()
        escribir(i)
        bd.release()
        estado = False
        fin = time.time()
        print(fin - inicio)

###################################3
if __name__ == "__main__":
    # Crear Lectores
    listaLectores = []
    for i in range(0, 3):
        l = Process(target=lector, args=(candado, db, nLectores, i, ))
        l.start()
        print("Proceso ID: " + str(l.pid) + " Lector numero: " + str(i))

        listaLectores.append(l)

    # Crear Escritores
    listaEscritores = []
    for i in range(0, 3):
        esc = Process(target=escritor, args=(db, i, ))
        esc.start()
        print("Proceso ID: " + str(esc.pid) + " Escritor numero: " + str(i))
        listaEscritores.append(esc)

    # Esperar Lectores
    for l in listaLectores:
        l.join()

    # Esperar escritores
    for e in listaEscritores:
        e.join()




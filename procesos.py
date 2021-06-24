from multiprocessing import Process, Lock, Semaphore, Value
from time import sleep
from random import randint

candado = Lock()
db = Semaphore(1)

nLectores = Value("i", 0)



def leerBD(i):
    print("Lector " + str(i) + " Leyendo...\n")
    sleep(randint(3,6))


def pensarQueLeer(i):
    print("Lector " + str(i) + "  Pensando que Leer...\n")
    sleep(randint(3, 5))


def lector(can, bd, nLect, i):
    while True:
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
        sleep(5)


##################
def pensarQueEscribir(i):
    print("Escritor " + str(i) + " Pensando que Escribir...\n")
    sleep(randint(3, 5))


def escribir(i):
    print("Escritor " + str(i) + " Escribiendo...\n")
    sleep(randint(5,10))


def escritor(bd, i):
    while True:
        pensarQueEscribir(i)

        bd.acquire()
        escribir(i)
        bd.release()


###################################3
if __name__ == "__main__":
    # Crear Lectores
    listaLectores = []
    for i in range(0, 10):
        l = Process(target=lector, args=(candado, db, nLectores, i, ))
        l.start()
        print("Proceso ID: " + str(l.pid) + " Lector numero: " + str(i))

        listaLectores.append(l)

    # Crear Escritores
    listaEscritores = []
    for i in range(0, 10):
        esc = Process(target=escritor, args=(db, i, ))
        esc.start()
        print("Proceso ID: " + str(esc.pid) + " Escritor numero: " + str(i))
        listaEscritores.append(esc)

    # Esperar Lectores
    for l in listaLectores:
        l.join()

    # Crear Escritores
    for esc in listaEscritores:
        esc.join()

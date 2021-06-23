from multiprocessing import Process, Lock, Semaphore, Value
from time import sleep
from random import randint

candado = Lock()
db = Semaphore(1)

nLectores = Value("i", 0)


def leerBD():
    print("Lector Leyendo...\n")
    sleep(randint(5, 10))


def pensarQueLeer():
    print("Lector Pensando que Leer...\n")
    sleep(randint(3, 5))


def lector(can, bd, nLect):
    while True:
        pensarQueLeer()
        can.acquire()
        nLect.value += 1

        if nLect.value == 1:
            bd.acquire()

        can.release()

        leerBD()

        can.acquire()
        nLect.value -= 1

        if nLect.value == 0:
            bd.release()

        can.release()


##################
def pensarQueEscribir():
    print("Escritor Pensando que Escribir...\n")
    sleep(randint(3, 5))


def escribir():
    print("Escritor Escribiendo...\n")
    sleep(randint(20, 30))


def escritor(bd):
    while True:
        pensarQueEscribir()

        bd.acquire()
        escribir()
        bd.release()


###################################3
if __name__ == "__main__":
    # Crear Lectores
    listaLectores = []
    for i in range(0, 10):
        l = Process(target=lector, args=(candado, db, nLectores,))
        l.start()

        listaLectores.append(l)

    # Crear Escritores
    listaEscritores = []
    for i in range(0, 10):
        esc = Process(target=escritor, args=(db,))
        esc.start()

        listaEscritores.append(esc)

    # Esperar Lectores
    for l in listaLectores:
        l.join()

    # Crear Escritores
    for esc in listaEscritores:
        esc.join()

# -*- coding: cp1252 -*-
#Gustavo de Leon 17085
#Luis Esturban 17256
import math
import simpy
import random

RAND_SEED = 50
NEW_PROS = 25
INT_PROS = 3.0
#Tiempo dedicado a cada proseso
global TIE_PROS
TIE_PROS = 2
#Tiempo para las instrucciones de entrada y salida
global TIE_IO 
TIE_IO = 3
#Numero de instrucciones maximas
global INST_MAX 
INST_MAX = 10
#Cantidad de menoria maxima
global MEM_MAX 
MEM_MAX=10
#Tiempo total
global tieTot 
tieTot=0

#Funcion para la creacion y manejo de procesos
def proceso(env, nombre, CPU, memRAM, inOut, mem, inst):
    global TIE_PROS
    global TIE_IO
    global tieTot
    #Crea un nuevo proceso
    #Marca el momento de creacion
    creacion = env.now  
    print('%s se creo a las %s unidades de tiempo' % (nombre, creacion))
    with memRAM.get(mem) as req:
        yield req
        ready=env.now
        print('%s paso a ready en %s' % (nombre,ready))
        while(inst>0):
            with CPU.request() as req1:
                yield req1
                proc=env.now
                print ('empezando a procesar %s en %s' % (nombre, proc))
                yield env.timeout(TIE_PROS)
                proc=env.now
                print ('termino de procesar %s en %s' % (nombre, proc))

                if (inst-3)<0:
                    terminated=env.now
                    tiempoProceso=terminated-creacion
                    tieTot=tieTot +tiempoProceso
                    print('%s termino en %s' % (nombre, terminated))
                    memRAM.put(mem)
                    inst=0
                else:
                    inst=inst-3
                    if random.randint(0,1)== 0:
                        with inOut.request() as req2:
                            yield req2
                            print(' %s empezo proceso I/O en %s' % (nombre, env.now))
                            tib = random.randint(1, TIE_IO)
                            yield env.timeout(tib)
                            print(' %s termino proceso I/O en %s' % (nombre, env.now))
                            
#Funciona para darlo recursos a los procesos                       
def recursos(env, numero, inter, CPU, inpOut, memRAM):
    for i in range(numero):
        p= proceso(env, 'proceso %s' % i, CPU, memRAM, inOut, random.randint(1,MEM_MAX), random.randint(1,INST_MAX)) 
        env.process(p)
        t = random.expovariate(1.0 / inter)
        yield env.timeout(t)

random.seed(RAND_SEED)
env = simpy.Environment()

#Empieza el procesos y lo ejecuta
CPU = simpy.Resource(env, capacity=1)
inOut = simpy.Resource(env, capacity=1)
memRAM =simpy.Container(env, 10000, init=10000)
env.process(recursos(env, NEW_PROS, INT_PROS, CPU, inOut, memRAM))
env.run()

prom=tieTot/NEW_PROS

print('------------------------------------------------------')
print('------------------------------------------------------')
print('El PC demoro %s unidades de tiempo en terminar los procesos pendientes' % (tieTot))
print ('El promedio de tiempo por proceso es de: %s unidades de tiempo' % (prom))
print('------------------------------------------------------')

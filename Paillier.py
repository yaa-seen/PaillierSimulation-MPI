from phe import paillier
import libnum
import math
from mpi4py import MPI
import time
comm=MPI.COMM_WORLD
rank = comm.rank
size = comm.size
print(f"le processus est : {rank}")
debut=time.time()
def clientAdd(m1,m2,pub_key,priv_key):
    e1=pub_key.encrypt(m1)
    e2=pub_key.encrypt(m2)
    print(f"le temps pour chiffrer les deux messages est : {time.time() - debut}")
    #print(f"le temps pour chiffrer les deux messages est : {tps2 - tps1}")
    if rank ==0:
        comm.send(e1,dest=1)
        comm.send(e2,dest=1)
        print(f" je suis le processus {rank} j ai envoiyer e1 et e2 ")
    e=providerAdd(e1,e2)
    m=priv_key.decrypt(e)
    return m
debutLog=time.time()
def clientMulLog(m1,m2):
    l1=math.log(m1)
    l2=math.log(m2)
    e1=pub_key.encrypt(l1)
    e2=pub_key.encrypt(l2)
    if rank==0:
        comm.send(e1,dest=1)
        comm.send(e2,dest=1)
        print(f" je suis le processus {rank} j ai envoiyer e1 et e2 LOG")
    e=providerAdd(e1,e2)
    m=priv_key.decrypt(e)
    produit=math.exp(m)
    print(f"le temps pour appliquer le  LOG est : {time.time() - debutLog}")
    return produit

debutMullR=time.time()
def clientMulRusse(m1,m2,pub_key,priv_key):
    e2=pub_key.encrypt(m2)
    produit = pub_key.encrypt(0)
    if rank==0:
        comm.send(e2,dest=1)
        #comm.send(produit,dest=1)
        print(f" je suis le processus {rank} j ai envoiyer e1 et e2 MULRUSS")
    while m1>0:
        if m1%2==1:
            produit = providerAdd(produit,e2)
        m1=m1//2
        e2=e2*2
    m=priv_key.decrypt(produit)
    print(f"le temps pour appliquer la multiplication Russe est : {time.time() - debutMullR}")
    return m
def providerAdd(e1,e2):
    if rank ==1:
        comm.recv(source=0)
        comm.recv(source=0)
        print(f" je suis le processus {rank} j ai recu e1 et e2 ")
    return e1+e2
def afficherTest(test,m1,m2,m):
    print("\n",test)
    print("m1=",m1,"\t m2=",m2,"\tm=",m)
#1- générer la clé publique et clé privée
pub_key,priv_key=paillier.generate_paillier_keypair(n_length=1024)
#afficherParametres(pub_key,priv_key)
#2-choix des entrées
m1=430000
m2=226000
#3-tester l'homomorphe additif m1 et m2 crypté
#calculer le temps
m=clientAdd(m1,m2,pub_key,priv_key)
afficherTest("vérification de homorphisme additif",m1,m2,m)
#4-simulation par le logarithme
m=clientMulLog(m1,m2)
afficherTest("simulation par le logarithme",m1,m2,m)
#5-simulation par la multiplication russe
m=clientMulRusse(m1,m2,pub_key,priv_key)
afficherTest("simulation par la multiplication russe",m1,m2,m)

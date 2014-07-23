from PIL import Image
import numpy#potreban paket 'python-numpy'
from numpy import *

#biblioteka potrebna za prikaz slika
#import pylab


#metoda koja racuna euklidsku udaljenost dvaju tocaka
def euclidean(x,y):
	sumSq=0.0
	#add up the squared differences
	for i in range(len(x)):
		sumSq+=(x[i]-y[i])**2
 
	#take the square root of the result
	return (sumSq**0.5)


#metoda koja vraca indeks elementa i iz liste arr
def iMin(arr,i):
	return nonzero(arr==min(arr))[i]


def main():
	
	'''
	ucenje lica
	'''
	
	
	#kreiranje liste slika lica
	print 'ucenje lica je zapocelo, 40 osoba na 80 slika'
	print 'nakon 40 slika ponovo se nalazi 40 slika osoba u istom redosljedu (sto znaci da za odabranu sliku 1 tocan odgovor je 1 i 41)'
	imlist=[]
	imnbr=80
	for i in range(1,(imnbr+1)):
		imlist.append('bb/'+str(i)+'.png')
	
	im = numpy.array(Image.open(imlist[0])) #prva slika u 2D matricu
	m,n = im.shape[0:2] #dimenzije matrice


	#pohrana slika lica u vektore lica
	fv = numpy.array([numpy.array(Image.open(imlist[i])).flatten() for i in range(imnbr)],'f')#vektori lica iz slika lica, vektor dimenzija m*n
	fvm = numpy.array([numpy.array(Image.open(imlist[i])).flatten() for i in range(imnbr)],'f')#vektori lica iz slika lica, vektor dimenzija m*n


	meanf = fv.mean(axis=0)#zajednicko lice
	
	#oduzimanje zajednickog lica od svih lica
	for i in range(len(fvm)):
		fvm[i]-=meanf


	C=numpy.cov(fvm)#matrica kovarijacija


	e,EV = linalg.eigh(C)#racunanje eigen vrijednosti e i eigen vektora EV
	
	tmp = dot(fvm.T,EV).T#promjena dimenzije
	U = tmp[::-1]#sortiranje prostora
	S = sqrt(e)[::-1]#sortiranje eigen vrijednosti



	'''
	trazenje lica, sve osobe su naucene
	1. potrebno je odabrati broj prostora lica u koje ce se lica projecirati
	2. potrebno je unijeti broj od 1 do 40
	'''


	#koliko U vrijednosti koristit
	print 'Broj svojstvenih vektora mora biti manji od '+str(len(U)+1)
	rng=input('Broj svojstvenih vektora: ')
	while rng>len(U):
		print 'Broj svojstvenih vektora mora biti manji od '+str(len(U)+1)
		rng=input('Broj svojstvenih vektora: ')

	
	#projeciranje naucenih lica u prostore lica
	vls=[]
	for i in range(rng):
		tpp=[]
		for j in range(len(fvm)):
			tpp.append(U[i].T*fvm[j])#projekcija
		vls.append(tpp)


	#odabir osobe koju traziti
	tst=input('odaberite broj lica (1-40): ')
	while tst>40:
		tst=input('odaberite broj lica (1-40): ')

		
	nv=numpy.array(Image.open('aa/'+str(tst)+'.png')).flatten()#pohrana odabrane slike kao m*n vektor
	nvm=nv-meanf#oduzimanje zajednickog lica

	
	#projeciranje lica u prostore lica
	nvl=[]
	for i in range(rng):
		nvl.append(U[i].T*nvm)#projekcija

	
	#izracun euklidskih udaljenosti odabranog lica od naucenih lica
	ek=[]
	for i in range(rng):
		tpp=[]
		for j in range(len(vls[0])):
			tpp.append(euclidean(nvl[i],vls[i][j]))#euklidske udaljenosti 
		ek.append(tpp)
		
	reez=iMin(ek[0],0)+1#dohvat indeksa najmanje euklidske udaljenosti
	

	#korekcija rezultata (osobe se nakon 40 slika pocinju ponavljati istim redosljedom)
	mnn=True
	def rngCheck(a):
		if a>39:
			a-=40
		return a
		
	#provjera rezultata za odabrani broj prostora lica
	for i in range(1,rng):
		if rngCheck(iMin(ek[i],0))!=rngCheck(mnn):
			mnn=False
			break
	
	print 'za sliku osobe '+str(tst)+' probnadena je osoba pod brojem '+str(reez[0])
	if not mnn:
		print 'rezultat nije isti za sve odabrane svojstvene vektore'


	#prikaz slike odabrane i pronadene osobe, zahtjeva paket 'matplotlib'
	'''
	slika = nv.reshape(m,n)
	pylab.figure()
	pylab.gray()
	pylab.imshow(slika)

	slika = fv[iMin(ek[0],0)].reshape(m,n)
	pylab.figure()
	pylab.gray()
	pylab.imshow(slika)
	pylab.show()

	'''

if __name__ == "__main__":
	main()

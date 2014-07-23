#!/usr/bin/env python

# example images.py

import pygtk
pygtk.require('2.0')
import gtk
from PIL import Image
import numpy
from numpy import *
import time


def euclidean(x,y):
	sumSq=0.0
	for i in range(len(x)):
		sumSq+=(x[i]-y[i])**2
	return (sumSq**0.5)
imlist=[]
def iMin(arr,i):
	return nonzero(arr==min(arr))[i]

#korekcija rezultata (osobe se nakon 40 slika pocinju ponavljati istim redosljedom)
def rngCheck(a):
	if a>39:
		a-=40
	return a
def prepoznavanje(tst,rng):
	startTime=time.time()
	
	'''
	ucenje lica
	'''
	
	
	#kreiranje liste slika lica
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

	
	#projeciranje naucenih lica u prostore lica
	vls=[]
	for i in range(rng):
		tpp=[]
		for j in range(len(fvm)):
			tpp.append(U[i].T*fvm[j])#projekcija
		vls.append(tpp)

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
	
	mnn=iMin(ek[0],0)#dohvat indeksa najmanje euklidske udaljenosti
	
	if min(ek[0])>=(max(ek[0])/2):
		return -1,time.time()-startTime#osoba ne postoji u bazi
	else:
		#provjera rezultata za odabrani broj svojstvenih vektora
		for i in range(1,rng):
			if rngCheck(iMin(ek[i],0))!=rngCheck(mnn):
				mnn=False
				break
		if mnn!=False:
			return iMin(ek[0],0)+1,time.time()-startTime
		else:
			return 0,time.time()-startTime



class PCA:
		#metoda za zatvaranje aplikacije
        def close_application(self, widget, event, data=None):
                gtk.main_quit()
                return False
		#metoda za zatvaranje forme
        def close_window(self, widget, event, data=None):
                widget.hide()
		#dogadaj koji se pokrece na pritisak na neko od lica i pokrece proces trazenja
        def button_clicked(self, widget, data=None):
			
				#prikaz forme za rezultat
                window = gtk.Window(gtk.WINDOW_TOPLEVEL)
                window.connect("delete_event", self.close_window)
                window.set_border_width(10)
                window.show()
                hbox = gtk.HBox()
                hbox.show()
                window.add(hbox)
                
                #dohvat rezltata za trazeno lice data
                rzz,tme=prepoznavanje(data,int(self.entry.get_text()))
                
                #dodavanje odabranog lica na formu
                pixbufanim = gtk.gdk.PixbufAnimation("aa/"+str(data)+".png")
                image = gtk.Image()
                image.set_from_animation(pixbufanim)
                image.show()
                button = gtk.Button()
                button.add(image)
                button.show()
                hbox.pack_start(button)
                
                #ako je pronadeno lice 
                if rzz>0:
						#prikaz pronadenog lica
                        rzz=rzz[0]
                        pixbufanim = gtk.gdk.PixbufAnimation("bb/"+str(rzz)+".png")
                        image = gtk.Image()
                        image.set_from_animation(pixbufanim)
                        image.show()
                        button = gtk.Button()
                        button.add(image)
                        button.show()
                        hbox.pack_start(button)
                        label = gtk.Label("Potrebno vrijeme:\n"+str("{0:.2f}".format(tme))+"s")
                        hbox.pack_start(label)
                        label.show()
                #ako nije pronadeno
                else:
					if rzz==0:
						label = gtk.Label("Osoba nije pronadena!\n\n\nPotrebno vrijeme:\n"+str(tme)+"s")
					else:
						label = gtk.Label("Osoba ne postoji u bazi!\n\n\nPotrebno vrijeme:\n"+str(tme)+"s")
					hbox.pack_start(label)
					label.show()
        def __init__(self):
				#prikaz glavne forme
                window = gtk.Window(gtk.WINDOW_TOPLEVEL)
                window.connect("delete_event", self.close_application)
                window.set_border_width(10)
                window.show()

                tarRng=[10,5]
                table = gtk.Table(tarRng[0], tarRng[1], True)
                table.set_row_spacings(1)
                for i in range(5):
                        table.set_row_spacing(i,20)
                window.add(table)

                label = gtk.Label("Preopoznavanje lica PCA metodom\n\nOdaberite sliku lica osobe koju zelite pronaci")
                table.attach(label, 0,3, 0, 1)
                label.show()

                label = gtk.Label("Broj svojstvenih vektora: ")
                table.attach(label, 4,6, 0, 1)
                label.show()

                self.entry= gtk.Entry(2)
                self.entry.set_text("1")
                table.attach(self.entry, 6,8, 0, 1)
                self.entry.show()

                uk=1
                #dodavanje tipki s slikama lica
                for j in range(1,tarRng[1]):
                        for i in range(tarRng[0]):
                                pixbufanim = gtk.gdk.PixbufAnimation("aa/"+str(uk)+".png")
                                image = gtk.Image()
                                image.set_from_animation(pixbufanim)
                                image.show()
                                button = gtk.Button()
                                button.add(image)
                                button.show()
                                button.set_alignment(0,0)
                                table.attach(button, i,i+1, j, j+1)
                                button.connect("clicked", self.button_clicked, str(uk))
                                uk+=1
                table.show()
def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    PCA()
    main()

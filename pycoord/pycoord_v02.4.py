#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__  = "Édoaurd Lopez"
__version__ = "v2.4"
__date__    = "2008-28-05"
# contact: edouard.lopez+ter@gmail.com
#########################################################
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#########################################################

import os, sys, math, copy # modules natifs
import Pmw # modules tiers nécessaire au fonctionnement
from stat import *
import  tkMessageBox, tkSimpleDialog
from Tkinter import *
try:# pour utiliser au moins une fois les exceptions (par vraiment pertinent... enfin je crois)
	from PIL import Image, ImageTk, ImageDraw
	# ImageTk => installation de python-imaging python-imaging-tk
except ImportError:
	import Image, ImageTk, ImageDraw


class Application(): # héritage de la classe 'Frame' de Tkinter
	os.chdir(os.path.dirname(sys.argv[0])) # on se place dans le dossier du fichier -> adresse relative

	def __init__(self):
		"""Instanciation de la classe"""
		self.dossier_input_image =  os.path.join(os.getcwd(), 'base')
		self.dossier_output_image =  os.path.join(os.getcwd(), 'baseout')
		self.i=0
		#self.dico_fichier = {}
		self.list_fichier = [] # liste temporaire des images trouvées, on utilise un type liste pour pouvoir faire un tri alphabétique
		self.all_coord_pts = {} # auto-incrémente + si aucun index ça le cré
		self.photo_pts = {'image':self.list_fichier, 'pts':self.all_coord_pts} # mis à jour dynamiquement par python -> variable pseudo-fictiv (dépend de list_fichier et coord_pts)
		self.photo = ['', ''] # contient la photo d'origine (en 0), la photo zoomer (en 1)
		self.zoomf = 1 # facteur de zoom
		self.x, self.y = 0, 0
		self.bord = 1 # bordure des points
		self.root={'fenetre': Tk()} # on crée un tableau dynamique; la 1re valeur est la fenetre Tkinter
		self.nb_img = self.file_lister()-1 # nb d'images valides trouvées dans le dossier
		self.createGUI()
		#print self.root['fenetre'].winfo_width(), self.root['fenetre'].winfo_height()
		self.precedente = self.i
		self.suivante = self.i+1
		self.cb_suivante(self.i) # affiche la première image.

		self.root['fenetre'].resizable(1, 1) # redimensionnable horizontalement et verticalement
		self.root['fenetre'].protocol("WM_DELETE_WINDOW", self.close)

		self.root['fenetre'].mainloop() # en attente d'événement souris/clavier
	#

	def dic2scilab(self):
		"""Convertion de notre dictionnaire image-points en matrice pour scilab."""
		scilab = ''
		for pts in self.all_coord_pts.values():# retourne les valeurs de chaque entrée du dictionnaire
			if len(pts)==4:
				scilab += '%i %i %i %i %i %i %i %i;\n' % (pts[0][0], pts[0][1], pts[1][0], pts[1][1], pts[2][0], pts[2][1], pts[3][0], pts[3][1])
			else:
				pass
		return scilab
	#

	def close(self):
		"""Écriture de la matrice des points dans un fichier avant la fermeture de l'application."""
		self.dossier_output_image
		outfile = open('points.sce','a') # ouvre en mode ajout en fin de fichier : a = append()
		outfile.write(self.dic2scilab())
		outfile.close()
		self.root['fenetre'].quit
		self.root['fenetre'].destroy()
	#

	#_____________________________________
	#						| |	Nom			 	| [			]		|
	#						|^| Dimension | [			]		|
	#		image		|v|	[Zoomx2]	|	[Zoomx2]	|
	#						| |	[Zoom :]	|	[1	]			|
	#<=========>													|
	#	statusbar___________________________|
	def createGUI(self): # Graphic User Interface
		"""Création de l'interface"""
	# titre
		self.root['fenetre'].title("Pycoordon'")
		self.root['fenetre'].config(width=600, height=400)
		#self.root['fenetre'].maxsize(1024, 800)
	# Cadre du canevas (canevas, scrollbar verticale et horizontale)
		self.root['Fcanevas'] = Frame(self.root['fenetre']) # on crée la partie de gauche = le canevas
		self.root['Fcanevas'].pack(side=RIGHT, expand=YES, fill=BOTH) # pack le Fcanevas sur la partie gauche de la fenetre
		#self.root['Fcanevas2'] = Frame(self.root['Fcanevas']) # on crée la partie de gauche = le canevas
		#self.root['Fcanevas2'].pack(side=TOP, expand=YES, fill=BOTH) # pack le Fcanevas sur la partie gauche de la fenetre
	# <canevas>
		#self.root['canevas'] = Canvas(self.root['Fcanevas'], bg = 'gray', width=600, height=400)
	# Status Bar
		self.root['Fstatusbar'] = Frame(self.root['Fcanevas'], bd=1, relief=SUNKEN)
		self.root['SBcoord'] = Label(self.root['Fstatusbar'], text=" coordonnées : ?, ?")
		self.root['SBzoom'] = Label(self.root['Fstatusbar'], text=" zoom : 100%")
		self.root['SBcoord'].pack(side=LEFT, anchor=W)
		self.root['SBzoom'].pack(side=RIGHT, anchor=E)
		self.root['Fstatusbar'].pack(side=BOTTOM, fill=X) # pack, construit l'objet root['statusbar'] et l'affiche
	# Scrollbars
		# appartient à 'Fcanevas', fait bouger horizontalement/verticalement 'canevas'
		self.root['canevas'] = Pmw.ScrolledCanvas(self.root['Fcanevas'], usehullsize =1, hull_width =400, hull_height =300, canvas_bg ='grey40', canvasmargin=0, borderframe=1, borderframe_borderwidth=0)#, labelpos=N, label_text ='Attrapez le bouton !', )
		self.root['canevas'].configure(vscrollmode ='dynamic', hscrollmode='dynamic')
		self.root['canevas'].pack(side=TOP, expand=YES, fill=BOTH)
		# crée un lien entre l'événement 'clic gauche' et la fonction de récupération de coordonnées sur 'canevas'
		#self.root['canevas'].component('canvas').bind("<Button-1>", self.cb_onclick_get_coord)
		self.root['canevas'].component('canvas').bind("<Button-1>", self.cb_onclick_get_coord)

	# Cadre des boutons/labels (nom, dimensions, zooms, etc.)
		self.root['Fpanel'] = Frame(self.root['fenetre'])
	# partie haute = info
		self.root['Fpanel_info'] = Frame(self.root['Fpanel'], relief=RIDGE, bd=2)
	# Nom image
		self.root['Fnom'] = Frame(self.root['Fpanel_info'])
		self.root['Lnom'] = Label(self.root['Fnom'], text='Nom :', bd=1) # définition du Label
		self.root['Lnom'].pack(side=LEFT)
		self.root['Enom'] = Entry(self.root['Fnom'], bg = 'white', bd=1) # edit pour sélectionner le nom du fichier affiché
		self.root['Enom'].insert(0, '?') # valeur par défaut
		self.root['Enom'].pack(side=RIGHT)
		self.root['Fnom'].pack(fill=X, padx=5, pady=5)
	# Dimension image
		self.root['Fsize'] = Frame(self.root['Fpanel_info'])
		self.root['Lsize'] = Label(self.root['Fsize'], text='Dimension : ', bd=1)
		self.root['Lsize'].pack(side=LEFT)
		self.root['Esize'] = Entry(self.root['Fsize'], bg = 'white', bd=1)
		self.root['Esize'].insert(0, '?x?')
		self.root['Esize'].pack(side=RIGHT)
		self.root['Fsize'].pack(fill=X, padx=5)

	# labels de coordonnées
		self.root['Fpts'] = Frame(self.root['Fpanel_info'])
		self.root['Lpts'] = Label(self.root['Fpts'], text='Coordonnées des points :', bd=1, anchor=W) # définition du Label
		self.root['Lpts'].pack(side=TOP, fill=X)
		self.root['Epts'] = Entry(self.root['Fpts'], bg = 'white', bd=1) # edit pour sélectionner le nom du fichier affiché
		self.root['Epts'].insert(0, '') # valeur par défaut
		self.root['Epts'].pack(side=BOTTOM, fill=X)
		self.root['Fpts'].pack(fill=X, padx=5, pady=5)
	# partie haute = info
		self.root['Fpanel_info'].pack(side=BOTTOM, fill=X, pady=5)#pack(side=TOP, ipadx=5, pady=10)

	# partie basse = manip
		self.root['Fpanel_manip'] = Frame(self.root['Fpanel'], relief=RIDGE, bd=2)
	# Zoom in/out
		self.root['Fzoom'] = Frame(self.root['Fpanel_manip'])
	# Zoom avant
		self.zoomin = ImageTk.PhotoImage(Image.open('zoom_in.png'))
		self.root['Bzoomin'] = Button(self.root['Fzoom'], image=self.zoomin, command=lambda:self.cb_zoom(2,True), bd=1) # zoom avant x2 par défaut
		self.root['Bzoomin'].pack(side=RIGHT, padx=5)
	# Zoom arrière
		self.zoomout = ImageTk.PhotoImage(Image.open('zoom_out.png'))
		self.root['Bzoomout'] = Button(self.root['Fzoom'], image=self.zoomout, command=lambda:self.cb_zoom(0.5, True), bd=1) # zoom arrière x1/2
		self.root['Bzoomout'].pack(side=RIGHT, padx=5)
	# Zoom perso
	# Menu
		self.zoomf = 1
		self.root['Mbzoom'] = Menubutton(self.root['Fzoom'], text='Autres zooms', relief=RAISED, bd=1)
		self.root['Mbzoom'].pack(fill=X)
		# partie déroulante du menu
		zval=[0.5, 1, 1.5, 2, 4, 8]
		self.root['Mzoom_options'] = Menu(self.root['Mbzoom']) # création du menu
		self.root['Mzoom_options'].add_radiobutton(label=str(int(zval[0]*100))+'%', variable=self.zoomf, value=0, command=lambda:self.cb_zoom(zval[0], 0))
		self.root['Mzoom_options'].add_radiobutton(label=str(int(zval[1]*100))+'%', variable=self.zoomf, value=1, command=lambda:self.cb_zoom(zval[1], 0))
		self.root['Mzoom_options'].add_radiobutton(label=str(int(zval[2]*100))+'%', variable=self.zoomf, value=2, command=lambda:self.cb_zoom(zval[2], 0))
		self.root['Mzoom_options'].add_radiobutton(label=str(int(zval[3]*100))+'%', variable=self.zoomf, value=3, command=lambda:self.cb_zoom(zval[3], 0))
		self.root['Mzoom_options'].add_radiobutton(label=str(int(zval[4]*100))+'%', variable=self.zoomf, value=4, command=lambda:self.cb_zoom(zval[4], 0))
		#self.root['Mzoom_options'].add_radiobutton(label=str(int(zval[5]*100))+'%', variable=self.zoomf, value=5, command=lambda:self.cb_zoom(zval[5], 0))

	# Intégration du menu :
		self.root['Mbzoom'].configure(menu = self.root['Mzoom_options'])
		self.root['Mbzoom'].pack(fill=X, padx=5)
		self.root['Fzoom'].pack(fill=X, pady=5)

	# bouton de validation/passage à l'image suivante
		self.root['FNavimg'] = Frame(self.root['Fpanel_manip'])
		self.root['Bprecedent'] = Button(self.root['FNavimg'], text="Précédente", bd=1, command=lambda:self.cb_suivante(self.precedente))
		self.root['Bprecedent'].pack(fill=X, expand=YES, side=LEFT)
		self.root['Bsuivant'] = Button(self.root['FNavimg'], text="Suivante", bd=1, command=lambda:self.cb_suivante(self.suivante))
		self.root['Bsuivant'].pack(fill=X, expand=YES, side=RIGHT)
		self.root['FNavimg'].pack(side=BOTTOM, fill=X, padx=5, ipady=5)
	# partie basse = manip
		self.root['Fpanel_manip'].pack(side=TOP, fill=X)

	# on pack le frame de droite
		self.root['Fpanel'].pack(side=TOP, pady=10, padx=5, ipadx=5, ipady=5, expand=NO)
	# Fin de la fenetre



	def cb_suivante(self, pos):
		"""Passe à l'image n° pos de la liste."""
		print 'tableau des coordonnées : ', self.all_coord_pts#, self.dic2scilab()
		if pos==0 or pos==self.nb_img:
			pass# si on est sur la 1re ou dernière image de la liste on ne change pas les paramètres
		else:
			self.precedente = pos-1
			self.suivante = pos+1
			self.all_coord_pts[self.i] = self.coord_pts
		self.i=pos # met à jour la position actuelle
		self.update_img()
	#

	def update_img(self):
		"""Met à jour le canevas."""
		self.update_label('Enom', self.list_fichier[self.i])
		self.image_loader() # affiche l'image 'self.i' de la liste
		print 'image n°: %i' % self.i
	#

	def fin(self):
		"""callback for the "INFO" button"""
		tkMessageBox.showinfo("INFO", message="Fin de la liste d'images.")
	#

	def cb_onclick_get_coord(self, event):
		"""Affiche les coordonnées du curseur sur le canevas."""
		evx, evy = self.root['canevas'].canvasx(event.x), self.root['canevas'].canvasy(event.y)
		if evx>self.photo[1].size[0] or evy>self.photo[1].size[1]: # click a coté de l'image
			pass
		else:
			self.x, self.y = int(round(evx/self.zoomf)), int(round(evy/self.zoomf))
			print "zoom x%i, (%i, %i)" % (self.zoomf, self.x, self.y)
			# bon cacul ? il est tard...
			self.add_point_coord() # ajoute les coordonnées du point dans la liste
			self.statusbar_update_coord()
			self.root['SBcoord'].config(text=" coordonnées : %ix%i" % (self.x, self.y))
			# ????????????????????????????
	#

	def add_point_coord(self):
		"""Tant qu'on a pas les coordonnées des tous les points, on continue de les rajoutez à la lite."""
		if len(self.coord_pts)<4:
			self.coord_pts.append((self.x, self.y))
			self.root['Epts'].insert(END, '%i,%i; ' % (self.x, self.y)) # valeur par défaut
			self.gribouille()
		else:
			tkMessageBox.showwarning("Redondance","Tous les points ont déjà été saisi."			)
			print self.coord_pts
	#

	def statusbar_update_coord(self):
		"""Mise à jour des coordonnées du curseur sur le canevas."""
		self.root['SBcoord'].config(text=" coordonnées : %ix%i" % (self.x, self.y))
		self.root['SBzoom'].config(text=" zoom : %i%%" % (self.zoomf*100) )
	#

	def gribouille(self):
		"""dessine un rectangle au coordonnées des points."""
		width = int(math.ceil(self.bord*self.zoomf)) # 'épaisseur' autour du point central
		for coord in self.coord_pts:
			#x1, y1, x2, y2 = int(round(coord[0]*self.zoomf-width)), int(round(coord[1]*self.zoomf-width)), int(round(coord[0]*self.zoomf+width)), int(round(coord[1]*self.zoomf+width))
			self.x, self.y = coord[0], coord[1]
			print 'x, y : %d, %d x%2.2f' % (self.x, self.y, self.zoomf)
			x1, y1, x2, y2 = self.x*self.zoomf-width, self.y*self.zoomf-width, self.x*self.zoomf+width, self.y*self.zoomf+width
			print 'rectangle :',(x1, y1, x2, y2 )
			self.gribouillage.rectangle([(x1, y1), (x2, y2)], fill=255)#, color='red')
			self.invoque_img() # = rafraichissement du contenu du canvas
		save_file = os.path.join(self.dossier_output_image, 'dot-%04d__%s.png' % (self.i, self.list_fichier[self.i]))
		self.photo[1].save(save_file, "PNG")
	#

	def update_label(self, label, val):
		"""Met à jour un Label"""
		self.root[label].delete(0, END)
		self.root[label].insert(0, val)
	#

	def file_lister(self, extension=['.jpg', '.jpeg', '.gif']):
		"""List les fichiers de type 'extension' du dossiers"""
		print 'dossier des images : %s' % self.dossier_input_image
		print "\n==================================\nfichiers IMAGES %s trouvés: " % extension
		for fichier in os.listdir(self.dossier_input_image):
			chemin = os.path.join(self.dossier_input_image, fichier) # crée le chemin absolu/complet
			for ext in extension:
				if os.path.splitext(fichier)[1]==ext:
					mode = os.stat(chemin)[ST_MODE] # récupère le 'mode' du fichier (dossier, fichier, lien, etc.) parmi le tableau de résultat de 'stat()'
					if S_ISREG(mode):#fichier normal
						self.list_fichier.append(fichier)
					print '\t'+fichier+" est de type: %s" % (ext)
		self.list_fichier.sort() # tri alphabétique
		return len(self.list_fichier)
	#

	def cb_zoom(self, factor=2, zoom_abs=False):
		"""Effectue un zoom de facteur défini (défaut=2)."""
		if zoom_abs==True:# distinction zoom relatif vs. absolu (dans le menu)
			self.zoomf = self.zoomf*factor
		else:
			self.zoomf = factor

		if self.zoomf>4 or self.zoomf<0.25:
			print 'zoom trop grand %i' % self.zoomf
			pass
		else:
			self.statusbar_update_coord()
			nw, nh = int(round(self.photo[0].size[0]*self.zoomf)), int(round(self.photo[0].size[1]*self.zoomf)) # calcul les nouvelles dimensions à partir de l'image d'origine
			print "zoom x%s -> taille = %dx%d" % (self.zoomf, nw, nh)
			self.photo[1] = self.photo[0].resize((nw, nh), 1) # créée une image de redimensionner
			self.root['canevas'].configure(hull_width=self.photo[1].size[0]%1024, hull_height=self.photo[1].size[1]%800)
			self.root['canevas'].resizescrollregion()

			print 'image zoomée : %ix%i' % (self.photo[1].size[0], self.photo[1].size[1])
			#self.zoomf = factor # pour les coordonnées lorsque l'image est zoomée
			self.gribouillage = ImageDraw.Draw(self.photo[1]) # crée un objet de dessin
			self.gribouille()
			self.invoque_img()
	#

	def invoque_img(self):
		"""Charge l'image dans le canevas."""
		self.photo_cnv = ImageTk.PhotoImage(self.photo[1]) # charge l'image ## ne pas écraser l'objet 'img' ! ##
		self.item = self.root['canevas'].create_image(0, 0, image=self.photo_cnv, anchor=NW)
	#

	def env_image_load(self):
		"""Redéfinit l'environnement (label, entry, tableau de point) pour une nouvelle image."""
		self.update_label('Enom', self.list_fichier[self.i])
		self.root['Epts'].delete(0, END)
		self.coord_pts = [] # contient les coordonnées des 4 points
		self.all_coord_pts[self.i] = self.coord_pts
		self.zoomf = 1 # facteur de zoom
		self.cb_zoom(1, True)
		self.root['canevas'].configure(hull_width=self.photo[1].size[0]%1024, hull_height=self.photo[1].size[1]%800)
		#self.root['fenetre'].geometry("%dx%d+%d+%d" % (self.photo[1].size[0]%1024+300, self.photo[1].size[1]%800, 0, 0)) # "wxh±x±y" = dimensions de la fenetre

	#

	def image_loader(self):
		"""Charge une nouvelle image dans l'interface"""
		fichier = os.path.join(self.dossier_input_image, self.list_fichier[self.i])
		self.photo[0] = Image.open(fichier).convert("RGB") # open() retourne un objet de type 'image'; convert() force une image couleur; on utilise PIL car PhotoImage ne supporte pas le jpg
		self.photo[1] = self.photo[0] # l'image zoomer est l'image originale au début
		self.env_image_load() # définie les variable d'environnement pour chaque image

		# verbose
		print "dimensions de %s: x=%d y=%d" % (self.list_fichier[self.i][0], self.photo[0].size[0], self.photo[0].size[1])
		# paramètres d'environnement
		self.update_label('Esize', str(self.photo[0].size[0])+"x"+str(self.photo[0].size[1]))
		self.invoque_img()

	#

if __name__ == "__main__":
	app = Application() # création de l'appli

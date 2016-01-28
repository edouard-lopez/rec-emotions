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

import os, sys, math, copy, operator # modules natifs
import Pmw # modules tiers nécessaire au fonctionnement
from stat import *
import  tkMessageBox, tkSimpleDialog
from Tkinter import *
try:# pour utiliser au moins une fois les exceptions (par vraiment pertinent... enfin je crois)
	from PIL import Image, ImageTk, ImageDraw, ImageStat, ImageOps
	# ImageTk => installation de python-imaging python-imaging-tk
except ImportError:
	import Image, ImageTk, ImageDraw


class Application(): # héritage de la classe 'Frame' de Tkinter
	os.chdir(os.path.dirname(sys.argv[0])) # on se place dans le dossier du fichier -> adresse relative

	def __init__(self):
		"""Instanciation de la classe"""
		self.dossier_input_image =  os.path.join(os.getcwd(), 'mouth')
		self.dossier_output_image =  os.path.join(os.getcwd(), 'mouth')
		self.i=0
		#self.dico_fichier = {}
		self.list_fichier = [] # liste temporaire des images trouvées, on utilise un type liste pour pouvoir faire un tri alphabétique
		self.all_coord_pts = {} # auto-incrémente + si aucun index ça le cré
		self.photo_pts = {'image':self.list_fichier, 'pts':self.all_coord_pts} # mis à jour dynamiquement par python -> variable pseudo-fictiv (dépend de list_fichier et coord_pts)
		self.photo = ['', ''] # contient la photo d'origine (en 0), la photo zoomer (en 1)
		self.zoomf = 1 # facteur de zoom
		self.bord = 1 # bordure des points
		self.root={'fenetre': Tk()} # on crée un tableau dynamique; la 1re valeur est la fenetre Tkinter
		self.nb_img = self.file_lister()-1 # nb d'images valides trouvées dans le dossier
		self.createGUI()
		#print self.root['fenetre'].winfo_width(), self.root['fenetre'].winfo_height()
		self.precedente = self.i
		self.suivante = self.i+1
		self.cb_suivante(self.i) # affiche la première image.
		#self.detect_mouth()

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
		self.root['fenetre'].title("pyMouth Detector")
		self.root['fenetre'].config(width=600, height=400)
		#self.root['fenetre'].maxsize(1024, 800)
	# Cadre du canevas (canevas, scrollbar verticale et horizontale)
		self.root['Fcanevas'] = Frame(self.root['fenetre']) # on crée la partie de gauche = le canevas
		self.root['Fcanevasin'] = Frame(self.root['Fcanevas'], bd=2) # on crée la partie de gauche = le canevas
		self.root['Fcanevasin'].pack(side=TOP, expand=YES, fill=BOTH) # pack le Fcanevas sur la partie gauche de la fenetre

		self.root['Fcanevasout'] = Frame(self.root['Fcanevas'], bd=2) # on crée la partie de gauche = le canevas
		self.root['Fcanevasout'].pack(side=BOTTOM, expand=YES, fill=BOTH) # pack le Fcanevas sur la partie gauche de la fenetre
		self.root['Fcanevas'].pack(side=RIGHT, expand=YES, fill=BOTH, ipadx=10)

	# Scrollbars
		# appartient à 'Fcanevasin', fait bouger horizontalement/verticalement 'canevasin'
		self.root['canevasin'] = Pmw.ScrolledCanvas(self.root['Fcanevasin'], usehullsize =1, hull_width =400, hull_height =300, canvas_bg ='grey40', canvasmargin=0, borderframe=1, borderframe_borderwidth=0)#, labelpos=N, label_text ='Attrapez le bouton !', )
		self.root['canevasin'].configure(vscrollmode ='dynamic', hscrollmode='dynamic')
		self.root['canevasin'].pack(side=TOP, expand=YES, fill=BOTH)
		self.root['canevasout'] = Pmw.ScrolledCanvas(self.root['Fcanevasout'], usehullsize =1, hull_width =400, hull_height =300, canvas_bg ='grey40', canvasmargin=0, borderframe=1, borderframe_borderwidth=0)#, labelpos=N, label_text ='Attrapez le bouton !', )
		self.root['canevasout'].configure(vscrollmode ='dynamic', hscrollmode='dynamic')
		self.root['canevasout'].pack(side=TOP, expand=YES, fill=BOTH)
		# crée un lien entre l'événement 'clic gauche' et la fonction de récupération de coordonnées sur 'canevasin'
		#self.root['canevasin'].component('canvas').bind("<Button-1>", self.cb_onclick_get_coord)
		#self.root['canevasin'].component('canvas').bind("<Button-1>", self.cb_onclick_get_coord)

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

	# partie haute = info
		self.root['Fpanel_info'].pack(side=TOP, fill=X, pady=5)#pack(side=TOP, ipadx=5, pady=10)

	# partie centrale = manip
		self.root['Fpanel_manip'] = Frame(self.root['Fpanel'], relief=RIDGE, bd=2)
		self.root['FNavimg'] = Frame(self.root['Fpanel_manip'])
		self.root['Lnav'] = Label(self.root['FNavimg'], text='Navigation : ', bd=1)
		self.root['Lnav'].pack(side=LEFT)
		self.root['Bprecedent'] = Button(self.root['FNavimg'], text="Précédente", bd=1, command=lambda:self.cb_suivante(self.precedente))
		self.root['Bprecedent'].pack(side=LEFT, fill=X, expand=YES)
		self.root['Bsuivant'] = Button(self.root['FNavimg'], text="Suivante", bd=1, command=lambda:self.cb_suivante(self.suivante))
		self.root['Bsuivant'].pack(side=RIGHT, fill=X, expand=YES)
		self.root['FNavimg'].pack(side=BOTTOM, fill=X, padx=5, ipady=5)
		self.root['Fpanel_manip'].pack(side=TOP, fill=X, pady=5)

	## partie centrale =  détection
		self.root['Fpanel_detection'] = Frame(self.root['Fpanel'], relief=RIDGE, bd=2)
		# Méthode de détection
		self.root['FDetection'] = Frame(self.root['Fpanel_detection'])
		self.root['Ldetection_methode'] = Label(self.root['FDetection'], text='Méthode de détection : ', bd=1)
		self.root['Ldetection_methode'].pack(side=LEFT)
		self.root['BmethodeRGB'] = Button(self.root['FDetection'], text='RGB', bd=1, command=lambda:self.detect_mouth('rgb'))
		self.root['BmethodeRGB'].pack(side=LEFT, fill=X, expand=YES)
		self.root['BmethodeHSV'] = Button(self.root['FDetection'], text='HSV', bd=1, command=lambda:self.detect_mouth('hsv'))
		self.root['BmethodeHSV'].pack(side=RIGHT, fill=X, expand=YES)
		self.root['FDetection'].pack(side=BOTTOM, fill=X, padx=5, ipady=5)
		# Méthode de détection
		self.root['Fblock'] = Frame(self.root['Fpanel_detection'])
		self.root['Lblok'] = Label(self.root['Fblock'], text='Taille des blocs : ', bd=1)
		self.root['Lblok'].pack(side=LEFT)
		self.root['ScBlock'] = Scale(self.root['Fblock'], orient=HORIZONTAL, from_=8, to=128, length=150)
		self.root['ScBlock'].pack(side=RIGHT, pady =5, padx =20)
		self.root['ScBlock'].set(12)
		self.root['Fblock'].pack(side=BOTTOM, fill=X, padx=5, ipady=5)

		self.root['Fpanel_detection'].pack(side=TOP, fill=X, pady=5)

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
			#self.statusbar_update_coord()
			nw, nh = int(round(self.photo[0].size[0]*self.zoomf)), int(round(self.photo[0].size[1]*self.zoomf)) # calcul les nouvelles dimensions à partir de l'image d'origine
			print "zoom x%s -> taille = %dx%d" % (self.zoomf, nw, nh)
			self.photo[0] = self.photo[0].resize((nw, nh), 1) # créée une image de redimensionner
			self.root['canevasin'].configure(hull_width=self.photo[0].size[0]%1024, hull_height=self.photo[0].size[1]%800)
			self.root['canevasin'].resizescrollregion()
			self.photo[1] = self.photo[1].resize((nw, nh), 1) # créée une image de redimensionner
			self.root['canevasout'].configure(hull_width=self.photo[1].size[0]%1024, hull_height=self.photo[1].size[1]%800)
			self.root['canevasout'].resizescrollregion()

			print 'image zoomée : %ix%i' % (self.photo[1].size[0], self.photo[1].size[1])
			#self.zoomf = factor # pour les coordonnées lorsque l'image est zoomée
			#self.gribouillage = ImageDraw.Draw(self.photo[1]) # crée un objet de dessin
			#self.gribouille()
			self.invoque_img()
	#

	def invoque_img(self):
		"""Charge l'image dans le canevas."""
		self.photo_cnv_in = ImageTk.PhotoImage(self.photo[0]) # charge l'image ## ne pas écraser l'objet 'img' ! ##
		self.item = self.root['canevasin'].create_image(0, 0, image=self.photo_cnv_in, anchor=NW)
		#posterize = ImageOps.posterize(self.photo_cnv_in, 1)
		#self.item = self.root['canevasin'].create_image(0, 0, image=posterize, anchor=NW)
		self.photo_cnv_out = ImageTk.PhotoImage(self.photo[1]) # charge l'image ## ne pas écraser l'objet 'img' ! ##
		self.item = self.root['canevasout'].create_image(0, 0, image=self.photo_cnv_out, anchor=NW)
	#

	def env_image_load(self):
		"""Redéfinit l'environnement (label, entry, tableau de point) pour une nouvelle image."""
		self.update_label('Enom', self.list_fichier[self.i])
		#self.root['Epts'].delete(0, END)
		self.coord_pts = [] # contient les coordonnées des 4 points
		self.all_coord_pts[self.i] = self.coord_pts
		self.zoomf = 1 # facteur de zoom
		self.cb_zoom(.5, True)
		self.root['canevasin'].configure(hull_width=self.photo[0].size[0]%1024, hull_height=self.photo[0].size[1]%800)
		self.root['canevasout'].configure(hull_width=self.photo[1].size[0]%1024, hull_height=self.photo[1].size[1]%800)
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

	def detect_mouth(self, methode):
		""""""
		self.methode = methode
		self.get_img_nfo()
	#

	def get_img_nfo(self):
		"""Récupère des informations sur l'image :
			* dimensions (n, m),
			* la somme et la moyenne de la composante rouge de tous les pixels,
			* le nombre de pixel."""
		self.N = self.photo[0].size[0]
		self.M = self.photo[0].size[1]
		stat = ImageStat.Stat(self.photo[0])
		self.sum = map(int, stat.sum) # somme de chaque composante de tous les pixels
		#self.mean = stat.mean # moyenne de chaque composante de tous les pixels
		self.mean = map(int, stat.mean) # moyenne de chaque composante de tous les pixels
		self.pixcount = stat.count[0] # nombre de pixels de l'image
		print self.pixcount, self.sum, self.mean
		print 'Nb Pixels : %i # Pixel Moyen : (%i,%i,%i) # Somme Pixels : (%i,%i,%i)' % (self.pixcount, int(self.mean[0]),int(self.mean[1]),int(self.mean[2]), int(self.sum[0]),int(self.sum[1]),int(self.sum[2]))
		self.grille8()
	#

	def grille8(self):
		"""On pixélise l'image (-> matrice self.nblockxself.nblock)."""
		pix = self.photo[0].load() # charge l'image dans une matrice
		self.nblock = self.root['ScBlock'].get() # taille des sous-blocs = position du curseur
		#self.sub_mean = [[(0,0,0)]*self.nblock]*self.nblock # /!\ toutes les cases font références au même objet !!!
		self.sub_mean = [] # crée la matrice représentatnt les sous-blocs
		self.block_size = [int(self.N/self.nblock), int(self.M/self.nblock)] # dimensions des sous-blocs

		# On découpe des carrés/blocks de dimensions 'self.block_size' dans l'image d'origine desquels ont va extraire la valeur moyenne
		for i in range(self.nblock): # parcours les zones horizontalement
			self.sub_mean.append([]) # ajoute la ligne
			for j in range(self.nblock): # parcours les zones verticalement
				box = (i*self.block_size[0], j*self.block_size[1], (i+1)*self.block_size[0], (j+1)*self.block_size[1]) # définie le block courant
				ss_block = self.photo[0].crop(box) # découpe le block -> permet traitement d'image (Image.Stat)
				stat_ss_block = ImageStat.Stat(ss_block) # statistiques sur le bloc
				ss_block_mean = [int(s) for s in stat_ss_block.mean] # moyen (liste d'entier)
				self.sub_mean[i].append(ss_block_mean) # ajoute la case à cette ligne
				print 'Sous-bloc: (%i, %i) # Coordonnées: (%i, %i, %i, %i) # Pixel Moyen: (%i, %i, %i)' % (i, j, box[0], box[1], box[2], box[3], ss_block_mean[0], ss_block_mean[1], ss_block_mean[2])
		print 'sub_mean: ', self.sub_mean,'\n\n'
		#self.sub_mean = [[[213, 213, 206], [214, 214, 206], [211, 212, 206], [206, 207, 202], [204, 205, 203], [196, 200, 200], [191, 195, 198], [186, 190, 195]],
											#[[224, 223, 214], [224, 223, 214], [221, 222, 215], [217, 218, 213], [211, 212, 208], [202, 204, 204], [197, 200, 203], [186, 190, 198]],
											#[[228, 228, 220], [186, 176, 163], [145, 120, 106], [127, 97, 83], [136, 102, 89], [153, 130, 120], [111, 104, 102], [62, 62, 65]],
											#[[184, 169, 148], [129, 92, 77], [195, 145, 127], [171, 126, 115], [190, 132, 120], [179, 123, 115], [168, 114, 109], [41, 29, 33]],
											#[[170, 152, 127], [153, 109, 83], [208, 155, 133], [178, 134, 120], [199, 139, 125], [189, 133, 122], [192, 135, 123], [56, 39, 40]],
											#[[217, 215, 203], [150, 133, 112], [132, 98, 78], [140, 100, 81], [162, 117, 98], [145, 110, 92], [143, 121, 101], [98, 95, 87]],
											#[[219, 220, 212], [220, 221, 213], [213, 212, 198], [198, 195, 181], [191, 187, 173], [197, 196, 184], [209, 211, 206], [208, 212, 211]],
											#[[210, 211, 203], [211, 212, 205], [213, 214, 207], [213, 215, 210], [212, 216, 211], [211, 215, 211], [208, 212, 211], [204, 208, 207]]]
		#print self.sub_mean
		self.selection_block()
	#

	def rgb2hsv(self, rgb):
		"""Conversion d'un 3-uplets RGB en 3-uplets HSV."""
		rgb = map(operator.div, rgb, [float(255)]*3)
		MAX = max(rgb)
		MIN = min(rgb)
		DELTA = float(MAX-MIN)
		#print 'MAX', MAX, 'MIN', MIN, 'rgb',rgb, 'delta',DELTA
		R,G,B = rgb[0], rgb[1], rgb[2]

	# Hue = Teinte
		#caseH = {
			#MAX==MIN: 0,
			#MAX==R and G>=B: 60*(G-B)/DELTA,
			#MAX==R and G<B: 60*(G-B)/DELTA+360,
			#MAX==G: 60*(B-R)/DELTA+120,
			#MAX==B: 60*(R-G)/DELTA+240
		#}

		if MAX==MIN:
			H = 0
		elif MAX==R and G>=B:
			H = 60*(G-B)/DELTA
		elif MAX==R and G<B:
			H = 60*(G-B)/DELTA+360
		elif MAX==G:
			H = 60*(B-R)/DELTA+120
		elif MAX==B:
			H = 60*(R-G)/DELTA+240
	# Saturation
		if MAX==0:
			S = 0
		else:
			S = 1-float(MIN)/MAX # fivision flottante
	# Value
		V = MAX # VALUE = maximum des 3 composantes
		#print H,S,V
		return [H,S,V]
	#

	def HSVtest(self, sub_mean2):
		"""Dis si la case est valide ou non avec la méthode HSV"""
		HSV = self.rgb2hsv(sub_mean2)
		H, S, V = HSV[0], HSV[1], HSV[2]
		#print 'HSV:', H,S,V
		p1= S>=0.5
		p2= V>=0.3
		p3= V<=0.7
		p4 = (H in range(330,360) or H in range(0,30))


		#s1, s2 = 1, 0.05 # diamètre du cylindre = Saturation (normal, réduit)
		##s1 = 1# diamètre du cylindre = Saturation (normal, réduit)
		#v1 = v2 = 1 # hauteur du cône dans le spectre HSV (normale, tronqué)
		#p1 = S**2-(V)**2 <= (s1/v1)**2 # équation du cône-supérieur : z^2 = (x^2+y^2)/s^2
		#p2 = S**2-(V)**2 >= (s2/v2)**2 # opérateur puissance : **
		##p1 = S**2-(2*(0.5-V))**2 <= (s1/(v1/2))**2 # équation du cône-supérieur : z^2 = (x^2+y^2)/s^2
		##p2 = S**2-(2*(0.5-V))**2 >= (s2/(v2/2))**2 # opérateur puissance : **
		#p3 = (H in range(300,360) or H in range(0,100))
		print 'sub_mean2:', sub_mean2, 'HSV:',HSV, 'Pi:', [p1, p2, p3,p4]
		return p1  and  p2 and  p3
	#

	def selection_block(self):
		self.valid_area = [] # on construit la liste des sous-blocs respectant la condition
		self.gribouillage = ImageDraw.Draw(self.photo[1]) # crée un objet de dessin
		# détection des zones supérieur à la moyenne
		for i in range(self.nblock): # parcours les zones horizontalement
			for j in range(self.nblock): # parcours les zones verticalement
				mean2 = map(int, [1.05*self.mean[0],self.mean[1],self.mean[2]]) # moyenne avec le canal rouge renforcé
				sub_mean2 = self.sub_mean[i][j]
				#print 'sub_mean: ', self.sub_mean[i][j], '# mean:', self.mean, '# mean2:', mean2, '# sub_mean-mean:', map(operator.sub, self.sub_mean[i][j], mean2)
				methode_selection = { # structure équivalente à un case
					'rgb':sub_mean2[0] > mean2[0] and sub_mean2[1] < mean2[1] and sub_mean2[2] < mean2[2], # la zones à une couleur moyenne supérieur à la couleur moyenne de l'image
					'hsv': self.HSVtest(sub_mean2)
				}
				if methode_selection[self.methode]==TRUE:
					self.valid_area.append((i,j))
					self.gribouillage.rectangle([(i*self.block_size[0], j*self.block_size[1]), ((i+1)*self.block_size[0], (j+1)*self.block_size[1])], fill=(self.sub_mean[i][j][0], self.sub_mean[i][j][1], self.sub_mean[i][j][2]))#
				else:# non valide
					self.gribouillage.rectangle([(i*self.block_size[0], j*self.block_size[1]), ((i+1)*self.block_size[0], (j+1)*self.block_size[1])], fill='green')#

				self.invoque_img() # = rafraichissement du contenu du canvas
		print self.valid_area

	#
##parmis ceux qui sont rouge: on regarde ceux qui ont une composante bleu/vert faible.
##seconde selection : on teste les distances des carrés retenus. on ne retient dans B2 que les carrés adjacents.
#for i=1:nb-1
  #for j=i+1:nb
  #if abs(B(i,1)-B(j,1))<2 #pt'etre à changer en 1
  #and abs(B(i,2)-B(j,2))<2
  #then

  #for m=1:nb2-1
    #if B2(m,:)=B(i,:) then
    #break
    #nb2=nb2+1
    #B2(nb2,:)=B(i,:)
  #end
  #B2(nb2+1,:)=B(j,:)

  #end
 #end
#end


if __name__ == "__main__":
	app = Application() # création de l'appli

#image -> image + image avec seulement la bouche sur fond vert

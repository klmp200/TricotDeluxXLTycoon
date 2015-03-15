# -*- coding: utf8 -*-
import sys
import pygame
from pygame.locals import *

class Video():

	"""
		Permet d'afficher des vidéos en plein écran
	"""

	def __init__(self, video, SETTINGS, titre="", icone="", son="", FPS=60):
		self.FPS = FPS
		self.SETTINGS = SETTINGS
		self.video = pygame.movie.Movie(SETTINGS['VIDEOS_DIR'] + video)
		self.screen = pygame.display.set_mode(self.video.get_size())
		self.video_screen = pygame.Surface(self.video.get_size()).convert()
		self.clock = pygame.time.Clock()

		if son != "":
			self.son = (True, pygame.mixer.Sound(SETTINGS['SONS_DIR'] + son))
		else:
			self.son = (False, "")

		self.titre = titre
		if icone != "":
			icone = pygame.image.load(SETTINGS['IMAGES_DIR'] + icone)
			pygame.display.set_icon(icone)
		pygame.display.set_caption(self.titre)

	def jouer(self):
		if self.video.has_audio() and self.son[0] == False:
			self.video.set_volume(0.99)
		elif self.son[0]:
			self.video.set_volume(0.0)
			self.son[1].play(loops=-1, maxtime=0, fade_ms=0)

		self.video.set_display(self.video_screen)
		self.video.play()

		playing = True
		while playing:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					playing = False
				elif event.type == pygame.QUIT:
					playing = False
					sys.exit() 

			if self.video.get_busy() == False:
				playing = False

			self.screen.blit(self.video_screen,(0,0))
			pygame.display.update()
			self.clock.tick(self.FPS)

		self.video.stop()
		if self.son[0]:
			self.son[1].stop()
#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import platform
import time

class SeleniumManager:

	def __init__(self, waiting_time, nbr_request_max=100):

		""" initialize """
		self.waiting_time = waiting_time
		self.nbr_request = 0
		self.driver = None
		self.nbr_request_max = nbr_request_max
		
		""" no client at initialization """
		self.client = None

		self.init_driver()

		""" no time limit the first time """
		self.last_time = time.time()-waiting_time

	def init_driver(self):
		""" different drivers between os"""
		os_driver = "error"
		if platform.system() == "Windows":
			os_driver = "/libraries/SNScrapping/seleniumClass/geckodriver_windows64.exe"
		elif platform.system() == "Linux":
			os_driver = "/libraries/SNScrapping/seleniumClass/geckodriver_linux"
			#os_driver = "/seleniumClass/geckodriver_linux"
		else :
			print("OS not supported")

		if os_driver != "error" :
			self.driver = webdriver.Firefox(executable_path=os.getcwd()+os_driver)

		#delete all cookies initially
		self.driver.delete_all_cookies()
		self.driver.set_page_load_timeout(120)

	""" connection on a social network with a client datas and managing of the connection"""
	def connection(self, client):

		""" if time between now and last request or connection is less than parameter waiting_time we wait """
		if time.time()-self.last_time<self.waiting_time:
			time.sleep(self.waiting_time-(time.time()-self.last_time))

		"""initialize"""
		self.client = client 

		print("Connection with client")
		"""open url connection and manage connection """
		self.get(client.link_login, 3)

		while (self.client.login()!=True):
			#new driver to delete all possible problems
			self.driver_quit()
			self.init_driver()
			#specify new driver to client
			self.client.driver = self.driver
			#try again
			self.client.login()

		print("Connection is working")

		""" update last request time """
		self.last_time = time.time()

	def reconnection(self):
		""" if time between now and last request or connection is less than parameter waiting_time we wait """
		if time.time()-self.last_time<self.waiting_time:
			time.sleep(self.waiting_time-(time.time()-self.last_time))

		"""open url connection and manage connection """
		self.get(self.client.link_login, 3)
		self.client.login()
		print("Reconnection is working.")

		""" update last request time """
		self.last_time = time.time()		

	

	""" Permet de gérer le temps entre les requêtes """
	def get(self, url, pause_time):

		""" Test if we are connected on a social network """
		if self.client != None:

			""" reboot the client if the number of request is more than parameter nbr_request_max """
			if self.nbr_request > self.nbr_request_max:
				self.nbr_request = 0
				self.client.rebootSettings()
				self.reconnection()
				self.last_time = time.time()
				print("Reboot settings")


			""" if time between now and last request or connection is less than parameter waiting_time we wait """
			if time.time()-self.last_time<self.waiting_time:
				time.sleep(self.waiting_time-(time.time()-self.last_time))

			""" Try to go to the url specified 3 times, reconnecting each time, than stop if fail """
			isonpage = False
			numbersTry = 0
			while (not isonpage) and (numbersTry<3):
				try:
					""" increase the numbers of request effectued with this login """
					self.nbr_request = self.nbr_request + 1
					numbersTry = numbersTry + 1
					self.driver.get(url)
					isonpage = True

					""" wait requisite time """
					time.sleep(pause_time)

					""" keep in memory the time """
					self.last_time = time.time()
				except TimeoutException as ex:
					print("Exception has been thrown. " + str(ex))
					#new driver to delete all possible problems
					self.driver_quit()
					self.init_driver()
					#specify new driver to client
					self.client.driver = self.driver
					""" restart with a login() first """
					self.reconnection()

			if numbersTry >= 3:
				raise ValueError('Connection with client fail')
		else:
			print("Connection with a client necessary.")

	def driver_quit(self):
		self.driver.quit()
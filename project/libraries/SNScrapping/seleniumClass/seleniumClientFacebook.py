#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import randrange


class ClientFacebook(object):

    def __init__(self, driver, kwargs):
        self.settings = kwargs

        self.num_setting = randrange(0,len(self.settings))
        self.driver = driver
        self.username = kwargs[self.num_setting]["username"]
        self.password = kwargs[self.num_setting]["password"]
        self.link_login = "https://www.facebook.com/login/"

    def login(self):

        try:
            # Return False if connection impossible
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.ID, "email")
                )
            )
        except TimeoutException as ex:
            return False

        elem = self.driver.find_element_by_id("email")
        elem.clear()
        elem.send_keys(self.username)
        elem = self.driver.find_element_by_id("pass")
        elem.send_keys(self.password)
        # Enter credentials with Keys.RETURN
        elem.send_keys(Keys.RETURN)
        # Wait a few seconds for the page to load
        time.sleep(3)
        return True

    """ pass to another setting for the client """
    def rebootSettings(self):

        self.num_setting = self.num_setting + 1
        if self.num_setting == len(self.settings):
            self.num_setting = 0

        self.username = self.settings[self.num_setting]["username"]
        self.password = self.settings[self.num_setting]["password"]

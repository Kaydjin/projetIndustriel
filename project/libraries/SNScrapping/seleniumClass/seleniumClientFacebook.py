#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class ClientFacebook(object):

    def __init__(self, driver, kwargs):
        self.settings = kwargs

        self.num_setting = 0
        self.driver = driver
        self.username = kwargs[self.num_setting]["username"]
        self.password = kwargs[self.num_setting]["password"]
        self.link_login = "https://www.facebook.com/login/"

    def login(self):
        """login to linkedin then wait 3 seconds for page to load"""
        # Enter login credentials
        WebDriverWait(self.driver, 120).until(
            EC.element_to_be_clickable(
                (By.ID, "email")
            )
        )
        elem = self.driver.find_element_by_id("email")
        elem.send_keys(self.username)
        elem = self.driver.find_element_by_id("pass")
        elem.send_keys(self.password)
        # Enter credentials with Keys.RETURN
        elem.send_keys(Keys.RETURN)
        # Wait a few seconds for the page to load
        time.sleep(3)

    """ pass to another setting for the client """
    def rebootSettings(self):

        self.num_setting = self.num_setting + 1
        if self.num_setting == len(kwargs):
            self.num_setting = 0

        self.username = kwargs[num_setting]["username"]
        self.password = kwargs[num_setting]["password"]
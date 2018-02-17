#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ClientLinkedin(object):
    def __init__(self, driver, **kwargs):
        self.driver         =  driver
        self.username       =  kwargs["username"]
        self.password       =  kwargs["password"]

    def driver_quit(self):
        self.driver.quit()

    def login(self):
        """login to linkedin then wait 3 seconds for page to load"""
        # Enter login credentials
        WebDriverWait(self.driver, 120).until(
            EC.element_to_be_clickable(
                (By.ID, "session_key-login")
            )
        )
        elem = self.driver.find_element_by_id("session_key-login")
        elem.send_keys(self.username)
        elem = self.driver.find_element_by_id("session_password-login")
        elem.send_keys(self.password)
        # Enter credentials with Keys.RETURN
        elem.send_keys(Keys.RETURN)
        # Wait a few seconds for the page to load
        time.sleep(3)
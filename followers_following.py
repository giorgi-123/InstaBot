#!/usr/bin/python3
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from helping_tool import username, password, profile_name
from time import sleep


ser = Service("/usr/local/bin/chromedriver")
ID = "id"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
NAME = "name"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"

class Get_in:
    def __init__(self, username, password, profile_name):
        self.username = username
        self.password = password
        self.profile_name = profile_name
        self.driver = webdriver.Chrome(service=ser)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(width=1920, height=1080)
        self.driver.get("https://www.instagram.com")
        sleep(1.2)
        self.driver.find_element(By.NAME, "username").send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH,
            '//*[@id="loginForm"]/div/div[3]/button'
        ).click()
        sleep(3)
        self.driver.find_element(By.XPATH,
            '//*[@id="react-root"]/section/main/div/div/div/div/button'
        ).click()
        sleep(1)
        self.driver.find_element(By.XPATH,
            "/html/body/div[5]/div/div/div/div[3]/button[2]"
        ).click()
        sleep(1)
        self.driver.find_element(By.XPATH,
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'
        ).send_keys(self.profile_name)
        sleep(2)
        self.driver.find_element(By.XPATH,
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a'
        ).click()
        sleep(2)


    def get_unfollowers(self):
        # Get Followers
        self.driver.find_element(By.XPATH,
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
        ).click()
        followers = self._get_names(2)
        # Get Followings
        self.driver.find_element(By.XPATH,
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
        ).click()
        following = self._get_names(3)
        for i in followers:
            if i in following:
                following.remove(i)

        print("-" * 80)
        print(*following, sep=" | ")
        self.driver.quit()


    def _get_names(self, _index):
        sleep(1)
        scrolling = self.driver.find_element(By.XPATH,
            "/html/body/div[6]/div/div/div/div[" + str(_index) + "]"
            )
        counter = self.driver.find_element(By.XPATH,
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[' + str(_index) +']/a/div/span'

        ).text

        if "." in counter:
            counter = counter.replace(".", "")
        elif "," in counter:
            counter = counter.replace(",", "")
        
        if "k" in counter:
            follower_number = int(counter.replace("k", "000"))
        elif "m" in counter:
            follower_number = int(counter.replace("m", "000000"))
        else:
            follower_number = int(counter)

        
        sleep(1)

        div_container = self.driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[' + str(_index) +']/ul/div')

        while True:
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                scrolling,
            )
            li_elements_list = div_container.find_elements(By.TAG_NAME, 'li')
            if len(li_elements_list) == follower_number:
                break

        sleep(1)
        all_elements = self.driver.find_element(By.XPATH, 
            '/html/body/div[6]/div/div/div/div[' + str(_index) +']/ul/div'
        )
        sleep(1)
        links = all_elements.find_elements(By.TAG_NAME, "a")
        all_names = [names.text for names in links if names.text != '']
        self.driver.find_element(By.XPATH, 
            '/html/body/div[6]/div/div/div/div[1]/div/div[2]/button'
        ).click()

        return all_names
    


if username == "" or password == "" or profile_name == "":
    print("\nPlease Enter Username, password and profile name !")
else:
    startgetin = Get_in(username, password, profile_name)
    startgetin.get_unfollowers()

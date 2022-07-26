import os
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

def setProfile(name: str, options):
    options.add_argument("user-data-dir=" + os.path.abspath(__file__) + os.pathsep + "env" + os.pathsep + name)
    return options

options = webdriver.ChromeOptions()

# env settings
driver = webdriver.Chrome(ChromeDriverManager().install(), options=setProfile("env1", options))

# open instagram
driver.get("https://www.instagram.com/")

sendUsers = []
if os.path.exists("users.txt"):
    with open("users.txt", "r") as f:
        sendUsers = f.read().splitlines()
        print("load users from file")
        print("count: " + str(len(sendUsers)))

driver.implicitly_wait(5)
# wait login
while True:
    if driver.current_url == "https://www.instagram.com/":
        break
    sleep(1)

# search bar
tagname = "cats"

count = 0
while True:
    driver.get("https://www.instagram.com/explore/tags/" + tagname + "/")
    driver.implicitly_wait(10)
    sleep(5)
    posts = driver.find_elements(By.CLASS_NAME, "_aagw")
    posts[count].click()
    sleep(5)
    print("clicked")
    atags = driver.find_elements(By.TAG_NAME, "a")
    name = ""
    for atag in atags:
        clazz = "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl _acan _acao _acat _acaw _a6hd"
        if atag.get_attribute("class") == clazz:
            name = atag.text
            sleep(5)
            print("NAME: " + name)
            break
    if name == "":
        continue
    if name in sendUsers:
        count += 1
        continue

    # send msg
    msg = "Hello " + name + "! #cats"
    url = "https://www.instagram.com/direct/inbox/"
    driver.get(url)
    driver.implicitly_wait(10)
    sleep(3)
    svgs = driver.find_elements(By.TAG_NAME, "svg")
    for svg in svgs:
        aria_label = "新規メッセージ"
        if svg.get_attribute("aria-label") == aria_label:
            svg.click()
            break

    # get cursor
    driver.implicitly_wait(10)
    sleep(3)
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for input in inputs:
        if input.get_attribute("placeholder") == "検索...":
            input.send_keys(name)
            sleep(15)
            break

    sleep(5)
    circles = driver.find_elements(By.TAG_NAME, "circle")
    for circle in circles:
        cx = "12.008"
        r = "11.25"
        if circle.get_attribute("cx") == cx and circle.get_attribute("r") == r:
            circle.click()
            break

    sleep(5)

    divs = driver.find_elements(By.TAG_NAME, "div")
    for div in divs:
        clazz = "_aagz"
        text = "次へ"
        if div.get_attribute("class") == clazz and div.text == text:
            div.click()
            break

    textareas = driver.find_elements(By.TAG_NAME, "textarea")
    for textarea in textareas:
        placeholder = "メッセージ..."
        if textarea.get_attribute("placeholder") == placeholder:
            textarea.send_keys(msg)
            textarea.send_keys(Keys.ENTER)
            break

    sleep(5)
    driver.implicitly_wait(10)
    sleep(3)
    count += 1

    # write user to file
    with open("users.txt", "a") as f:
        f.write(name + "\n")
    sendUsers.append(name)
    print("SENT: " + name)

    # wait hour
    print("wait hour")
    print("count: " + str(count))
    sleep(60*60)







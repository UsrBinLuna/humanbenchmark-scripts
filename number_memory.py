from selenium import webdriver
from selenium.webdriver.common.by import By
from getpass import getpass
from time import sleep
import base64
import os

limit: int = input("How many digits would you like to do? ")

file_ask2 = None
if os.path.isfile("credentials"):
    file_ask = input("Credentials file found. Use existing authentication? (Y/n) ")
    if file_ask == "y" or file_ask == "yes" or file_ask == "Y" or file_ask == "Yes":
        file = open("credentials", "rb")
        content = file.readlines()
        file.close()

        un_b64 = content[0].decode("utf-8").strip()
        pw_b64 = content[1].decode("utf-8").strip()
        username = str(base64.b64decode(un_b64[2:-1]))[2:-1]
        password = str(base64.b64decode(pw_b64[2:-1]))[2:-1]

    else:
        username = input("Username: ")
        password = getpass("Password (will not echo): ")
        file_ask2 = input("Store credentials to encrypted file? (Y/n):" )

else: 
    username = input("Username: ")
    password = getpass("Password (will not echo): ")
    file_ask2 = input("Store credentials to encrypted file? (Y/n): " )


if file_ask2 == "y" or file_ask2 == "yes" or file_ask2 == "Y" or file_ask2 == "Yes":

    # check if file exists. if so, delete
    if os.path.isfile("credentials"):
        os.remove("credentials")

    # encode strings for encryption
    un_enc = username.encode(encoding = 'UTF-8', errors = 'strict')
    pw_enc = password.encode(encoding = 'UTF-8', errors = 'strict')
    un_b64 = base64.b64encode(un_enc)
    pw_b64 = base64.b64encode(pw_enc)


    file = open("credentials", "w+")
    creds = [str(un_b64) + "\n", str(pw_b64) + "\n"]
    file.writelines(creds)
    file.close()

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
web = webdriver.Chrome(options=options)

url_login = "https://humanbenchmark.com/login"
web.get(url_login)
# wait for page to load
web.implicitly_wait(5)

# login
text_area = web.find_element(by=By.NAME, value="username")
text_area.send_keys(username)

text_area = web.find_element(by=By.NAME, value="password")
text_area.send_keys(password)

# submit and wait for user page to load
web.implicitly_wait(1)
login_btn = web.find_element(by=By.CLASS_NAME, value='css-z5gx6u')
login_btn.click()
web.implicitly_wait(3)

play_btn = web.find_element(by=By.XPATH, value='//a[contains(@href,"/tests/number-memory")]')
play_btn.click()
sleep(2)

nr_text = None
i: int = 1
while True:
    if nr_text == None:
        start_btn = web.find_element(by=By.CLASS_NAME, value="css-de05nr")
        start_btn.click()
    else:
        start_btn = web.find_element(by=By.CLASS_NAME, value="css-de05nr")
        start_btn.click()
        web.implicitly_wait(2)
        start_btn = web.find_element(by=By.CLASS_NAME, value="css-de05nr")
        start_btn.click()
    number_text = web.find_element(by=By.CLASS_NAME, value='big-number')
    print(number_text.text)
    nr_text = number_text.text
    web.implicitly_wait(10+i)
    submit_area = web.find_element(by=By.CSS_SELECTOR, value='#root > div > div:nth-child(4) > div.number-memory-test.prompt.e12yaanm0.css-18qa6we.e19owgy77 > div > div > div > form > div:nth-child(2) > input[type=text]')
    submit_area.send_keys(nr_text)
    
    if int(i) >= int(limit):
        exit()
    i += 1

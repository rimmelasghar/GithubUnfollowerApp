import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
from selenium.common.exceptions import NoSuchElementException


cred = open('info.txt','rt')
context = cred.read()
context = context.split('\n')

user_name = context[0]
user_pass = context[1]



def extract_digit(digit):
    y = ''
    for i in digit:
        if i.isdigit():
            y += i
    return int(y)


PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://github.com/login")

sleep(3)
username = driver.find_element(By.XPATH,'//input[@name="login"]')
username.send_keys(user_name)

sleep(3)
password = driver.find_element(By.XPATH,'//input[@name="password"]')
password.send_keys(user_pass)

sleep(3)
submit = driver.find_element(By.XPATH,'//input[@type="submit"]')
submit.click()

sleep(3)

try:
    drop = driver.find_element(By.XPATH,'/html/body/div[1]/header/div[7]/details/summary')
    drop.click()
    sleep(3)
    pth = f'//details-menu//a[@href="/{user_name}"][@role="menuitem"][@class="dropdown-item"]'
    profile = driver.find_element(By.XPATH,pth)
    profile.click()
    sleep(3)
except NoSuchElementException:
    nav = driver.find_element(By.XPATH,'//button[@aria-label="Toggle navigation"]')
    nav.click()
    pth = f'//nav//a[@href="/{user_name}"]'
    profile = driver.find_element(By.XPATH,pth)
    profile.click()

sleep(10)
pth = f'//a[@href="https://github.com/{user_name}?tab=followers"]'
follower = driver.find_element(By.XPATH,pth)
follower.click()

followers_lst=[]
followers = extract_digit(follower.text)
follower_count = 0

while True:

    if followers > 48:

        sleep(2)
        user_followers = driver.find_elements(By.XPATH,'//span[@class ="Link--secondary pl-1"]')
        for i in user_followers:
            followers_lst.append(i.text)
        # follower_count += len(user_followers)
        follower_count += 48
        if follower_count >= followers:
            break
        else: 
            try:
                sleep(2)
                Next = driver.find_element(By.XPATH,'//a[contains(text(),"Next")]')
                Next.click()
                sleep(1)
            except NoSuchElementException:
                pass
            else:
                break
    else:
        sleep(2)
        user_followers = driver.find_elements(By.XPATH,'//span[@class ="Link--secondary pl-1"]')
        for i in user_followers:
            followers_lst.append(i.text)
        break
        
sleep(3)
lst = [[i] for i in followers_lst]

filename = csv.writer(open("myfollowers.csv","w",newline=''),delimiter=',')
filename.writerows(lst)

sleep(1)
pth = f'//a[@href="https://github.com/{user_name}?tab=following"]'
following =  driver.find_element(By.XPATH,pth)
following.click()

followings = extract_digit(following.text)
followings_count = 0
sleep(4)
while True:
    if followings > 48:
        sleep(2)
        user_followings = driver.find_elements(By.XPATH,'//span[@class ="Link--secondary pl-1"]')
        for i in user_followings:
            if i.text not in followers_lst:
                pth = f'//input[@title="Unfollow {i.text}"]'
                user = driver.find_element(By.XPATH,pth)
                user.click()
        followings_count += len(user_followings)
        if followings_count >= followings:
            break
        else:
            try:
                sleep(2)
                Next = driver.find_element(By.XPATH,'//a[contains(text(),"Next")]')
                Next.click()
                sleep(1)
            except NoSuchElementException:
                    sleep(1)
                    pth = f'//a[@href="https://github.com/{user_name}?tab=following"]'
                    following =  driver.find_element(By.XPATH,pth)
                    following.click()
                    pass
    else:
        sleep(3)
        user_followings = driver.find_elements(By.XPATH,'//span[@class ="Link--secondary pl-1"]')
        for i in user_followings:
            if i.text not in followers_lst:
                pth = f'//input[@title="Unfollow {i.text}"]'
                user = driver.find_element(By.XPATH,pth)
                user.click()
        break

driver.close()
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib.request

# urllib.request.urlretrieve("url","zz.jpg")

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 5)

driver.get('https://www.google.com/')
elem = driver.find_element(By.CLASS_NAME,"gLFyf")
elem.send_keys("인물 사진")
elem.send_keys(Keys.RETURN)
driver.implicitly_wait(5)
elem = driver.find_element(By.CSS_SELECTOR,"#hdtb-msb > div:nth-child(1) > div > div:nth-child(2) > a")
elem.click()
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rg_i.Q4LuWd")))
small_img = driver.find_elements(By.CSS_SELECTOR,".rg_i.Q4LuWd")
print(len(small_img))

img_arr = []
for img in range(len(small_img)):
    xpath='//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]'
    driver.execute_script("arguments[0].scrollIntoView();", small_img[img])
    small_img[img].click()
    wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    imgUrl = driver.find_element(By.XPATH,xpath).get_attribute("src")
    img_arr.append(imgUrl)

print("## 작업 끝 ##")

count=0
for url in img_arr:
    try:
        count = count+1
        now = datetime.datetime.now()
        date = "{}-{}-{}:{}".format(now.year,now.month,now.day,count)
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url,"person/"+date+".jpg")
        print(date+".jpg")
    except:
        pass
    finally:
        print("job done")
        
driver.close()
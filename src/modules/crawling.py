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

from .json_job import update_count_to_json, get_count_to_json,in_history_json,update_history_to_json
import urllib.request

# urllib.request.urlretrieve("url","zz.jpg")
def crawling_and_save(search_name, isPass):
    # 이미 수집한 이미지는 수집하지 않음
    if in_history_json(isPass, search_name):
        return print("'{}'는 이미 수집한 이미지 입니다.".format(search_name))
    
    try:
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        wait = WebDriverWait(driver, 10)

        driver.get('https://www.google.com/')
        elem = driver.find_element(By.CLASS_NAME,"gLFyf")
        elem.send_keys(search_name)
        elem.send_keys(Keys.RETURN)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a')))
        elem = driver.find_element(By.CSS_SELECTOR,"#hdtb-msb > div:nth-child(1) > div > div:nth-child(2) > a")
        elem.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rg_i.Q4LuWd")))
        small_img = driver.find_elements(By.CSS_SELECTOR,".rg_i.Q4LuWd")
        print(len(small_img))

        img_arr = []
        wait_img = WebDriverWait(driver, 3)
        for img in range(len(small_img)):
            try:
                xpath='//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]'
                driver.execute_script("arguments[0].scrollIntoView();", small_img[img])
                small_img[img].click()
                wait_img.until(EC.presence_of_element_located((By.XPATH, xpath)))
                imgUrl = driver.find_element(By.XPATH,xpath).get_attribute("src")
                img_arr.append(imgUrl)
            except:
                pass
                

        # pass 사진인지 nonPass 사진인지 분류
        subdirectory = 'pass' if isPass else 'nonPass'
        # 이미지 파일의 이름을 순번과 중복방지임
        count= get_count_to_json(isPass)
        cnt_for_json = 0
        for url in img_arr:
            try:
                count = count+1
                now = datetime.datetime.now()
                date = "{}-{}-{}:{}".format(now.year,now.month,now.day,count)
                opener=urllib.request.build_opener()
                opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(url,"imgs/{}/".format(subdirectory)+date+".jpg")
                print(date+".jpg")
                cnt_for_json = cnt_for_json+1
            except:
                pass
        # 이미지 파일 이름 저장
        update_count_to_json(isPass,count)
        update_history_to_json(isPass,cnt_for_json,search_name)
                
        driver.close()

    except:
        print("수행중 오류가 발생했습니다.")








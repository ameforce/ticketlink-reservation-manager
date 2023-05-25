from libs.selechecker import selechecker
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from playsound import playsound
import random
import datetime
import time


def log(log_level: str, content: str):
    print(f'[{datetime.datetime.now()}] {log_level}: {content}')


def get_element_by_xpath(driver: webdriver.Chrome, xpath_content: str, is_print_log: bool = True):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, xpath_content))
    )
    if is_print_log:
        log('INFO', f'XPATH is detected: {element}')
    return element


def click_next_date_page(driver: webdriver.Chrome):
    get_element_by_xpath(driver, '//*[@id="content"]/section[2]'
                                 '/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/button[2]/span[1]').click()


def click_date(driver: webdriver.Chrome, date: str):
    while True:
        calendar_month = get_element_by_xpath(driver, '//*[@id="content"]/section[2]'
                                                      '/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/strong').text
        if calendar_month == '2023.06':
            break
        click_next_date_page(driver)
    if date == '0617':
        get_element_by_xpath(driver, '//*[@id="content"]/section[2]'
                                     '/div[1]/div[1]/div/div/div[2]/div[2]/div[3]/div[7]').click()
    elif date == '0618':
        get_element_by_xpath(driver, '//*[@id="content"]/section[2]'
                                     '/div[1]/div[1]/div/div/div[2]/div[2]/div[4]/div[1]').click()


def alert_music():
    while True:
        playsound('sounds\\alert.wav')


def main_logic(driver: webdriver.Chrome, valid_date_list: list[str]):
    seat_data = ''
    for date in valid_date_list:
        click_date(driver, date)
        for i in range(4):
            log('INFO', f'[{i + 1} / 4] Try to get remaining seats. ({date})')
            get_element_by_xpath(driver, f'//*[@id="content"]/section[2]'
                                         f'/div[1]/div[2]/ul/li[{i + 1}]/button/span').click()  # 10시 00분
            seat_data = get_element_by_xpath(driver, '//*[@id="content"]/section[2]'
                                                     '/div[1]/div[3]/ul/li/span[2]/span').text
            if seat_data != '매진':
                break
            random_time = random.uniform(0, 2.5)
            log('INFO', f'Waiting for {random_time}')
            time.sleep(random_time)
        if seat_data != '매진':
            break
    if seat_data == '매진':
        driver.refresh()
        init_popup_close_logic(driver)
        return
    get_element_by_xpath(driver, '//*[@id="content"]/section[2]/div[2]/div[2]/a').click()
    while len(driver.window_handles) == 1:
        time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[1])
    driver.execute_script('javascript:_requestAuth()')
    alert_music()
    time.sleep(50000)


def login_logic(driver: webdriver.Chrome, payco_id: str, payco_pw: str, payco_birth: str):
    get_element_by_xpath(driver, '//*[@id="app"]/div/header/div[1]/div/div[2]/ul/li[1]/a').click()
    while len(driver.window_handles) == 1:
        time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[1])
    get_element_by_xpath(driver, '//*[@id="id"]').send_keys(payco_id)
    get_element_by_xpath(driver, '//*[@id="pw"]').send_keys(payco_pw)
    get_element_by_xpath(driver, '//*[@id="loginBtn"]').click()
    get_element_by_xpath(driver, '//*[@id="birthday"]').send_keys(payco_birth)
    get_element_by_xpath(driver, '//*[@id="confirmBtn"]').click()
    while len(driver.window_handles) != 1:
        time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[0])


def init_popup_close_logic(driver: webdriver.Chrome):
    get_element_by_xpath(driver, '//*[@id="app"]/div[1]/div/div/div[2]/button', False).click()


def init_variable() -> str and str and list[str] and webdriver.Chrome:
    payco_id = 'kwg0085@naver.com'
    payco_pw = 'dlsvp2tmxm'
    payco_birth = '19980210'
    valid_date_list = ['0617', '0618']
    url = 'https://www.ticketlink.co.kr/product/43830'
    driver = webdriver.Chrome(selechecker.driver_check())
    driver.get(url)
    driver.implicitly_wait(5)
    init_popup_close_logic(driver)
    login_logic(driver, payco_id, payco_pw, payco_birth)
    init_popup_close_logic(driver)
    return valid_date_list, driver


def main():
    valid_date_list, driver = init_variable()
    main_logic(driver, valid_date_list)
    driver.close()


if __name__ == '__main__':
    main()

# coding:utf-8
# usage :python2.7 demo.py user password cookies.txt
# 等待时间 产生随机数
import time
# Geettest 验证码
import geecrack
# web测试
from selenium import webdriver
# 鼠标操作
# 预期条件
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import sys

username = sys.argv[1]
password = sys.argv[2]

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = "/opt/google/chrome/chrome"

driver = webdriver.Chrome(chrome_options=chrome_options,executable_path="/opt/google/chromedriver")
driver.get("https://www.tianyancha.com/")
wait = WebDriverWait(driver, 100)
wait.until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div[4]/a')))

login_btn = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div[4]/a')
login_btn.click()
time.sleep(0.11)

pwd_login = '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[1]/div[2]'
wait.until(expected_conditions.presence_of_element_located((By.XPATH, pwd_login)))
pwd_btn = driver.find_element_by_xpath(pwd_login)
pwd_btn.click()
time.sleep(0.2)

phone_input = '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[2]/input'
phone_btn = driver.find_element_by_xpath(phone_input)
pwd_input = '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/input'
pwd_btn = driver.find_element_by_xpath(pwd_input)
submit_input = '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[5]'
submit_btn = driver.find_element_by_xpath(submit_input)

phone_btn.send_keys(username)
pwd_btn.send_keys(password)
submit_btn.click()
# time.sleep(1)

wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'gt_slider_knob.gt_show')))
print("find slider")
slider = geecrack.get_slider(driver,slider_class='gt_slider_knob.gt_show')
ActionChains(driver).click_and_hold(slider).perform()


# 加载 Geetest 验证码
wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'gt_cut_fullbg')))
# wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'gt_slice gt_show')))

 # 获取加载的图片
bg_path = geecrack.get_image(driver, "//div[@class='gt_cut_bg_slice']") 
full_bg_path = geecrack.get_image(driver, "//div[@class='gt_cut_fullbg_slice']")

# 移动距离
distance = geecrack.get_offset(full_bg_path, bg_path, offset=35)
print(distance)
# 获取移动轨迹
track = geecrack.get_track(distance)
print(track)
# 滑动圆球至缺口处
geecrack.drag_the_ball(driver, track, slider)
# 到此就完成滑动验证码啦~
time.sleep(5)
geecrack.save_cookies(driver,sys.argv[3])

driver.close()

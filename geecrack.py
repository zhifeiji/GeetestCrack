# coding:utf-8

# 等待时间
import time
# 产生随机数
import random
# 图片转换
import base64
# 图像处理标准库
from PIL import Image
# 鼠标操作
from selenium.webdriver.common.action_chains import ActionChains

import time,re,requests,random
from io import  BytesIO 
import json


def save_base64img(data_str, save_name):
    """
    将 base64 数据转化为图片保存到指定位置
    :param data_str: base64 数据，不包含类型
    :param save_name: 保存的全路径
    """
    img_data = base64.b64decode(data_str)
    file = open(save_name, 'wb')
    file.write(img_data)
    file.close()


def get_base64_by_canvas(driver, class_name, contain_type):
    """
    将 canvas 标签内容转换为 base64 数据
    :param driver: webdriver 对象
    :param class_name: canvas 标签的类名
    :param contain_type: 返回的数据是否包含类型
    :return: base64 数据
    """
    # 防止图片未加载完就下载一张空图
    bg_img = ''
    while len(bg_img) < 5000:
        getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/png");'
        bg_img = driver.execute_script(getImgJS)
        time.sleep(0.5)
    # print(bg_img)
    if contain_type:
        return bg_img
    else:
        return bg_img[bg_img.find(',') + 1:]


def save_bg(driver, bg_path="bg.png", bg_class='geetest_canvas_bg geetest_absolute'):
    """
    保存包含缺口的背景图
    :param driver: webdriver 对象
    :param bg_path: 保存路径
    :param bg_class: 背景图的 class 属性
    :return: 保存路径
    """
    bg_img_data = get_base64_by_canvas(driver, bg_class, False)
    save_base64img(bg_img_data, bg_path)
    return bg_path


def save_full_bg(driver, full_bg_path="fbg.png", full_bg_class='geetest_canvas_fullbg geetest_fade geetest_absolute'):
    """
    保存完整的的背景图
    :param driver: webdriver 对象
    :param full_bg_path: 保存路径
    :param full_bg_class: 完整背景图的 class 属性
    :return: 保存路径
    """
    bg_img_data = get_base64_by_canvas(driver, full_bg_class, False)
    save_base64img(bg_img_data, full_bg_path)
    return full_bg_path


def get_slider(driver, slider_class='geetest_slider_button'):
    """
    获取滑块
    :param slider_class: 滑块的 class 属性
    :return: 滑块对象
    """
    while True:
        try:
            slider = driver.find_element_by_class_name(slider_class)
            break
        except:
            time.sleep(0.5)
    return slider


def is_pixel_equal(img1, img2, x, y):
    """
    判断两个像素是否相同
    :param image1: 图片1
    :param image2: 图片2
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """
    # 取两个图片的像素点
    pix1 = img1.load()[x, y]
    pix2 = img2.load()[x, y]
    threshold = 60
    if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
            pix1[2] - pix2[2] < threshold)):
        return True
    else:
        return False


def get_offset(full_bg, bg, offset=35):
    """
    获取缺口偏移量
    :param full_bg_path: 不带缺口图片路径
    :param bg_path: 带缺口图片路径
    :param offset: 偏移量， 默认 35
    :return:
    """
    # full_bg = Image.open(full_bg_path)
    # bg = Image.open(bg_path)
    for i in range(offset, full_bg.size[0]):
        for j in range(full_bg.size[1]):
            if not is_pixel_equal(full_bg, bg, i, j):
                offset = i
                return offset
    return offset


def get_track(distance):
    """
    根据偏移量获取拟人的移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    """
    track = []
    current = 0
    if distance <= 5 :
        while current < distance:
            move=1
            track.append(round(move))
            current += round(move)
    else:
        move = round(distance / 5.0)
        while current < distance:
            if distance - current < move:
                move = distance - current
            track.append(move)
            current += move
    return track


def drag_the_ball(driver, track, slider):
    """
    根据运动轨迹拖拽
    :param driver: webdriver 对象
    :param track: 运动轨迹
    """
    # slider = get_slider(driver)
    ActionChains(driver).click_and_hold(slider).perform()
    while track:
        x = random.choice(track)
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
        track.remove(x)
    time.sleep(0.1)
    # 模拟人往回滑动
    imitate = ActionChains(driver).move_by_offset(xoffset=-2, yoffset=0)
    time.sleep(0.015)
    imitate.perform()
    time.sleep(random.randint(6, 10) / 50.0)
    imitate.perform()
    time.sleep(0.04)
    imitate.perform()
    time.sleep(0.012)
    imitate.perform()
    time.sleep(0.019)
    # imitate.perform()
    # time.sleep(0.033)
    ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
    # 放开圆球
    ActionChains(driver).pause(random.randint(6, 14) / 10.0).release(slider).perform()

def get_merge_image(filename,location_list):
    '''
    合并图片
    filename: 下载的图片
    location_list: 位置列表
    ''' 
    im = filename
    new_im = Image.new('RGB', (260,116))
    im_list_upper=[]
    im_list_down=[]
    for location in location_list:
        if location['y']==-58:
            pass
            im_list_upper.append(im.crop((abs(location['x']),58,abs(location['x'])+10,166)))
        if location['y']==0:
            pass
            im_list_down.append(im.crop((abs(location['x']),0,abs(location['x'])+10,58)))
    new_im = Image.new('RGB', (260,116))
    x_offset = 0
    for im in im_list_upper:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    x_offset = 0
    for im in im_list_down:
        new_im.paste(im, (x_offset,58))
        x_offset += im.size[0]
    return new_im
def get_image(driver,div):
    '''
    下载并还原图片
    :driver:webdriver
    :div:图片的div
    '''
    pass
    #找到图片所在的div
    background_images=driver.find_elements_by_xpath(div)
    location_list=[]
    imageurl=''
    for background_image in background_images:
        location={}
        #在html里面解析出小图片的url地址，还有长高的数值
        location['x']=int(re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",background_image.get_attribute('style'))[0][1])
        location['y']=int(re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",background_image.get_attribute('style'))[0][2])
        imageurl=re.findall("background-image: url\(\"(.*)\"\); background-position: (.*)px (.*)px;",background_image.get_attribute('style'))[0][0]
        location_list.append(location)
    imageurl=imageurl.replace("webp","jpg")
    r = requests.get(imageurl)
    jpgfile = Image.open(BytesIO(r.content))
    #重新合并图片 
    image=get_merge_image(jpgfile,location_list )
    return image

def save_cookies(driver,cookie_path):
    cookies = driver.get_cookies()
    str = ""
    for cookie in cookies:
        str = str + cookie['name'] +"=" + cookie['value'] + "; "
    str += "\n"

    file = open(cookie_path, 'wb')
    file.write(str)
    file.close()
    print(str)
    pass
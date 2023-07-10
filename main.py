from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
import time
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import win32api
import win32con

PNG_INDEX = 0
TOKEN = "undefine" # Set your own token here

def get_ibb_url(sourse):
    # Define the regular expression pattern
    pattern = r'https://ibb\.co/[a-zA-Z0-9]{7}'

    # Test the pattern with a sample string
    string = sourse
    match = re.findall(pattern, string)

    # Print the match if found
    if match:
        print(match)
    return match

def crawl_ibb_url(url_str): # use the method of right click to download the image

    VK_CODE ={'enter':0x0D, 'down_arrow':0x28}

    def keyDown(keyName):
        win32api.keybd_event(VK_CODE[keyName], 0, 0, 0)

    def keyUp(keyName):
        win32api.keybd_event(VK_CODE[keyName], 0, win32con.KEYEVENTF_KEYUP, 0)

    # Set up the browser
    options = EdgeOptions()
    options.use_chromium = True
    options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    driver_ibb = Edge(options=options, executable_path=r"C:\edgedriver\msedgedriver.exe")


    driver_ibb.get(url_str)
    element = driver_ibb.find_element(By.ID, 'image-viewer-container').find_element(By.TAG_NAME, 'img')
    img_url = element.get_attribute('src')

    action = ActionChains(driver_ibb).move_to_element(element)
    action.context_click(element).perform()
    time.sleep(2)
    action.context_click(element).perform()

    win32api.keybd_event(86, 0, 0, 0)
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(2)

    keyDown("enter")
    keyUp("enter")
    time.sleep(2)


def crawl_url(url_str):
    # Set up the browser
    options = EdgeOptions()
    options.use_chromium = True
    options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    driver = Edge(options=options, executable_path=r"C:\edgedriver\msedgedriver.exe")

    # Navigate to the login page
    driver.get(url_str)

    # Set the token in local storage using JavaScript
    js = 'window.localStorage.setItem("TOKEN", "'+TOKEN + '")'
    driver.execute_script(js)

    # Wait for the token to be set
    time.sleep(2)

    # Refresh the page to apply the token
    driver.refresh()

    # Wait for the page to load
    time.sleep(5)

    sourse = driver.page_source
    if 'ibb.co' in sourse:
        url_list = get_ibb_url(sourse)
        for url in url_list:
            crawl_ibb_url(url)

    else:
        driver.find_element(By.CLASS_NAME, "flow-item").click()
        time.sleep(5)
        url_list = get_ibb_url(sourse)
        for url in url_list:
            crawl_ibb_url(url)


def crawl_hidden():
    # Set up the browser
    options = EdgeOptions()
    options.use_chromium = True
    options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    driver = Edge(options=options, executable_path=r"C:\edgedriver\msedgedriver.exe")

    # Navigate to the login page
    driver.get('https://new-t.github.io')

    # Set the token in local storage using JavaScript
    js = 'window.localStorage.setItem("TOKEN", "'+TOKEN + '")'
    driver.execute_script(js)

    # Wait for the token to be set
    time.sleep(2)

    # Refresh the page to apply the token
    driver.refresh()

    # Wait for the page to load. flip down the page to load more hidden content
    time.sleep(10)
    driver.execute_script("window.scrollBy(0,1000)")
    time.sleep(3)
    driver.execute_script("window.scrollBy(0,1000)")
    time.sleep(3)
    driver.execute_script("window.scrollBy(0,1000)")
    time.sleep(3)
    driver.execute_script("window.scrollBy(0,1000)")
    time.sleep(3)

    # Find all the elements with class name "box-header-cw"
    headers = driver.find_elements(By.CLASS_NAME,"box-header-cw")

    hidden_hole_num = []

    # Loop through the headers and find the sibling element for each one
    for header in headers:
        sibling = header.find_element(By.XPATH, 'preceding-sibling::*')
        hole_num = sibling.text.split('\n')
        if hole_num[0] not in hidden_hole_num:
            hidden_hole_num.append(hole_num[0])

    print(hidden_hole_num)

    for line in hidden_hole_num:
        url = 'https://new-t.github.io/#' + line.strip()
        crawl_url(url)
          
    # Close the browser
    driver.quit()

while True:
    crawl_hidden()
    time.sleep(1000) # crawl every 1000 seconds

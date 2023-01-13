#!/usr/bin/env python3

# About To Write Some Medium Level Heresy Using iFrame Sanboxed Object Poisoning

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import os, binascii, sys, pickle

BASE_URL = 'https://fakku.net'

def minify(file):
    '''
    Function To Convert Simple Multiline JS Into Single Scoped One Liners For Selenium Ease Of Use
    '''
    with open(file , 'r') as file:
        script = ''.join([line.strip() for line in file])
        file.close()
    return script

def login(driver):
    '''
    Boring Function Used To Automate Login, Since I Am Lazy
    '''
    driver.get(BASE_URL + '/login')
    try:
        with open('cookies_store', 'rb') as cookies_store:
            cookies = pickle.load(cookies_store)
            for cookie in cookies:
                    if "expiry" in cookie:
                        cookie["expiry"] = int(cookie["expiry"])
                        driver.add_cookie(cookie)
            cookies_store.close()

    except EOFError:
        cookies_store.close()
        with open('credentials_store', 'r') as credentials_store:
            credentials = credentials_store.readline()
            username = credentials.split(':')[0]
            password = credentials.split(':')[1]
            credentials_store.close()
        driver.find_element(By.XPATH, "//input[@ name='username']").send_keys(username)
        driver.find_element(By.XPATH, "//input[@ autocomplete='current-password']").send_keys(password)
        driver.find_element(By.XPATH, "//button[@ name='login']").click()
        input('Hit Enter Once You Have Logged In: ')
        with open('cookies_store', 'wb') as cookies_store:
            pickle.dump(driver.get_cookies(), cookies_store)
            cookies_store.close()

def infect(driver):
    '''
    Funky Exploit Code To Control What Functions Are Alive And Well
    '''
    # Prototype Poison To Enable Javascript Injection
    driver.execute_script(minify('injection.js'))
    # Hidden New Step (Bypass CORS' Tainted Canvas Using Proxied Global Object Pollution) "aka didn't work, but was cool. see scripts folder"
    driver.execute_script(minify('proxy.js'))
    # iFrame Sandboxed Object Prototype Creation
    iframe = driver.find_element(By.XPATH, '//iframe')
    driver.switch_to.frame(iframe)
    # Abuse Global Variables Inside of Sandbox (EWWWWW)
    driver.execute_script(minify('creation.js'))
    driver.switch_to.default_content()
    # Wait Until Canvas Loads
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//canvas[@ class="page"]')))
    # Prototype Poison Canvas -> Profit (Assuming Shit Worked!)
    driver.execute_script(minify('poison.js'))

def cleanup(driver):
    '''
    A Function To Run One Command (Bad Practice Please I Beg Ignore)
    '''
    driver.close()

def controller(driver, location, last_page=None):
    '''
    Main Controller That Selects Books To Download From A URL
    '''
    page_num = 1
    driver.get(BASE_URL + location + '/page_' + str(page_num))
    if last_page == None:
        last_page = driver.find_element(By.XPATH, "//a[@ title='Last Page']").get_attribute('href')
    while driver.current_url != last_page:
        book_elements = driver.execute_script('return document.querySelectorAll(\'a[href^="/hentai/"]:not([class])\');')
        book_names = [x.get_attribute('href') for x in book_elements]
        for book_name in book_names:
            download_book(driver, book_name)
        page_num += 1
        driver.get(BASE_URL + location + '/page_' + str(page_num))

def download_book(driver, book):
    '''
    Main Download Manager That Gets The Page Count And Returns The Images
    '''
    driver.get(book + '/read/page/1')
    infect(driver)
    max = int(driver.execute_script('return document.evaluate(\'//span[@ class="count js-count"]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerText;'))
    for i in range(1, max + 1):
        driver.get(book + '/read/page/' + str(i))
        infect(driver)
        export(driver.execute_script('return window.curedCanvas.toDataURL();'), book, str(i))

def export(data, book, filename):
    '''
    Export And Converter That Manages Folders And Converts The Data URL
    '''
    book_name_tokens = book.split('/')
    book_name = book_name_tokens[len(book_name_tokens) - 1]
    data = data.split('base64,')[1]
    if not os.path.exists('export/' + book_name):
        os.mkdir('export/' + book_name)
    with open('export/' + book_name + '/' + filename + '.png', 'wb') as file:
        file.write(binascii.a2b_base64(data))
        file.close()

def main():
    '''
    Procedural Main, I Am Not Going To Code A Whole OOP Object For This Dumb Bet
    '''
    try:
        # Thankfully This Defaults To 127.0.0.1:4444 The Default GeckoDriver Config On Build
        driver = WebDriver()
        login(driver)
        if sys.argv[len(sys.argv) - 1] != __file__:
            controller(driver, sys.argv[len(sys.argv) - 1])
    except KeyboardInterrupt:
        print('\nThanks For Testing This I Guess???')
    except Exception:
        print('Debug Me Dear God...')
    cleanup(driver)

if __name__ == '__main__':
    main()

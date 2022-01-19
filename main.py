from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from glob import glob
import os,json,time
from colorama import init, Fore, Style
init(convert=True)
red,green,yellow = Fore.RED,Fore.GREEN,Fore.YELLOW
reset = Style.RESET_ALL

class Reader:
    def __init__(self, path: str) -> None:
        self.path = path
        self.extract_json_file()

    def extract_json_file(self) -> None:
            self.data = json.loads(open(self.path, encoding='utf-8').read())
            self.collection=self.data["collection"]
            self.lists=self.data["lists"]
            self.lists_length = len(self.lists)



class Webdriver:
    def __init__(self) -> None:
        self.webdriver_path = os.path.abspath('Assets/chromedriver.exe')
        self.polkadot_extension_path = os.path.abspath('Assets/polkadot.crx')
        self.driver = self.webdriver()

    def webdriver(self) -> webdriver:
        options = webdriver.ChromeOptions()
        options.add_extension(self.polkadot_extension_path)
        options.add_argument("log-level=3")
        options.add_argument("--mute-audio")
        driver = webdriver.Chrome(service=Service(self.webdriver_path), options=options)
        driver.maximize_window()
        return driver

    def clickable(self, element: str) -> None:
        try:
            WDW(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, element))).click()
        except Exception:
            self.driver.execute_script('arguments[0].click();', self.visible(element))

    def visible(self, element: str, timer: int = 30):
        return WDW(self.driver, timer).until(
            EC.visibility_of_element_located((By.XPATH, element)))

    def send_keys(self, element: str, keys: str) -> None:
        try:
            self.visible(element).send_keys(keys)
        except Exception:
            WDW(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, element))).send_keys(keys)

    def send_date(self, element: str, keys: str) -> None:
        self.clickable(element)  # Click first on the element.
        self.send_keys(element, keys)  # Then send it the date.

    def clear_text(self, element) -> None:
        self.clickable(element)  # Click on the element then clear its text.
        control = Keys.CONTROL if os.name == 'nt' else Keys.COMMAND
        webdriver.ActionChains(self.driver).key_down(control).perform()
        webdriver.ActionChains(self.driver).send_keys('a').perform()
        webdriver.ActionChains(self.driver).key_up(control).perform()

    def window_handles(self, window_number: int) -> None:
        WDW(self.driver, 30).until(lambda _: len(
            self.driver.window_handles) >= window_number + 1)
        self.driver.switch_to.window(self.driver.window_handles[window_number])

    def tab_changes(self, tab: int) -> None:
        self.window_handles(tab)  # Switch to a tab that will be closed.
        old_tabs: list = self.driver.window_handles  # Old tabs list.
        WDW(self.driver, 15).until(  # Wait the tabs lists to be different.
            lambda _: self.driver.window_handles != old_tabs
            and len(self.driver.window_handles) == len(old_tabs))
        self.window_handles(tab)  # Switch to a tab with the same index.

class NFTmart:
    def __init__(self, recovery_phrase: str,password: str, description:str) -> None:
        self.recovery_phrase = recovery_phrase
        self.password = password
        self.description=description
        self.polkadot_login_url="chrome-extension://mopnmbcafieddcagagdcbnhejhlodfdd/index.html"
        self.nftmart_login_url = 'https://app.nftmart.io/'
        self.create_url = 'https://opensea.io/asset/create'

    def polkadot_login(self) -> None:
        try:
            web.driver.get(self.polkadot_login_url)
            print('Login to Polkadot.', end=' ')
            web.driver.refresh()
            web.clickable('//*[@id="root"]/main/div[4]/button')
            web.clickable('//*[@id="root"]/main/div[1]/div/div[2]/div[1]')
            web.clickable('//*[@id="root"]/main/div[1]/div/div[3]/div[4]')
            web.send_keys('//*[@id="root"]/main/div[3]/div[1]/textarea', self.recovery_phrase)
            web.clickable('//*[@id="root"]/main/div[5]/button')

            web.send_keys('//*[@id="root"]/main/div[3]/div/input',self.description)
            web.send_keys('//*[@id="root"]/main/div[4]/div/input',self.password)
            web.send_keys('//*[@id="root"]/main/div[5]/div/input',self.password)

            web.clickable('//*[@id="root"]/main/div[7]/button[2]')

            print(f'{green}Logged to Polkadot.{reset}')
        except Exception:
            print(f'\n{red}Login to Polkadot failed, retrying...{reset}')
            self.polkadot_login()
        
    def nftmart_login(self) -> None:
        try:
            web.driver.get(self.nftmart_login_url)
            print('Login to NFTmart.', end=' ')
            web.window_handles(1)
            web.clickable('//*[@id="root"]/main/div[1]/div[2]/div/button/div[1]')

            web.window_handles(0)
            web.clickable('//*[@id="root"]/header/div/div[5]/div/a')
            web.clickable('//*[@id="root"]/main/div/div/div/div/div[2]/div/div')
            web.clickable('/html/body/div[1]/header/div/div[5]/div/div[1]/img[2]')
            web.clickable('/html/body/div[1]/header/div/div[5]/div/div[2]/section/div[2]/div[4]')
            print(f'{green}Logged to NFTmart.{reset}')
        except Exception:
            print(f'\n{red}Login to NFTmart failed, retrying...{reset}')
            self.nftmart_login()

    def nftmart_select_collection(self) -> None:
        print(f'Find Collection of '+reader.collection+' .', end=' ')
        try:
            web.clickable('//*[@id="root"]/main/div[2]/div[2]/div/div/a[*]/div/p[contains(string(), "{}")]'.format(reader.collection))
            print(f'{green}Find Collection of {reader.collection}.{reset}')
        except Exception:
            print(f'\n{red}Cannot Find Collection of '+reader.collection+' ...{reset}')
    
    def upload_nft(self,number:int) -> bool:
            print(f'Uploading NFT {number+1}/{reader.lists_length}.', end=' ')
            file_base=reader.lists[number]
            web.clickable('//*[@id="root"]/main/div[1]/div/a/button')
            web.send_keys('//*[@id="logoUrl"]', os.path.abspath("Files")+'\\'+file_base["filePath"])
            web.send_keys('//*[@id="name"]', file_base["name"])
            web.clickable('/html/body/div[1]/main/div[2]/form/div[3]/div/div[2]/div[6]/div[1]/div/div/div/div[5]/pre')
            web.send_keys('/html/body/div[1]/main/div[2]/form/div[3]/div/div[2]/div[1]/textarea', file_base["description"])
            
            propertie_items=list(file_base["properties"].items())
            for propertie_item_number in range(len(file_base["properties"])):
                web.send_keys('//*[@id="'+str(propertie_item_number)+'" and @placeholder="property name"]', propertie_items[propertie_item_number][0])
                web.send_keys('//*[@id="'+str(propertie_item_number)+'" and @placeholder="property value"]', propertie_items[propertie_item_number][1])
                if propertie_item_number+1  < len(file_base["properties"]):
                    web.clickable('//*[@id="root"]/main/div[2]/form/p[2]')
            web.clickable('//*[@id="root"]/main/div[2]/form/div[5]/button')
            print(f'{green}Upload Done.{reset}')
            web.window_handles(1)
            web.clickable('//*[@id="root"]/main/div[3]/div[1]/div/input')
            web.send_keys('//*[@id="root"]/main/div[3]/div[1]/div/input',self.password)
            web.clickable('//*[@id="root"]/main/div[3]/button')
            web.window_handles(0)
            # web.clickable('//*[@id="root"]/main/div[3]/div[2]/div[2]/div/div/a/div/div/div[2]/div/p[contains(string(), "{}")]'.format(file_base["name"]))
            # web.clickable('//*[@id="root"]/main/div[1]/div/div[2]/button')
            # web.send_keys('//*[@id="price"]',file_base["price"])
            # web.clickable('//*[@id="deposits"]')
            # web.send_keys('//*[@id="deposits"]',1)
            # web.clickable('//*[@id="accordion-panel-796"]/div[1]/button')
            # web.window_handles(1)
            # web.clickable('//*[@id="root"]/main/div[3]/div[1]/div/input')
            # web.send_keys('//*[@id="root"]/main/div[3]/div[1]/div/input',self.password)
            # web.clickable('//*[@id="root"]/main/div[3]/button')
            # web.window_handles(0)
            # web.driver.get(self.nftmart_login_url)
            # web.clickable('/html/body/div[1]/header/div/div[5]/div/div[1]/img[2]')
            # web.clickable('/html/body/div[1]/header/div/div[5]/div/div[2]/section/div[2]/div[4]')
            


if __name__ == '__main__':
    recovery_phrase = "snake salt entry tribe ethics history economy lecture purse reveal minimum bird"
    reader = Reader("data.json")
    nftmart = NFTmart(recovery_phrase,"PuZaoSi2021","PuZaoSi")
    web = Webdriver()
    nftmart.polkadot_login()
    nftmart.nftmart_login()
    nftmart.nftmart_select_collection()
    for i in range(999):
        nftmart.upload_nft(i)
     

    # for nft_file_number in range(reader.lists_length):

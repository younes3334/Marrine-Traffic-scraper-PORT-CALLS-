import os
# Import the libraries to handle the work
# if the libraries were not installed, they will be installed automatically
# you can remove "#" in line 122 to have headless mode

try:
    import pandas as pd
    import numpy as np
    import openpyxl
    from random import randrange
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    import warnings
    import re
    from selenium import webdriver
except ImportError:
    import pip
    pip.main(['install', '--user', 'selenium'])
    pip.main(['install', '--user', 'webdriver_manager'])
    pip.main(['install', '--user', 'openpyxl'])
    pip.main(['install', '--user', 'pandas'])
    import pandas as pd
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium import webdriver
    import time
    import warnings
    import re

warnings.filterwarnings('ignore')


# Main functions
def get_Marrinetraffic_data(url, driver, wait):

    driver.get(url)
    time.sleep(3)

    # click on the Agree for cockies
    try:
        buttons_agree = driver.find_element_by_class_name("qc-cmp2-summary-buttons").find_elements_by_tag_name("button")[-1]
        buttons_agree.click()
    except:
        pass

    df = pd.DataFrame()

    # we will do a Loop to get through all the pages
    # we will get the data from the page and then we will click on the next page
    # and then we will get the data from the page and then we will click on the next page
    # and so on


    #page_limit = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1s27g5r")))[-1].text
    page_limit = 10
    #int(page_limit.split(' ')[-1])
    print("\nNumber of pages: ", page_limit)

    for i in range(1, page_limit+1):

        ################################################################################
        # Load more data 50 per page
        selector = '#mui-1'
        driver.find_element_by_css_selector(selector).click()
        ActionChains(driver).click(driver.find_element_by_css_selector(selector)).perform()
        time.sleep(1)

        content = driver.find_elements_by_css_selector(".ag-react-container")
        content_text = [x.text for x in content]

        # 1- remove all the ' ' from the list
        content_text2 = [x for x in content_text if x != '']

        element_to_start_with = ['Leg Start Port/anch', 'In Transit Port Calls']
        if( element_to_start_with[1] in content_text2):
            index = content_text2.index(element_to_start_with[1])
        elif( element_to_start_with[0] in content_text2):
            index = content_text2.index(element_to_start_with[0])
        else:
            print('element not found')
        
        content_text1 = content_text2[index+1:]
        #content_text1 = content_text2[7:]

        Vessels = []
        for x in content_text1:
            if x not in ['ARRIVAL', 'DEPARTURE']:
                Vessels.append(x)
            else:
                break
        
        data = content_text1[len(Vessels):]

        list_vessels = []
        for i in range(0, len(data), 9):
            list_vessels.append(data[i:i+9])

        

        if (len(list_vessels) == len(Vessels)):
            all_vessels_info = []
            for i in range(len(list_vessels)):
                all_vessels_info.append([Vessels[i]] + list_vessels[i])
            
            df1 = pd.DataFrame(all_vessels_info, columns = ['Vessel Name', 'Port call Type', 'Port Type', 'Port At call', 'ATA/ATD', 'Origin Port Name', 'Leg Start Port', 'Intransit',"MMSI", "IMO"])
            # concat the two dataframes
            df = pd.concat([df, df1], axis = 0)

        else:
            print('Error in the data')
            return None
    
        # go to the next page
        class_name = 'MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeSmall.MuiButton-containedSizeSmall.MuiButton-disableElevation.MuiButtonBase-root.jss46.css-c33zuv'
        element_1=driver.find_element_by_css_selector(".MuiTablePagination-actions").find_elements_by_class_name(class_name)[1]
        ActionChains(driver).click(element_1).perform()

    ################################################################################

    # drop repeated rows
    #df.drop_duplicates(subset = 'Vessel Name', keep = 'first', inplace = True)

    return df


if __name__ == '__main__':

    print("\nOpening the browser...")
    try:
        # Initilaize selenium
        #PATH = ChromeDriverManager(version='90.0.4430.24').install()
        #service = Service(PATH)
        options = Options()
        options.add_argument('--no-sandbox')
        #options.add_argument('--headless')
        options.add_argument('-disable-gpu')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.24 Safari/537.36"
        )

        #options.add_argument("--disable-popup-blocking")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        d = webdriver.DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'performance': 'ALL'}
        driver = Chrome(options=options, desired_capabilities=d)

        #driver = Chrome(PATH,  options=options,desired_capabilities=d)
        wait = WebDriverWait(driver, 10)
        time.sleep(1)
    except:
        # Initilaize selenium
        PATH = ChromeDriverManager().install()
        service = Service(PATH)
        options = Options()
        options.add_argument('--no-sandbox')
        #options.add_argument('--headless')
        options.add_argument('-disable-gpu')
        driver = Chrome(PATH, options=options)
        wait = WebDriverWait(driver, 10)

    time.sleep(2)
    action = ActionChains(driver)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    print("Browser opened succefully")
    time.sleep(1)

    url = "https://www.marinetraffic.com/en/data/?asset_type=arrivals_departures&columns=shipname,move_type,port_type,port_name,ata_atd,origin_port_name,leg_start_port,intransit,mmsi,imo&ata_atd_betwe"

    data = get_Marrinetraffic_data(url, driver, wait)

    # check if the data under the name : 'Marrinetraffic_data.xlsx' exists, if yes then read it and then concat it with the new data

    if os.path.exists('Marrinetraffic_data.xlsx'):
        df = pd.read_excel('Marrinetraffic_data.xlsx', engine='openpyxl')
        data = pd.concat([df, data], axis=0)
        # drop repeated rows
        data.drop_duplicates(inplace=True)

        data.to_excel('Marrinetraffic_data.xlsx', index=False)
    else:
        # drop repeated rows
        data.drop_duplicates(inplace=True)
        data.to_excel('Marrinetraffic_data.xlsx', index=False)
    print(data)

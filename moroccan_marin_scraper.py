import os
# Import the libraries to handle the work
# if the libraries were not installed, they will be installed automatically
# the "config.py" file should be in the same folder as this script


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
    import config
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
    import config

warnings.filterwarnings('ignore')


# Main functions
def get_Marrinetraffic_data(url, driver, wait):

    driver.get(url)
    time.sleep(3)

    # click on the Agree for cockies
    try:
        buttons_agree = driver.find_element_by_class_name("qc-cmp2-summary-buttons").find_elements_by_tag_name("button")[-1]
        buttons_agree.click()
        print("Cookies handled !")
    except:
        print("cookies not handled !")
        pass

    df = pd.DataFrame()

    # we will do a Loop to get through all the pages
    # we will get the data from the page and then we will click on the next page
    # and then we will get the data from the page and then we will click on the next page
    # and so on

    # Load more data 50 per page
    time.sleep(1)
    selector = '#mui-1'
    driver.find_element_by_css_selector(selector).click()
    ActionChains(driver).click(driver.find_element_by_css_selector(selector)).perform()
    time.sleep(1)

    page_limit = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1s27g5r")))[-1].text
    page_limit = int(page_limit.split(' ')[-1])
    #page_limit = 1
    
    print("\nNumber of pages: ", page_limit)

    for j in range(1, page_limit+1):

        ################################################################################

        content = driver.find_elements_by_css_selector(".ag-react-container")
        content_text = [x.text for x in content]

        # 1- remove all the ' ' from the list
        content_text2 = [x for x in content_text if x != '']
        #print(content_text2)


        # 2- find the element to start with depending on the structure of the page
        element_to_start_with = ['Leg Start Port/anch','Port At Call', 'In Transit Port Calls','Ata/atd']
        if( element_to_start_with[-1] in content_text2):
            index = content_text2.index(element_to_start_with[-1])
        elif( element_to_start_with[1] in content_text2):
            index = content_text2.index(element_to_start_with[1])
        else:
            print('element not found')
        
        content_text1 = content_text2[index+1:]

        """Vessels = []
        for x in content_text1:
            if x not in ['ARRIVAL', 'DEPARTURE']:
                Vessels.append(x)
            else:
                break"""
        
        data = content_text1[:]

        list_vessels = []
        for i in range(0, len(data), 10):
            list_vessels.append(data[i:i + 10])

        if (True):
            all_vessels_info = []
            for i in range(len(list_vessels)):
                all_vessels_info.append(list_vessels[i])

            # create a dataframe from the list of lists of vessels info
            df1 = pd.DataFrame(all_vessels_info,
                               columns=[
                                   'Vessel Name', 'Port call Type',
                                   'Port Type', 'Port At call', 'ATA/ATD',
                                   'Origin Port Name', 'Leg Start Port',
                                   'Intransit', "MMSI", "IMO"
                               ])
            # concat the two dataframes
            df = pd.concat([df, df1], axis=0)
            print(df)
        else:
            print('Error in the data')
            return None
    
        # go to the next page
        try:
            print("Page number: ", j," is done")
            class_name = 'MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeSmall.MuiButton-containedSizeSmall.MuiButton-disableElevation.MuiButtonBase-root.jss46.css-c33zuv'
            element_1=driver.find_element_by_css_selector(".MuiTablePagination-actions").find_elements_by_class_name(class_name)[1]
            ActionChains(driver).click(element_1).perform()
            time.sleep(1)
        except:
            pass

    ################################################################################

    return df


if __name__ == '__main__':

    print("\nOpening the browser...")
    try:
        # Initilaize selenium with all the options
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('-disable-gpu')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.24 Safari/537.36"
        )
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        d = webdriver.DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'performance': 'ALL'}
        driver = Chrome(options=options, desired_capabilities=d)

        driver.maximize_window()
        wait = WebDriverWait(driver, 10)
        time.sleep(1)
    except:
        # Initilaize selenium with all the options
        PATH = ChromeDriverManager().install()
        service = Service(PATH)
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('-disable-gpu')
        driver = Chrome(PATH, options=options)

        driver.maximize_window()
        wait = WebDriverWait(driver, 10)

    time.sleep(2)
    action = ActionChains(driver)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    print("Browser opened succefully")
    time.sleep(1)

    keyword = config.KEYWORD

    url = "https://www.marinetraffic.com/en/data/?asset_type=arrivals_departures&columns=shipname,move_type,port_type,port_name,ata_atd,origin_port_name,leg_start_port,intransit,mmsi,imo"


    if keyword != "":
        url = url+ "&quicksearch|begins|quicksearch=" + keyword
    else:
        pass
  
  
    while(True):
        
        print("Scraping data...")
        # get some random cookies to avoid the bot detection
        driver.get("https://www.google.com/")
        time.sleep(1)

        # Scraping data
        data = get_Marrinetraffic_data(url, driver, wait)

        file_name = config.DATA_FILE_NAME

        # check if the data under the file name exists, if yes then read it and then concat it with the new data

        if os.path.exists(file_name):
            df = pd.read_csv(file_name)
            data = pd.concat([df, data], axis=0)
            # drop repeated rows
            data.drop_duplicates(inplace=True)
            data.to_csv(file_name, index=False)

        else:
            # drop repeated rows
            data.drop_duplicates(inplace=True)
            data.to_csv(file_name, index=False)
        print(data)
        print("\n\tData saved succefully\n")

        # wait for the next scraping
        time.sleep(config.TIME_TO_WAIT)
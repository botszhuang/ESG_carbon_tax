#download chromedriver from https://googlechromelabs.github.io/chrome-for-testing/#stable
#unzip chromedriver-linux64.zip
#python3 -u web_scraping_mof_statistics.py > web_scraping.log 2>&1 &

import random
import sys
import time
import csv
import os
from dotenv import load_dotenv



from datetime import datetime, timezone

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

myUrl="https://web02.mof.gov.tw/njswww/WebMain.aspx?sys=100&funid=defjsptgl"

DOWNLOAD_DIR = []
CHROME_PATH = []


def init_web_driver () :
    
    #service = Service('./chromedriver-linux64/chromedriver')
    service = Service( CHROME_PATH )
    options = webdriver.ChromeOptions()
    #options.add_argument("--start-maximized")

    prefs = {
        "download.default_directory": DOWNLOAD_DIR, # 指定下載目錄
        "download.prompt_for_download": False,      # 關鍵：禁止彈出「另存新檔」視窗
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,               # 避免被安全偵測擋住
        "profile.default_content_settings.popups": 0, # 禁用彈窗
        #-------------------------------------------------------------
        #"download.open_pdf_in_system_reader": False,
        "download.extensions_to_open": "csv"
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--incognito") # 無痕模式
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--headless=new") # 使用新版的無頭模式
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    return driver

def list_all_frame ( driver ):
 
    frames = driver.find_elements(By.TAG_NAME, "frame")
    print(f"Found {len(frames)} frames:\n")

    for i, frame in enumerate(frames, start=1):
        print(f"{i}. name = {frame.get_attribute('name')}")
        print(f"   src  = {frame.get_attribute('src')}")
 
    # end of list_all_frame

def select_dropdown_by_value( target_text , name ):

    time.sleep ( random.uniform ( 1, 3 ) )

    # 1. Find the select element by its name 
    element = wait.until(EC.visibility_of_element_located((By.NAME, name)))

    # 2. Use the Select class to choose the option
    select_obj = Select(element)

    try:
        # 3.Select by visible text
        select_obj.select_by_visible_text( target_text )
        print(f"Success: Set {name} to value '{target_text}'")

    except Exception as e:
        print(f"Error selecting {name} : {e}")
    
    # ===== end of select_dropdown_by_value =====

def switch_to_frame( driver, str_frameName ):
    driver.switch_to.default_content()
    driver.switch_to.frame( str_frameName )
    print(f" Switched to frame: {str_frameName}")
    # ===== endf of switch_to_frame =====

def wait_for_the_checkboxes ( wait ):
    try:
        checkboxes = wait.until(
            EC.presence_of_all_elements_located( ( By.XPATH, "//input[@type='checkbox']" ) )
        )
        print(f"Found {len(checkboxes)} checkboxes")

        clicked = 0

    except:
        print("Cannot find the checkboxes.")
    # ===== end of wait_for_the_checkboxes =====

def click_the_JSbtn ( strJS_clickCheckNode , str0 , driver , wait ):

    try:
        # Target the 'a' tag with the specific javascript link
        the_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//a[@href='javascript:clickCheckNode({strJS_clickCheckNode})']")
        ))
        
        driver.execute_script("arguments[0].click();", the_btn)
        print( f"✅ Clicked {str0} successfully" )

    except Exception as e:
        print(f"Could not click the link {str0} : {e}")
    # ===== end of click_the_JSbtn =====

def click_the_item ( str0 , driver , wait ):

    strXPATH="//a[.//font[contains(text(),'{}')]]".format(str0)

    try:
        # wait for and click the item by visible text
        item = wait.until(EC.element_to_be_clickable(
            (By.XPATH, strXPATH )
        ))
        item.click()

        print(f"Clicked: {str0}")
    except:
        print(f"Can not open the section: {str0}" )
    # ===== end of click_the_item =====

def click_the_query_btn ( driver , wait ):
    
    try:
        query_btn = wait.until(EC.presence_of_element_located((By.NAME, "querybtn")))
        
        # Manually dispatch the mouseup event that the website is looking for
        driver.execute_script("""
            var btn = arguments[0];
            var event = new MouseEvent('mouseup', {
                'view': window,
                'bubbles': true,
                'cancelable': true
            });
            btn.dispatchEvent(event);
        """, query_btn)
        
        print("Forced MouseUp event on Query button.")
    except Exception as e:
        print(f"Error: {e}")
    # ===== end of click_the_click_the_query_btn =====

def get_filename_after_download(download_path, timeout=20):

    start_time = time.time()
    # List files before we start (to avoid old files)
    old_files = set(os.listdir(download_path))

    time.sleep(10)
    
    while ( time.time() - start_time ) < timeout:
        current_files = set(os.listdir(download_path))
        new_files = current_files - old_files
        
        if new_files:
            for f in new_files:
                # Ignore temporary chrome download files
                if not f.endswith('.crdownload') and not f.endswith('.tmp'):
                    return f
    return None

def rename_the_file ( fName , year , month ):

    fName = f"{DOWNLOAD_DIR}/{fName}"
    print ( f"File: {fName}" )
    
    if fName == None :
        return
    
    new_fName = f"{DOWNLOAD_DIR}/mof_statistic_{year}_{month}.csv"
    
    try:
        os.rename( fName , new_fName )
        print(f"✅ File renamed: {fName} --> { new_fName }")
        return new_fName
    
    except Exception as e:
        print(f"Error renaming file: {e}")
        return None
    # ====== end of rename_the_file =====

def get_csv_file( section_str , driver , wait , str_theYear , str_TheM ):

    # Switch to the correct frame
    switch_to_frame ( driver , "qry1" )

    # --------- Click "出口主要國家/地區、主要貨品" ----------
    click_the_item ( section_str , driver , wait )

    # ----------------------------------------------------------------------
    switch_to_frame ( driver , "qry2" )

    #-------------- select the dropdown list -------------------------------
    #--- Start Date ---
    #select_dropdown_by_value("104", "yyf") # Year From
    select_dropdown_by_value( str_theYear, "yyf") # Year From
    select_dropdown_by_value( str_TheM, "mmf")   # Month From

    # --- End Date ---
    #select_dropdown_by_value("114", "yyt") # Year To
    select_dropdown_by_value( str_theYear, "yyt") # Year To
    select_dropdown_by_value( str_TheM, "mmt")   # Month To
    # ----------------------------------------------------------------------
    #select_dropdown_by_value( "(列)統計期　(行)統計項/複分類" , "outkind"  )
    # 找到 outkind 選單
    element = wait.until(EC.visibility_of_element_located((By.NAME, "outkind")))
    select_obj = Select(element)

    # 直接選取第二個選項 (通常索引 0 是總計，索引 1 是分國家)
    select_obj.select_by_index(1) 
    print(f"✅ 已透過索引選取: {select_obj.first_selected_option.text}")
    # ---------------------------------------------------------------------
    select_dropdown_by_value( "統計值"      , "compmode" )
    select_dropdown_by_value( "試算表(CSV)" , "outmode"  )
    select_dropdown_by_value( "月(含年)" , "cycle"  )


    # --------- Wait for checkboxes & click all ----------
    wait_for_the_checkboxes ( wait )

    time.sleep( random.uniform ( 1, 3 ) )
    click_the_JSbtn ( "0" , "國家/地區別 (全選)" , driver , wait )

    time.sleep( random.uniform ( 1, 3 ) )
    click_the_JSbtn ( "75" , "主要貨品別 (全選)" , driver , wait )

    # ----------Click the Query Button -----------------------------------
    time.sleep( random.uniform ( 1, 3 ) )
    click_the_query_btn ( driver , wait )

    # ===== end of get_csv_file =====

if __name__ == "__main__" :

    # Load the variables from .env
    load_dotenv()
    # Access them using os.environ.get
    DOWNLOAD_DIR = os.environ.get('DOWNLOAD_DIR')
    CHROME_PATH = os.environ.get('CHROME_DRIVER_PATH')

    print( DOWNLOAD_DIR )
    print( CHROME_PATH )

    driver = init_web_driver ()
    driver.get( myUrl )
    wait = WebDriverWait(driver, 10)

    list_all_frame ( driver )
    section = "出口主要國家/地區、主要貨品"

    for y in range ( 114 , 103 , -1 ) :
        for m in range ( 1, 13 , 1 ) :

            yearStr  = str( y )
            monthStr = str( m )

            get_csv_file( section , driver , wait , yearStr , monthStr )
            cvsf = get_filename_after_download ( DOWNLOAD_DIR )
            rename_the_file ( cvsf , yearStr , monthStr )
            os.system("pkill -f soffice") # soffice 是 LibreOffice 的進程名稱
            print("✅ shotdown LibreOffice")    




    driver.quit()

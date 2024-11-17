# scapper.py
# 
# Functions that interact with the websites directly, i.e. the driver.
# 
#

import streamlit as st

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

# ---------------------------------------------------------
# Step 1: Given the BLAST's URL for a resulting gene,
#         click the transcriptDNA and take to gene's full
#         information page.
# ---------------------------------------------------------

# ---------------------------------------------------------------
# Purpose: Taking a URL for a gene provided directly from BLAST,
# click the transcript DNA taking you to the gene's information
# page where we can extract the sequence directly. 
# ---------------------------------------------------------------
def clickTranscriptDNA(driver, url):
    # Using on local driver OPEN provided URL (the URL directly from BLAST)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')

    # 1. Open the driver 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
    driver.get(url)

    time.sleep(5) # Can't be shortened

    # 2. Look for transcript DNA in the page
    element = driver.find_element(By.XPATH, '//*[@id="track_Transcripts"]/canvas')

    # 3. Click on the transcript DNA & take to gene's information page
    element.click()
    st.write(f'Step 1/3 (clickTranscriptDNA): Transcript clicked with driver {driver}')

    # 4. Return the gene's information page (current url)
    return driver.current_url


# ---------------------------------------------------------
# Step 2: From the gene's information page, extract inform-
#         iation: gene name, CDS. (Could add more).
# ---------------------------------------------------------

# ---------------------------------------------------------------
# Purpose: Given a gene information page, extract the gene name
#          from its position on the page. 
# ---------------------------------------------------------------
def extractGeneNameFromGeneURL(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')

    # 1. Open the driver 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
    st.write(f"Step 2/3 (extractGeneName): Driver still active {driver}")
    
    driver.get(url)
    
    # 2. Wait & find gene name from position on website
    element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/dl/dd[1]'))
    )
    st.write(f"Step 2/3 (extractGeneName): Name found {element.text}")
    name = element.text

    # 3. Return the direct name information
    print(name.split("\n"))  # Splits into an array of elements each split where there was an '\n', in this case [header], [sequence]
    return name.split("\n")[0]

def extractCDSFromGeneURL(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')
    
    # 1. Open driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
    st.write(f"Step 3/3 (extractCDSFromGeneURL): Driver open - DEBUG:DRIVER:{driver}")
    driver.get(url)

    # 2. For the CDS sequence, click the BLAST search in Phytozome button 
    #      this puts the CDS sequence in a continuous string format that we 
    #      can extract directly.
    element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[4]/div[4]/label/div/div/a/button/span'))
    )
    element.click()
    
    # 3. Extract the CDS once the page has loaded.
    element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div/div/form/fieldset/textarea'))
    )
    sequence = element.text

    # 4. Return the second part of the text -- the sequence
    # If we wanted the full FASTA header included -- it would be the full sequence variable. 
    return sequence.split("\n")[1]
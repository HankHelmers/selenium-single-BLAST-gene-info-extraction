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
import time

# Inputs:
#   - driver: 
# 
# Purpose: Taking a URL for a gene provided directly from BLAST,
# click the transcript DNA taking you to the gene's information
# page where we can extract the sequence directly. 
def clickTranscriptDNA(driver, url):
    # Using on local driver OPEN provided URL (the URL directly from BLAST)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
    # st.write(f"clickTranscriptDNA: DRIVER--{driver}-- OPENED.")
    driver.get(url)

    time.sleep(5)

    # Look for transcript DNA in the page
    element = driver.find_element(By.XPATH, '//*[@id="track_Transcripts"]/canvas')

    # Click on the transcript DNA & take to gene's information page
    element.click()

    st.write(f'Step 1/3 (clickTranscriptDNA): Transcript clicked with driver {driver}')

    # Return the gene's information page (current url)
    return driver.current_url
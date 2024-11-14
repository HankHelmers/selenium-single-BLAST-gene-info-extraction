import streamlit as st

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

from scrapper import *


# ------------- Settings for Pages -----------
st.set_page_config(layout="wide")

# Keep text only
def get_website_content(url):
    driver = None
    try:
        # Using on Local
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1200')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
        st.write(f"DEBUG:DRIVER:{driver}")
        driver.get(url)
        time.sleep(5)
        html_doc = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup.get_text()
    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None: driver.quit()
    return None

# Step 1: Given the BLAST's URL for a resulting gene,
#         click the transcriptDNA and take to gene's full
#         infromation page.

# Purpose: Interface with the driver & run the step 1 of extraction. 
# 
# Input:
# - url: BLAST's outputted URL for a matched gene 
#
# Output:
# - newUrl: BLAST URL's gene's full information URL 

def callClickTranscriptDNA(url):
    driver = None
    try:
        return clickTranscriptDNA(driver, url)            # Defined in scrapper.py
    except Exception as e:
        st.write(f"Step 1/3 (callClickTranscriptDNA): DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None: driver.quit()
    return None
    

def getGeneName(url):
    driver = None
    try:
        # Using on Local
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1200')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
        st.write(f"DEBUG:DRIVER:{driver}")
        driver.get(url)

        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/dl/dd[1]'))
        )
        print(element.text)

        name = element.text
        print(name.split("\n"))  # Splits into an array of elements each split where there was an '\n', in this case [header], [sequence]
        return name.split("\n")[0]


    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None: driver.quit()
    return None

def getCDS(url):
    driver = None
    try:
        # Using on Local
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1200')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
        st.write(f"DEBUG:DRIVER:{driver}")
        driver.get(url)

        ## Click button to go to Blast
        element = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[4]/div[4]/label/div/div/a/button/span'))
        )
        element.click()
        
        element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div/div/form/fieldset/textarea'))
        )
        sequence = element.text
        return sequence.split("\n")[1]

    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None: driver.quit()
    return None


# ---------------- Page & UI/UX Components ------------------------
def main_sidebar():
    # 1.Vertical Menu
    st.header("Single BLAST URL GENE INFO (Name & CDS) Extraction")
    site_extraction_page()


def site_extraction_page():
    SAMPLE_URL = "https://phytozome-next.jgi.doe.gov/jbrowse/index.html?data=genomes%2FTaestivumcv_ChineseSpring_v2_1&loc=Chr2B%3A646472438..646474664&tracks=UserBlastResults%2CTranscripts%2CAlt_Transcripts%2CPASA_assembly%2CBlastx_protein&highlight="
    
    # Input text field 
    url = st.text_input(label="URL", placeholder="https://example.com", value=SAMPLE_URL)

    # Button to begin
    clicked = st.button("Extract from URL",type="primary")
    if clicked:
        # Container to update & write to 
        with st.container(border=True):
            with st.spinner("Loading page website..."):
                nextUrl = callClickTranscriptDNA(url)
                st.write(nextUrl)

                geneName = getGeneName(nextUrl)
                st.write(geneName)

                cdsText = getCDS(nextUrl)
                st.write(cdsText)


# Starting method
if __name__ == "__main__":
    main_sidebar()

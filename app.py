# # app.py
# #
# # main streamlit file for managing the app page
# #

# import streamlit as st

# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.service import Service

# import time
# from concurrent.futures import ThreadPoolExecutor

# from scrapper import *


# # ------------- Settings for Pages -----------
# st.set_page_config(layout="wide")

# # ---------------------------------------------------------
# # Step 1: Given the BLAST's URL for a resulting gene,
# #         click the transcriptDNA and take to gene's full
# #         information page.
# # ---------------------------------------------------------

# # Purpose: Interface with the driver & run the step 1 of extraction. 
# # 
# # Input:
# # - url: BLAST's outputted URL for a matched gene 
# #
# # Output:
# # - newUrl: BLAST URL's gene's full information URL 
# def callClickTranscriptDNA(url):
#     driver = None
#     try:
#         return clickTranscriptDNA(driver, url)            # Defined in scrapper.py
#     except Exception as e:
#         st.write(f"Step 1/3 (callClickTranscriptDNA): DEBUG:INIT_DRIVER:ERROR:{e}")
#     finally:
#         if driver is not None: driver.quit()
#     return None

# # ---------------------------------------------------------
# # Step 2: From the gene's information page, extract inform-
# #         iation: gene name, CDS. (Could add more).
# # ---------------------------------------------------------

# def callExtractGeneName(url):
#     driver = None
#     try:
#         return extractGeneNameFromGeneURL(url)
#     except Exception as e:
#         st.write(f"Step 2/3 (callExtractGeneName): DEBUG:INIT_DRIVER:ERROR:{e}")
#     finally:
#         if driver is not None: driver.quit()
#     return None

# def callExtractCDS(url):
#     driver = None
#     try:
#         return extractCDSFromGeneURL(url)
#     except Exception as e:
#         st.write(f"Step 3/3 (callExtractCDS):DEBUG:INIT_DRIVER:ERROR:{e}")
#     finally:
#         if driver is not None: driver.quit()
#     return None


# # ---------------- Page & UI/UX Components ------------------------
# def main_sidebar():
#     # 1.Vertical Menu
#     st.header("Single BLAST URL GENE INFO (Name & CDS) Extraction")
#     site_extraction_page()


# def site_extraction_page():
#     SAMPLE_URL = "https://phytozome-next.jgi.doe.gov/jbrowse/index.html?data=genomes%2FTaestivumcv_ChineseSpring_v2_1&loc=Chr2B%3A646472438..646474664&tracks=UserBlastResults%2CTranscripts%2CAlt_Transcripts%2CPASA_assembly%2CBlastx_protein&highlight="
    
#     # Input text field 
#     url = st.text_input(label="URL", placeholder="https://example.com", value=SAMPLE_URL)

#     # Button to begin
#     clicked = st.button("Extract from URL",type="primary")
#     if clicked:
#         # Container to update & write to 
#         with st.container(border=True):
#             with st.spinner("Loading page website..."):
#                 startScraping(url)

# def startScraping(url):
#     start_time = time.time()
#     st.write("Timer started...")

#     # Step 1: click Transcript DNA
#     nextUrl = callClickTranscriptDNA(url)
#     st.write(nextUrl)

#     # Step 2 & 3: Extract info -- gene name & cds (concurrently)
#     def fetch_gene_name():
#         return callExtractGeneName(nextUrl)

#     def fetch_cds():
#         return callExtractCDS(nextUrl)

#     with ThreadPoolExecutor() as executor:
#         future_gene = executor.submit(fetch_gene_name)
#         future_cds = executor.submit(fetch_cds)

#         geneName = future_gene.result()
#         cdsText = future_cds.result()

#     st.write(geneName)
#     st.write(cdsText)

#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     st.write(f"Time elapsed... {elapsed_time:.2f} seconds.")

# #
# # 27.48684072494507
# # 27.79285764694214
# # 26.825424671173096
# # 27.195629358291626
# # 


# # Starting method
# if __name__ == "__main__":
#     main_sidebar()

import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time
from concurrent.futures import ThreadPoolExecutor

# Streamlit Page Settings
st.set_page_config(layout="wide")

# Selenium Functions
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def clickTranscriptDNA(driver, url):
    try:
        driver.get(url)
        time.sleep(5)  # Required for the page to load
        element = driver.find_element(By.XPATH, '//*[@id="track_Transcripts"]/canvas')
        element.click()
        st.write("Step 1/3: Transcript clicked.")
        return driver.current_url
    except Exception as e:
        st.write(f"Error in clickTranscriptDNA: {e}")
        return None

def extractGeneNameFromGeneURL(driver, url):
    try:
        driver.get(url)
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/dl/dd[1]'))
        )
        st.write("Step 2/3: Gene name extracted.")
        return element.text.split("\n")[0]
    except Exception as e:
        st.write(f"Error in extractGeneNameFromGeneURL: {e}")
        return None

def extractCDSFromGeneURL(driver, url):
    try:
        driver.get(url)
        element = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[4]/div[4]/label/div/div/a/button/span'))
        )
        element.click()
        sequence_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div/div/div/form/fieldset/textarea'))
        )
        st.write("Step 3/3: CDS sequence extracted.")
        return sequence_element.text.split("\n")[1]
    except Exception as e:
        st.write(f"Error in extractCDSFromGeneURL: {e}")
        return None

# Wrapper Functions for Calling Steps
def callClickTranscriptDNA(driver, url):
    return clickTranscriptDNA(driver, url)

def callExtractGeneName(driver, url):
    return extractGeneNameFromGeneURL(driver, url)

def callExtractCDS(driver, url):
    return extractCDSFromGeneURL(driver, url)

# Main Scraping Logic
def scrapeSingleURL(url):
    driver = init_driver()
    try:
        start_time = time.time()
        st.write("Timer started...")

        # Step 1: Click Transcript DNA
        nextUrl = callClickTranscriptDNA(driver, url)
        if not nextUrl:
            st.write("Failed at Step 1: Cannot proceed.")
            return

        # Step 2 & 3: Extract gene name and CDS concurrently
        geneName, cdsText = None, None
        try:
            with ThreadPoolExecutor() as executor:
                future_gene = executor.submit(callExtractGeneName, driver, nextUrl)
                future_cds = executor.submit(callExtractCDS, driver, nextUrl)
                geneName = future_gene.result()
                cdsText = future_cds.result()
        except Exception as e:
            st.write(f"Error during concurrent execution: {e}")

        st.write(f"Gene Name: {geneName or 'Not found'}")
        st.write(f"CDS Text: {cdsText or 'Not found'}")

        end_time = time.time()
        elapsed_time = end_time - start_time
        st.write(f"Time elapsed: {elapsed_time:.2f} seconds.")
    finally:
        driver.quit()

# Streamlit UI
def site_extraction_page():
    SAMPLE_URL = "https://phytozome-next.jgi.doe.gov/jbrowse/index.html?data=genomes%2FTaestivumcv_ChineseSpring_v2_1&loc=Chr2B%3A646472438..646474664&tracks=UserBlastResults%2CTranscripts%2CAlt_Transcripts%2CPASA_assembly%2CBlastx_protein&highlight="

    # Input URL
    url = st.text_input(label="Enter BLAST URL", placeholder="https://example.com", value=SAMPLE_URL)

    # Extract Button
    if st.button("Extract from URL", type="primary"):
        with st.spinner("Processing..."):
            scrapeSingleURL(url)

# Streamlit App Entry Point
if __name__ == "__main__":
    st.title("BLAST Gene Information Extractor")
    site_extraction_page()

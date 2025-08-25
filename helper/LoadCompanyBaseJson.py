import json
import os 

COMPANY_DATA_CACHE= {}

COMPANY_SECTION_DATA = {}


# Global variable to store the loaded configuration
SECTION_CARD_CONFIGS = None

def load_section_configs():
    global SECTION_CARD_CONFIGS
    if (
        SECTION_CARD_CONFIGS is None
    ):  # Only load the configuration if it's not already loaded
        with open("config/SectionComponents.json", "r") as file:
            SECTION_CARD_CONFIGS = json.load(file)


def load_company_data():
    """
    Load all company base component files once and store in cache by CompanyId.
    """
    config_file: str = "database/CompanyModel.json" 

    global COMPANY_DATA_CACHE

    with open(config_file, "r") as f:
        companies = json.load(f)

    for company in companies:

        company_id = company["CompanyId"]

        COMPANY_DATA_CACHE[company_id] = json.load(company)
       


# load_section_configs()
load_company_data()


# Optionally, provide a function to refresh the configuration if needed
def load_section_config(companyId:int):

    if companyId is not  COMPANY_SECTION_DATA:

        data = COMPANY_DATA_CACHE.get(companyId)
        file_path = data['FilePath']

        global SECTION_CARD_CONFIGS
        with open(file_path, "r") as file:
            data = SECTION_CARD_CONFIGS = json.load(file)

        COMPANY_SECTION_DATA[companyId] = data

    return COMPANY_SECTION_DATA[companyId]

        

with open("config/FileOutputTest.json", "r") as f:
    financialDataTest = json.load(f)


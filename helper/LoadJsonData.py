# financial_data_loader.py
import json

# Global variable to store the loaded configuration
SECTION_CARD_CONFIGS = None


def load_section_configs():
    global SECTION_CARD_CONFIGS
    if (
        SECTION_CARD_CONFIGS is None
    ):  # Only load the configuration if it's not already loaded
        with open("config/SectionComponents.json", "r") as file:
            SECTION_CARD_CONFIGS = json.load(file)


load_section_configs()


# Optionally, provide a function to refresh the configuration if needed
def reload_section_configs():
    global SECTION_CARD_CONFIGS
    with open("section_card_configs.json", "r") as file:
        SECTION_CARD_CONFIGS = json.load(file)


with open("config/FileOutput.json", "r") as f:
    financialData = json.load(f)


with open("config/FileOutputTest.json", "r") as f:
    financialDataTest = json.load(f)


# import json
# from pathlib import Path

# # === File Paths ===
# CONFIG_DIR = Path("config")
# SECTION_CONFIG_PATH = CONFIG_DIR / "SectionComponents.json"
# FILE_OUTPUT_PATH = CONFIG_DIR / "FileOutput.json"
# FILE_OUTPUT_TEST_PATH = CONFIG_DIR / "FileOutputTest.json"

# # === Global variables ===
# SECTION_CARD_CONFIGS = None
# FINANCIAL_DATA = None
# financialDataTest = None


# # === Utility: Load JSON File ===
# def load_json_file(path: Path):
#     try:
#         with path.open("r", encoding="utf-8") as file:
#             return json.load(file)
#     except FileNotFoundError:
#         print(f"File not found: {path}")
#         return {}
#     except json.JSONDecodeError:
#         print(f"Error decoding JSON in file: {path}")
#         return {}


# # === Loaders ===
# def load_section_configs():
#     global SECTION_CARD_CONFIGS
#     if SECTION_CARD_CONFIGS is None:
#         SECTION_CARD_CONFIGS = load_json_file(SECTION_CONFIG_PATH)


# def reload_section_configs():
#     global SECTION_CARD_CONFIGS
#     SECTION_CARD_CONFIGS = load_json_file(SECTION_CONFIG_PATH)


# def load_financial_data():
#     global FINANCIAL_DATA, FINANCIAL_DATA_TEST
#     FINANCIAL_DATA = load_json_file(FILE_OUTPUT_PATH)
#     FINANCIAL_DATA_TEST = load_json_file(FILE_OUTPUT_TEST_PATH)


# # === Initial load ===
# load_section_configs()
# load_financial_data()

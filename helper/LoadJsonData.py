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


with open("config/FileOutputTest.json", "r") as f:
    financialDataTest = json.load(f)

# financialDataTest = jsonData["Financial Data"]

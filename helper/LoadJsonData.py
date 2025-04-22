# financial_data_loader.py
import json

with open("config/FileOutput.json", "r") as f:
    financialData = json.load(f)


with open("config/FileOutputTest.json", "r") as f:
    financialDataTest = json.load(f)

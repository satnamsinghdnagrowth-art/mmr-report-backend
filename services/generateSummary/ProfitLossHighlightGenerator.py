from core.models.base.ResultModel import Result
from datetime import datetime
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

def generateProfitLossHighlights(data):
    try:
        prompt = f"""
            Following is the data of financial Statements {data}, you have to generate the good executive summary for the financial report.

            Rules:
            1. Generate summary for the Revenue, Gross Profit ,   Operating Expenses , Earnings Before Interest & Tax.
            2. Include YTD for each point.
            3. No need to genrate the table format.
            4. I need the points based on current and prior period comparison .Give in text base executive summry.
            5. generate descriptive points based on given input. 
            6. Generate one point for the current and prior period comparison and and one point for the YTD value.
            7. No need to write the more professional language , use simple words like increase , decrease no need to use its synonyms.
            8. Give me response in the HTML, inline CSS form and highlight the important metrics.
            9. Use <br> tags for new lines (no newline characters like \n).
            
            Example : 

            Executive Summary
            • Revenue of $13,029, a decrease of 84% or $69k against the last month of $81,551, driven by a decrease in
            E-commerce, Royalty and Services revenue.

                YTD actuals of $225,943.

            • Gross Margin of -103.88%, a decrease of 195% against the last month of 91.33%, driven by a decrease in Revenue
            Generation and an increase in Cost of Sales (COGS E-commerce (DSMP), Supplies & materials - COGS and Printing
            Materials).
            
                YTD actuals of 14.42%.
        """

        client = Groq(api_key=API_KEY)
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in Senior Fiancial Analyst .",
                },
                {"role": "user", "content": prompt},
            ],
        )
        response = completion.choices[0].message.content.strip()

        return Result(Data=response, Status=1, Message="Success")

    except Exception as ex:
        message = f"Error occurred in retriveDataRange: {ex}"
        print(f"{datetime.now()} {message}")
        return Result(Status=0, Message=message)

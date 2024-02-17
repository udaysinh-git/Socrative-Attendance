# here we will add the function that will go and add attendance to socrative website

import time
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
from utils.mongo_utils import get_attendance_api_key, get_all_attendance_prns
import concurrent.futures
import asyncio

student_website = "https://b.socrative.com/login/student/"


async def get_api_key(prn):
    print("in get_api_key")
    return await get_attendance_api_key(prn)


async def get_answer(prn, question):
    print("in get_answer")
    key = await get_api_key(prn)
    print("awaiting key")
    client = OpenAI(api_key=key)
    print("got key")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a educational bot that provides answer in 20-40 words and more accurate and reliable answers.",
                },
                {
                    "role": "user",
                    "content": f"{str(question)}",
                },
            ],
        )
        print("got response")
        return response.choices[0].message.content
    except:
        print("Error occured! at get_answer")
        # create an error telling api key is wrong
        return False


async def socrative(room_id, prn):
    driver = webdriver.Chrome()
    print("1")
    wait = WebDriverWait(driver, 10)
    print("2")
    driver.get(student_website)
    time.sleep(5)
    try:
        # find the input box for room number
        room_number = driver.find_element(By.ID, "studentRoomName")
        room_number.send_keys(f"{room_id.capitalize()}")
        # logging in
        room_button = driver.find_element(
            By.XPATH, "/html/body/div/div/div[2]/div/div[1]/div[3]/button"
        )
        room_button.click()
        print("Entered Room")
        time.sleep(1)
        while True:
            try:
                student_name = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div[3]/div/div/div/div/span/div/input",
                        )
                    )
                )
                break
            except:
                print("Student name not found")
                driver.close()
                await socrative(room_id, prn)
        student_name.send_keys(f"{prn}")
        driver.find_element(By.ID, "submit-name-button").click()
        print("socrative at loop")
        while True:
            try:
                print("Trying to get question")
                question = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "/html/body/div[1]/div[3]/div/div/div[2]/div/div/div/div[1]/div/div/pre",
                        )
                    )
                )

                break
            except:
                print("Question not found refreshing page")
                driver.refresh()
        print("Question found")
        answer_sheet = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[3]/div/div/div[2]/div/div/div/div[2]/textarea",
        )
        print("Answer sheet found")
        answer = await get_answer(prn, question.text)
        answer_sheet.send_keys(f"{answer}")
        print("Answer sent")
        time.sleep(3)
        submit_button = driver.find_element(By.ID, "submit-button")
        submit_button.click()
        time.sleep(3)
        driver.close()
        return True
    except:
        driver.close()
        print("Error occured! at socrative_attendance.py")
        return False


async def mark_attendance(room_id):
    print("Entered the mark attendane function")
    prns = await get_all_attendance_prns()
    print("Marking attendance for these prns : ", prns)
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = [socrative(room_id, prn) for prn in prns]
            responses = await asyncio.gather(*tasks)
            for response in responses:
                print(response)
        return "Attendance Marked!"
    except:
        return "Error Occured!"

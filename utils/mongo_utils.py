## here i will create a code that will store , update , delete the data from the database at mongodb

import motor.motor_asyncio
import os
import asyncio
import pytz, platform, psutil, discordmongo
import dotenv

# mongo_connect
dotenv.load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

# connect to mongo db database
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
db = client["Chotu"]


def get_collection(collection_name: str):
    return db[collection_name]


## a function to store username , apikey and prn number in the database of the student , if prn or username exists return false else add the prn to database and return true
async def add_user(user_id: int, apikey: str, prn: int, email: str = None):
    collection = get_collection("students")
    if email == None:
        email = 0
    await collection.insert_one(
        {
            "_id": user_id,
            "apikey": apikey,
            "prn": int(prn),
            "email": email,
        }
    )
    return True


async def get_user(user_id: int):
    # using username get the prn and apikey
    collection = get_collection("students")
    info = await collection.find_one({"_id": user_id})
    return info


async def update_apikey(user_id: int, apikey: str):
    collection = get_collection("students")
    await collection.update_one({"_id": user_id}, {"$set": {"apikey": apikey}})
    return True


async def check_user_exists(user_id: int):
    collection = get_collection("students")
    info = await collection.find_one({"_id": user_id})
    if info == None:
        return False
    else:
        return True


async def attendance_add(user_id: int):
    collection = get_collection("attendance")
    students = get_collection("students")
    try:
        info = await students.find_one({"_id": user_id})
        # get the prn of the student
        prn = info["prn"]
        api_key = info["apikey"]
    except:
        return False
    if await collection.find_one({"_id": int(prn)}) == None:
        await collection.insert_one({"_id": int(prn), "api_key": api_key})
        return True
    else:
        return False


async def attendance_remove(user_id: int):
    collection = get_collection("attendance")
    await collection.delete_one({"_id": user_id})
    return True


async def get_attendance_api_key(prn):
    print("getting api key")
    collection = get_collection("attendance")
    print("got collection")
    print(type(prn))
    info = await collection.find_one({"_id": int(prn)})
    print("got info")
    print(info)
    return info["api_key"]


async def get_all_attendance_prns():
    print("getting all prns")
    collection = get_collection("attendance")
    print("got collection")
    list = await collection.find().to_list(length=None)
    print("got list")
    for i in range(len(list)):
        list[i] = int(list[i]["_id"])
    print("Returning List")
    return list

import motor.motor_asyncio
import os

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGODB_URL"))
    db_prediction_mechanism = client["prediction_mechanism"]
except Exception as e:
    print(e)
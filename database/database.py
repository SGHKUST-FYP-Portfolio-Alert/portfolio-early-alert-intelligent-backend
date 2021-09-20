import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://analytics:71mpmU8Lw5ngKhe6@cluster0.lln5s.mongodb.net/"
)

database = client['portfolio_alert']

demo_collection = database.get_collection('demo')

async def retrieve_demo():
    demos = []
    async for demo in demo_collection.find():
        demos.append(demo)
    return demos

async def add_demo(demo_data: dict):
    await demo_collection.insert_one(demo_data)
    return
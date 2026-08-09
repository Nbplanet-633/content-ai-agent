from services.mongo_service import client, db


try:
    client.admin.command("ping")

    print("===== MONGODB TEST =====")
    print("MongoDB connection successful!")
    print(f"Database: {db.name}")

except Exception as error:
    print("===== MONGODB ERROR =====")
    print(type(error).__name__)
    print(error)
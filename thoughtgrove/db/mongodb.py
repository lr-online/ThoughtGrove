from motor.motor_asyncio import AsyncIOMotorClient
from thoughtgrove.core.config import get_settings

settings = get_settings()

class MongoDB:
    client: AsyncIOMotorClient = None
    
    async def connect(self):
        self.client = AsyncIOMotorClient(settings.mongodb_url)
        
    async def close(self):
        if self.client:
            self.client.close()
            
    @property
    def db(self):
        return self.client[settings.mongodb_db_name]
        
    def get_database(self):
        return self.db

mongodb = MongoDB() 
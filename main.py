from fastapi import FastAPI

from database import Database
from models.lookup_mac_to_vendor import LookupMacToVendorRequest, LookupMacToVendorResponse
from repositories import mac_lookups
from services.mac_lookup_app_service import MacLookupAppService

database = Database("storage.db")
mac_lookup_app = MacLookupAppService(database)
app = FastAPI()


@app.on_event("startup")
async def startup():
    # Prepare a DB structure on startup
    connection = database.connect()
    mac_lookups.create_table_if_not_exists(connection)
    connection.commit()
    connection.close()

    # Start the one background task
    mac_lookup_app.launch()


@app.post("/lookup/mac-to-vendor")
async def lookup_mac_to_vendor(request: LookupMacToVendorRequest) -> LookupMacToVendorResponse:
    connection = database.connect()
    result = mac_lookups.get(connection, request.mac_address)
    connection.close()

    if result is not None and len(result) > 0:
        return LookupMacToVendorResponse.succeed(result)
    else:
        return LookupMacToVendorResponse.failed()

from pydantic import BaseModel
from pydantic.schema import Optional


class LookupMacToVendorRequest(BaseModel):

    mac_address: str


class LookupMacToVendorResponse(BaseModel):

    class Item(BaseModel):
        mac_prefix: str
        vendor_name: str

    is_success: bool
    items: Optional[list[Item]]

    @staticmethod
    def succeed(items: [(str, str)]):
        return LookupMacToVendorResponse(
            is_success=True,
            items=list(map(lambda x: LookupMacToVendorResponse.Item(mac_prefix=x[0], vendor_name=x[1]), items))
        )

    @staticmethod
    def failed():
        return LookupMacToVendorResponse(is_success=False)

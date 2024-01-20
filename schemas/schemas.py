from pydantic import BaseModel, Field
from uuid import uuid4
from services.currency_exchange import CurrencyConverter
import constants


class Advertisement(BaseModel):
    phone: str = Field(examples=['+380680000000'])
    price: float = Field(examples=['10000.00'])
    manufacturer: str = Field(examples=['Toyota'])
    model: str = Field(examples=['Camry'])
    year: int = Field(ge=2010, examples=['2010'])
    description: str = Field(min_length=50, max_length=300)
    additional_details: list[constants.CHARACTERISTICS] = Field(default=[], max_items=5)
    images: list[str] = Field(default=[], max_items=5)


class SavedAdvertisement(Advertisement):
    uuid: str = str(uuid4())
    price_in_uah: float = None

    def __init__(self, **data):
        super().__init__(**data)
        currency_converter = CurrencyConverter()
        self.price_in_uah = currency_converter.convert(amount=self.price, from_currency=constants.USD)

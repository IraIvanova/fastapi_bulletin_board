from pydantic import BaseModel, Field
from uuid import uuid4

import constants


class Advertisement(BaseModel):
    phone: str
    price: float
    images: list = []
    manufacturer: str
    model: str
    year: int = Field(ge=2010)
    description: str = Field(min_length=50, max_length=300)
    additional_details: list[constants.CHARACTERISTICS] = Field(default=[], max_items=5)


class SavedAdvertisement(Advertisement):
    uuid: str = str(uuid4())
    success: bool = True
    priceInUah: float = None

# можемо розмістити оголошення -
# маємо вказати номер телефону, ціну в доларах США, список урлів з фотографіями авто
# (не менше 2-х, не більше 10), марку авто, модель авто, рік випуску (ціле число, не менше 2010), список додаткових опцій
# (Enum, може бути пустим), опис авто (не більше 300 символів, не менше 50)
# -> у відповідь отримуємо отримуємо словник з ключами: success: True,
# номер оголошення в системі (uuid),
# ціну даного авто в гривнях по комерційному курсу будь-якого комерційного банку (чи ваше джерело), ціна зберігається в доларах,
# інформація в гривнях оновлюється і є інформативною на час запиту, статус 201.
# Номер оголошення показується лише один раз при створенні,
# надалі це прихована інформація (вважаємо, що тільки автор буде його знати і таким чином керувати оголошенням).
# Марку та модель привести до верхнього регістру, при наявності пробілів на початку чи в кінці текстових даних їх потрібно обрізати
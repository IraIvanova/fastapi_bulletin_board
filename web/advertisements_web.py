from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import constants
import constants as c
from schemas.schemas import Advertisement, SavedAdvertisement
from services.currency_exchange import CurrencyConverter
from storage import storage
from datetime import datetime

templates = Jinja2Templates(directory='templates')

router = APIRouter(
    prefix='',
    tags=['WEB', 'Advertisements'],
)


@router.get('/')
def get_advertisements(request: Request, search: str = ''):
    currency_converter = CurrencyConverter()
    currencies_exchange_rate = currency_converter.get_main_currencies_exchange_rate([c.EUR, c.USD, c.PLN])

    ads = storage.get_list(search_string=search, limit=100)
    context = {
        'request': request,
        'ads': ads,
        'search': search,
        'currencies_exchange_rate': currencies_exchange_rate,
        'today_date': datetime.today().strftime('%Y-%m-%d'),
        'available_currencies': currency_converter.get_available_currencies_list()
    }

    return templates.TemplateResponse('index.html', context=context)


@router.get('/show-advertisement-form/{uuid}')
def show_create_or_update_form(request: Request, uuid: str):
    ad = storage.get_one({'uuid': uuid})

    context = {
        'request': request
    }

    if uuid != constants.CREATE_FORM and ad is None:
        return templates.TemplateResponse('error404.html', context=context)
    form_fields = {
        'phone': {'type': 'tel', 'placeholder': 'Enter phone number', 'label': 'Phone',
                  'value': ad['phone'] if ad else ''},
        'price': {'type': 'number', 'placeholder': 'Enter price', 'label': 'Price',
                  'value': ad['price'] if ad else ''},
        'manufacturer': {'type': 'text', 'placeholder': 'Enter manufacturer name', 'label': 'Manufacturer',
                         'value': ad['manufacturer'] if ad else ''},
        'model': {'type': 'text', 'placeholder': 'Enter model name', 'label': 'Model',
                  'value': ad['model'] if ad else ''},
        'year': {'type': 'number', 'placeholder': 'Enter year of manufacture', 'label': 'Year',
                 'value': ad['year'] if ad else ''},
        'description': {'type': 'text', 'placeholder': 'Enter description', 'label': 'Description',
                        'value': ad['description'] if ad else ''},
        'additional_details': {'type': 'checkbox', 'placeholder': 'Enter additional details',
                               'label': 'Additional details', 'value': ad['additional_details'] if ad else '',
                               'options': [option.value for option in constants.CHARACTERISTICS]},
        'images': {'type': 'text', 'placeholder': 'Insert images URLs separated by commas', 'label': 'Images'}
    }

    context['form_fields'] = form_fields
    context['type'] = constants.EDIT_FORM if ad else constants.CREATE_FORM
    context['ad'] = ad

    return templates.TemplateResponse('show_create_form.html', context=context)


@router.get('/show/{uuid}')
def show_advertisement(request: Request, uuid: str):
    advertisement = storage.get_one({'uuid': uuid})
    context = {
        'request': request
    }

    if advertisement is None:
        return templates.TemplateResponse('error404.html', context=context)

    advertisement_info = SavedAdvertisement(**advertisement)
    context['ad'] = advertisement_info

    return (templates.TemplateResponse('show.html', context=context))


@router.post('/update/{uuid}')
def update(advertisement: Advertisement, uuid: str):
    storage.update({'uuid': uuid}, advertisement.model_dump())
    return {
        'url': f'/show/{uuid}',
        'msg': f'<h4>Your advertisement was successfully updated!</h4>'
    }


@router.post('/create')
def create(advertisement: Advertisement):
    advertisement.model = advertisement.model.strip().upper()
    advertisement.manufacturer = advertisement.manufacturer.strip().upper()
    saved_advertisement = storage.create(advertisement.model_dump())
    return {
        'url': '/',
        'msg': f'<span>Your advertisement</span><br><span class="text-decoration-underline">#{saved_advertisement["uuid"]}<br> <span> successfully created!</span>'
    }


@router.get('/delete/{uuid}')
def delete(uuid: str):
    storage.delete({'uuid': uuid})
    return RedirectResponse('/', status_code=301)


@router.post('/convert-currencies')
def convert_currencies(data: dict) -> float:
    currency_converter = CurrencyConverter()
    return currency_converter.convert(float(data['amount']), data['from'], data['to'])

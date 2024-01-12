from fastapi import APIRouter, Request, Form, Depends, Body
from fastapi.templating import Jinja2Templates
from schemas.advertisement import Advertisement, SavedAdvertisement
from services.currency_exchange import CurrencyConverter
from storage import storage

templates = Jinja2Templates(directory='templates')

router = APIRouter(
    prefix='',
    tags=['WEB', 'Advertisements'],
)


@router.get('/')
def get_advertisements(request: Request, search: str = ''):
    # currency_converter = CurrencyConverter()
    # uah = currency_converter.convert(1, 'USD', 'UAH')
    search_params = {}

    if search:
        search_regex = {'$regex': f".*{search}.*", '$options': 'i'}

        params = [
            {'model': search_regex},
            {'manufacturer': search_regex},
            {'description': search_regex}
        ]
        search_params = {'$or': params}

    ads = storage.get_list(search_params)
    context = {
        'request': request,
        'page': 'page 1',
        'title': 'first page',
        'ads': ads,
        'search': search
    }

    return templates.TemplateResponse('index.html', context=context)


@router.get('/show-create-form')
def show_create_form(request: Request):
    form_fields = {
        'phone': {'type': 'tel', 'placeholder': 'Enter phone number', 'label': 'Phone'},
        'price': {'type': 'number', 'placeholder': 'Enter price', 'label': 'Price'},
        'manufacturer': {'type': 'text', 'placeholder': 'Enter manufacturer name', 'label': 'Manufacturer'},
        'model': {'type': 'text', 'placeholder': 'Enter model name', 'label': 'Model'},
        'year': {'type': 'number', 'placeholder': 'Enter year of manufacture', 'label': 'Year'},
        'description': {'type': 'text', 'placeholder': 'Enter description', 'label': 'Description'},
        'additional_details': {'type': 'textarea', 'placeholder': 'Enter additional details',
                               'label': 'Additional details'},
        # 'images': {'type': 'file', 'placeholder': 'Upload file(s)', 'label': 'Images'}
    }
    context = {
        'request': request,
        'form_fields': form_fields
    }
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

    return templates.TemplateResponse('show.html', context=context)


@router.post('/create')
def create(advertisement: Advertisement) -> SavedAdvertisement:
    advertisement.model = advertisement.model.strip().upper()
    advertisement.manufacturer = advertisement.manufacturer.strip().upper()
    saved_advertisement = storage.create(advertisement.model_dump())
    return saved_advertisement

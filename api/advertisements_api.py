from fastapi import APIRouter, status
from schemas.schemas import Advertisement, SavedAdvertisement
from storage import storage

router = APIRouter(
    prefix='/api/advertisements',
    tags=['API', 'Advertisements'],
)


@router.get('/')
def get_advertisements(search: str = None, skip: int = 0, limit: int = 10) -> dict:
    ads = storage.get_list(search_string=search, skip=skip, limit=limit)

    if not ads.alive:
        return {
            'advertisements': [],
            'success': True
        }

    result = []

    for ad in ads:
        instance = SavedAdvertisement(**ad)
        result.append(instance)

    return {
        'advertisements': result,
        'success': True
    }


@router.get('/show/{uuid}')
def show_advertisement(uuid: str) -> dict:
    advertisement = storage.get_one({'uuid': uuid})

    if advertisement is None:
        return {
            'errorMsg': 'Advertisement with such UUID doesn\'t exist',
            'error': True
        }

    advertisement_info = SavedAdvertisement(**advertisement)

    return {
        'advertisement': advertisement_info,
        'success': True
    }


@router.put('/update/{uuid}')
def update(advertisement: Advertisement, uuid: str) -> dict:
    storage.update({'uuid': uuid}, advertisement.model_dump())

    return {'success': True}


@router.post('/create', status_code=status.HTTP_201_CREATED)
def create(advertisement: Advertisement) -> dict:
    advertisement.model = advertisement.model.strip().upper()
    advertisement.manufacturer = advertisement.manufacturer.strip().upper()
    saved_advertisement = storage.create(advertisement.model_dump())

    return {
        'advertisement': saved_advertisement,
        'success': True
    }


@router.delete('/delete/{uuid}')
def delete(uuid: str) -> dict:
    storage.delete({'uuid': uuid})

    return {'success': True}

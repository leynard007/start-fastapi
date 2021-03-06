from application.controller import success
from application.logger import get_controller_logger
from application import config
from fastapi import APIRouter, UploadFile, File
from application.util import md5hash

app_name = config.get('APP_NAME')

router = APIRouter()

LOGGER = get_controller_logger('BASE')


@router.get('/health')
def health_check():
    return success(data={
        'name': app_name,
        'hash': md5hash(app_name),
    }, msg='Yes OK~')


@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    content = await file.read()
    decoded_content = content.decode('utf-8')
    LOGGER.info('Received file %s:\n%s' % (
        filename,
        decoded_content
    ))
    return success({
        'filename': filename,
        'contentType': file.content_type,
        'size': len(decoded_content)
    })

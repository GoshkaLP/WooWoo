from fastapi import APIRouter


status = APIRouter(
    prefix='/api/server',
    tags=['server']
)


@status.get('/version')
async def server_version():
    """
    Эндпоинт для получения статуса сервера.
    :return: Статус сервера.
    """
    return {'version': '1.0.0', 'status': 'working'}

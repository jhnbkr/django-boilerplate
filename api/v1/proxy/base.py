from ninja import Router

from api.v1.proxy.http import router as http_router

router = Router()
router.add_router("/http", http_router)

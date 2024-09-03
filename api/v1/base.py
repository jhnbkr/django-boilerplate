from ninja import NinjaAPI

from api.v1.proxy.base import router as proxy_router

api = NinjaAPI(
    title="Harvester API",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    version="1.0.0",
)


@api.get("/ping", url_name="ping")
def ping(request):
    return {"message": "pong"}


api.add_router("/proxy", proxy_router)

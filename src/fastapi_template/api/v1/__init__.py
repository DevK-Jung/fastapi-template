from fastapi_template.api.v1.samples import router as samples_router
from fastapi_template.api.v1.users import router as users_router
from fastapi_template.api.v1.sst_whisper import router as whisper_router

routers = [
    samples_router,
    users_router,
    whisper_router
]

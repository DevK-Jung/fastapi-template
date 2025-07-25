from fastapi_template.api.v1.samples import router as samples_router
from fastapi_template.api.v1.users import router as users_router

routers = [
    samples_router,
    users_router
]

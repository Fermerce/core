from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.celery.tasks.example.publisher import publish_message
from src.celery.tasks.example.tasks import test_task
from src.lib.base.settings import config
from src.lib.middleware.exclude_data_from_response import exclude_keys_middleware
from src.lib.middleware.response_formatter import response_data_transformer
from src.lib.base.router import v1, admin_v1
from src.lib.base.schema.response import IHealthCheck


def get_application():
    _app = FastAPI(
        title=config.project_name,
        version=config.project_version,
        openapi_url=f"/{config.api_prefix}/v{int(config.project_version)}/openapi.json",
        redoc_url=f"/{config.api_prefix}/v{int(config.project_version)}/redoc",
        contact={
            "email": config.contact_email,
            "name": config.contact_name,
        },
        docs_url=f"/{config.api_prefix}/v{int(config.project_version)}/docs",
        debug=config.debug,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.middleware("http")(exclude_keys_middleware(["password"]))
    _app.middleware("http")(response_data_transformer)

    return _app


app = get_application()


@app.get("/", response_model=IHealthCheck, tags=["Health status"])
def health_check():
    publish_message()
    return IHealthCheck(
        name=config.project_name,
        version=config.project_version,
        description=config.project_description,
    )


app.include_router(v1.router)
app.include_router(admin_v1.router)

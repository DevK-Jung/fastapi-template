from typing import List, Annotated

from fastapi import APIRouter, Query, Path, Body

from fastapi_ai.api.v1.sample.schemas import FilterParams, Sample

router = APIRouter(prefix="/samples", tags=["Samples"])


### 쿼리 매개 변수 ###
@router.get("/query")
async def query_param(
        name: str | None = Query(
            default=None,
            title="이름",
            description="이름",
        )
):
    return {"name": name}


@router.get("/query-list")
async def query_params(names: List[str] = Query(default=["foo", "bar"])):
    return {"names": names}


@router.get("/query-model")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


####################

### 경로 매개 변수 ###
@router.get("/path-parm/{name}")
async def path_parm(
        name: str = Path(
            ...,
            title="이름",
            description="이름",
            min_length=3,
            max_lenght=5
        )
):
    return {"name": name}


####################

### 쿼리 경로 동시 선언 ###
@router.get("/path-query/{name}")
async def path_parm(
        name: str = Path(
            ...,
            title="이름",
            description="이름",
            min_length=3,
            max_lenght=5
        ),
        age: int | None = Query(
            default=None,
            title="나이",
            description="나이",
            ge=1,
        )
):
    return {"name": name, "age": age}


####################

### body ###
@router.post("/body", status_code=201)
async def body(
        sample: Sample,
        importance: int = Body()  # 중첩 파라미터
):
    return {"sample": sample, "importance": importance}


@router.post("/body-flat", status_code=201)
async def body_flat(
        sample: Sample = Body(),
):
    return {"sample": sample}

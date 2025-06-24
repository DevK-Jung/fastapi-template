from datetime import datetime, timedelta, time
from typing import List, Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Query, Path, Body, Cookie, Header

from fastapi_ai.api.v1.sample.schemas import FilterParams, Sample, SampleJsonExample2, SampleJsonExample1, \
    SampleUserOut, SampleUserIn, Item

router = APIRouter(prefix="/samples", tags=["Samples"])


############################ 매개변수 #############################################

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


## api doc examples
@router.put("/api-doc/{item_id}")
async def update_item(
        *,
        item_id: int,
        item: Annotated[
            SampleJsonExample1,
            Body(
                examples=[
                    {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                    {
                        "name": "Bar",
                        "price": "35.4",
                    },
                    {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                ],
            ),
        ],
):
    results = {"item_id": item_id, "item": item}
    return results


## openapi json examples
@router.put("/api-doc2/{item_id}")
async def update_item(
        *,
        item_id: int,
        item: Annotated[
            SampleJsonExample2,
            Body(
                openapi_examples={
                    "normal": {
                        "summary": "A normal example",
                        "description": "A **normal** item works correctly.",
                        "value": {
                            "name": "Foo",
                            "description": "A very nice Item",
                            "price": 35.4,
                            "tax": 3.2,
                        },
                    },
                    "converted": {
                        "summary": "An example with converted data",
                        "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                        "value": {
                            "name": "Bar",
                            "price": "35.4",
                        },
                    },
                    "invalid": {
                        "summary": "Invalid data is rejected with an error",
                        "value": {
                            "name": "Baz",
                            "price": "thirty five point four",
                        },
                    },
                },
            ),
        ],
):
    results = {"item_id": item_id, "item": item}
    return results


## 추가 자료형
@router.put("/data-type/{item_id}")
async def read_items(
        item_id: UUID,
        start_datetime: Annotated[datetime, Body()],
        end_datetime: Annotated[datetime, Body()],
        process_after: Annotated[timedelta, Body()],
        repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }


## Cookie 매개변수
@router.get("/cookie/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


## 헤더 매개변수
@router.get("/header/")
async def read_items(user_agent: str | None = Header(default=None)):
    return {"User-Agent": user_agent}


################################################################################

############################ 응답 모델 ############################################

@router.post("/user/",
             response_model=SampleUserOut,
             status_code=201)
async def create_user(user: SampleUserIn) -> Any:
    return user


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@router.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)  # include
async def read_item_name(item_id: str):
    return items[item_id]


# exclude
@router.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]

################################################################################

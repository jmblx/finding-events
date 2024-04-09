import strawberry

from event.schemas import EventResponse, CategoryResponse, EventAdd, EventUpdate, EventGet


@strawberry.experimental.pydantic.type(model=CategoryResponse, all_fields=True)
class CategoryType:
    pass


@strawberry.experimental.pydantic.type(model=EventResponse)
class EventType:
    id: strawberry.auto
    title: strawberry.auto
    description: strawberry.auto
    img_path: strawberry.auto
    address: strawberry.auto
    category: CategoryType


@strawberry.experimental.pydantic.input(model=EventAdd, all_fields=True)
class EventInputType:
    pass


@strawberry.experimental.pydantic.input(model=EventUpdate, all_fields=True)
class EventUpdateType:
    pass


@strawberry.experimental.pydantic.input(model=EventGet, all_fields=True)
class EventGetType:
    pass

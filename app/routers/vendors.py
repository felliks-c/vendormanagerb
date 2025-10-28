@api_router.get("/items", response_model=list[Item])
async def list_items():
    # Заглушка — позже можно подключить базу данных
    return [Item(id=1, name="Sample")]


@api_router.post("/items", response_model=Item)
async def create_item(item: Item):
    # Заглушка — логика создания элемента
    return item
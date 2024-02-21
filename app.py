import chromadb


chroma_client = chromadb.Client()


def get_collection(name):
    return chroma_client.get_or_create_collection(name=name)


def add_items(collection: str, items: list):
    """
    Adds items to a collection.
    """
    get_collection(collection).upsert(
        documents=[i['content'] for i in items],
        metadatas=[i['metadata'] for i in items],
        ids=[i['id'] for i in items]
    )


def search(collection: str, query: str, number: int = 10, threshold: float = 0.5):
    """
    Returns items similar to the query.
    """
    return get_collection(collection).query(
        query_texts=[query],
        n_results=number
    )


items = [
    {
        "id": "1",
        "content": "This is a test article about cats.",
        "metadata": {
            "category": "mammals"
        },
    },
    {
        "id": "2",
        "content": "This is a test article about dogs.",
        "metadata": {
            "category": "mammals"
        },
    },
    {
        "id": "3",
        "content": "This is a test article about birds.",
        "metadata": {
            "category": "birds"
        },
    },
    {
        "id": "4",
        "content": "This is a test article about fish.",
        "metadata": {
            "category": "fish"
        },
    },
    {
        "id": "5",
        "content": "This is a test article about horses.",
        "metadata": {
            "category": "mammals"
        },
    },
    {
        "id": "6",
        "content": "This is a test article about cows.",
        "metadata": {
            "category": "mammals"
        },
    },
    {
        "id": "7",
        "content": "This is a test article about pigs.",
        "metadata": {
            "category": "mammals"
        },
    },
    {
        "id": "8",
        "content": "This is a test article about chickens.",
        "metadata": {
            "category": "birds"
        },
    },
    {
        "id": "9",
        "content": "This is a test article about sheep.",
        "metadata": {
            "category": "mammals"
        },
    },
    {
        "id": "10",
        "content": "This is a test article about goats.",
        "metadata": {
            "category": "mammals"
        },
    },
    {
        "id": "11",
        "content": "This is a test article about lizards.",
        "metadata": {
            "category": "reptiles"
        },
    },
    {
        "id": "12",
        "content": "This is a test article about snakes.",
        "metadata": {
            "category": "reptiles"
        },
    },
    {
        "id": "13",
        "content": "This is a test article about turtles.",
        "metadata": {
            "category": "reptiles"
        },
    },
    {
        "id": "14",
        "content": "This is a test article about alligators.",
        "metadata": {
            "category": "reptiles"
        },
    },
    {
        "id": "15",
        "content": "This is a test article about crocodiles.",
        "metadata": {
            "category": "reptiles"
        },
    },
    {
        "id": "16",
        "content": "This is a test article about frogs.",
        "metadata": {
            "category": "amphibians"
        },
    },
    {
        "id": "17",
        "content": "This is a test article about toads.",
        "metadata": {
            "category": "amphibians"
        },
    },
    {
        "id": "18",
        "content": "This is a test article about salamanders.",
        "metadata": {
            "category": "amphibians"
        },
    },
    {
        "id": "19",
        "content": "This is a test article about newts.",
        "metadata": {
            "category": "amphibians"
        },
    },
    {
        "id": "20",
        "content": "This is a test article about caecilians.",
        "metadata": {
            "category": "amphibians"
        },
    },
]

add_items("articles", items)

# print(similar('articles', 'reptiles', 1))

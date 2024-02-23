from crud_ai.opensearch import index_document

documents = [
    {
        "id": "1",
        "content": "This is a test article about cats.",
        "meta": {
            "category": "mammals"
        },
    },
    {
        "id": "2",
        "content": "This is a test article about dogs.",
        "meta": {
            "category": "mammals"
        },
    },
    {
        "id": "3",
        "content": "This is a test article about birds.",
        "meta": {
            "category": "birds"
        },
    },
    {
        "id": "4",
        "content": "This is a test article about fish.",
        "meta": {
            "category": "fish"
        },
    },
    {
        "id": "5",
        "content": "This is a test article about horses.",
        "meta": {
            "category": "mammals"
        },
    },
    {
        "id": "6",
        "content": "This is a test article about cows.",
        "meta": {
            "category": "mammals"
        },
    },
    {
        "id": "7",
        "content": "This is a test article about pigs.",
        "meta": {
            "category": "mammals"
        },
    },
    {
        "id": "8",
        "content": "This is a test article about chickens.",
        "meta": {
            "category": "birds"
        },
    },
    {
        "id": "9",
        "content": "This is a test article about sheep.",
        "meta": {
            "category": "mammals"
        },
    },
    {
        "id": "10",
        "content": "This is a test article about goats.",
        "meta": {
            "category": "mammals"
        },
    },
    {
        "id": "11",
        "content": "This is a test article about lizards.",
        "meta": {
            "category": "reptiles"
        },
    },
    {
        "id": "12",
        "content": "This is a test article about snakes.",
        "meta": {
            "category": "reptiles"
        },
    },
    {
        "id": "13",
        "content": "This is a test article about turtles.",
        "meta": {
            "category": "reptiles"
        },
    },
    {
        "id": "14",
        "content": "This is a test article about alligators.",
        "meta": {
            "category": "reptiles"
        },
    },
    {
        "id": "15",
        "content": "This is a test article about crocodiles.",
        "meta": {
            "category": "reptiles"
        },
    },
    {
        "id": "16",
        "content": "This is a test article about frogs.",
        "meta": {
            "category": "amphibians"
        },
    },
    {
        "id": "17",
        "content": "This is a test article about toads.",
        "meta": {
            "category": "amphibians"
        },
    },
    {
        "id": "18",
        "content": "This is a test article about salamanders.",
        "meta": {
            "category": "amphibians"
        },
    },
    {
        "id": "19",
        "content": "This is a test article about newts.",
        "meta": {
            "category": "amphibians"
        },
    },
    {
        "id": "20",
        "content": "This is a test article about caecilians.",
        "meta": {
            "category": "amphibians"
        },
    },
]

for document in documents:
    index_document(**document)

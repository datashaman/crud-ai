"""
OpenSearch API
"""
import json
import requests

from .config import OPENSEARCH_HOST


def search_documents(
    query: str,
    filters: dict = None,
    index: str = 'documents', 
    size: int = 10, 
    from_: int = 0
):
    """
    Search for documents in the OpenSearch index
    """
    url = f'{OPENSEARCH_HOST}/{index}/_search'
    response = requests.get(url, json={
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "content": query,
                        },
                    },
                ],
                "filter": filters or [],
            },
        },
        "size": size,
        "from": from_,
    })
    return response.json()


def get_document(id_: str, index: str = 'documents'):
    """
    Get a document from the OpenSearch index
    """
    url = f'{OPENSEARCH_HOST}/{index}/_doc/{id_}'
    response = requests.get(url)
    return response.json()


def index_document(
    id_: str,
    content: str, 
    contentType: str = 'text/plain', 
    meta: dict = None, 
    index: str = 'documents', 
    pipeline: str = None
):
    """
    Index a document in the OpenSearch index
    """
    url = f'{OPENSEARCH_HOST}/{index}/_doc/{id_}'
    params = {}
    if pipeline:
        params['pipeline'] = pipeline
    response = requests.put(url, params=params, json={
        "content": content,
        "contentType": contentType,
        "meta": meta or {},
    })
    return response.json()


def delete_document(id_: str, index: str = 'documents'):
    """
    Delete a document from the OpenSearch index
    """
    url = f'{OPENSEARCH_HOST}/{index}/_doc/{id_}'
    response = requests.delete(url)
    return response.json()


def read_document(id_: str):
    """
    Read a document from the filesystem
    """
    filename = f'documents/{id_}.json'
    with open(filename, 'r') as file:
        return json.load(file)


def update_pipeline(id_: str, model_id: str):
    """
    Update a pipeline in the OpenSearch service
    """
    url = f'{OPENSEARCH_HOST}/_ingest/pipeline/{id_}'
    json = {
        "description": "Extract embeddings from content",
        "processors": [
            {
                "text_embedding": {
                    "model_id": model_id,
                    "field_map": {
                        "content": "embedding",
                    },
                },
            },
        ],
    }
    response = requests.put(url, json=json)
    return response.json()


def delete_pipeline(id_: str):
    """
    Delete a pipeline from the OpenSearch service
    """
    url = f'{OPENSEARCH_HOST}/_ingest/pipeline/{id_}'
    response = requests.delete(url)
    return response.json()


def update_index_template(
    id_: str,
    default_pipeline: str,
    dimension: int,
    name: str,
    space_type: str,
    engine: str,
    parameters: dict
):
    """
    Update or create an index template in the OpenSearch service
    """
    url = f'{OPENSEARCH_HOST}/_index_template/{id_}'
    json = {
        "index_patterns": ["documents*"],
        "settings": {
            "default_pipeline": default_pipeline,
            "index.knn": true,
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text"
                },
                "contentType": {
                    "type": "keyword"
                },
                "embedding": {
                    "type": "knn_vector",
                    "dimension": dimension,
                    "method": {
                        "name": name,
                        "engine": engine,
                        "space_type": space_type,
                        "parameters": parameters,
                    },
                },
                "meta": {
                    "type": "object"
                },
                "title": {
                    "type": "text"
                }
            }
        }
    }
    response = requests.put(url, json=template)
    return response.json()


def delete_index_template(id_: str):
    """
    Delete an index template from the OpenSearch service
    """
    url = f'{OPENSEARCH_HOST}/_index_template/{id_}'
    response = requests.delete(url)
    return response.json()


def upload_model(
    name: str, 
    version: str, 
    model_format: str, 
    model_config: dict, 
    url: str
):
    """
    Upload a model to the OpenSearch service
    """
    url = f'{OPENSEARCH_HOST}/_plugins/_ml/models/_upload'

    json = {
        "name": name,
        "version": version,
        "model_format": model_format,
        "model_config": model_config,
        "url": url,
    }

    response = requests.post(url, json=json)
    return response.json()

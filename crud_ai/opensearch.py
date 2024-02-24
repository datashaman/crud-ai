"""
OpenSearch API
"""

import requests

from crud_ai.config import OPENSEARCH_HOST


def request(method: str, path: str, **kwargs):
    """
    Make a request to the OpenSearch service
    """
    url = f"{OPENSEARCH_HOST}/{path}"
    response = requests.request(method, url, timeout=30, **kwargs)
    return response.json()


def search_query(
    query: str,
    filters: dict = None,
    index: str = "documents",
    size: int = 10,
    from_: int = 0,
):
    """
    Search for documents in the OpenSearch index using full text search
    """
    payload = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "content": query,
                        },
                    }
                ],
            },
        },
        "size": size,
        "from": from_,
    }
    if filters:
        payload["query"]["bool"]["filter"] = filters
    return request("get", f"{index}/_search", json=payload)


def search_neural(
    query: str,
    filters: dict = None,
    index: str = "documents",
    size: int = 10,
    from_: int = 0,
    model_id: str = None,
    k: int = 10,
):
    """
    Search for documents in the OpenSearch index using neural search
    """
    payload = {
        "query": {
            "bool": {
                "should": [
                    {
                        "neural": {
                            "embedding": {
                                "query_text": query,
                                "model": model_id,
                                "k": k,
                            },
                        },
                    }
                ],
            },
        },
        "size": size,
        "from": from_,
    }
    if filters:
        payload["query"]["bool"]["filter"] = filters
    return request("get", f"{index}/_search", json=payload)


def search_combined(
    query: str,
    filters: dict = None,
    index: str = "documents",
    size: int = 10,
    from_: int = 0,
    model_id: str = None,
    k: int = 10,
    fts_score: float = 1.0,
    neural_score: float = 1.0,
):
    """
    Search for documents in the OpenSearch index using full text search and neural search
    """
    payload = {
        "query": {
            "bool": {
                "should": [
                    {
                        "script_score": {
                            "query": {
                                "match": {
                                    "content": query,
                                },
                            },
                            "script": {
                                "source": f"_score * {fts_score}",
                            },
                        },
                    },
                    {
                        "script_score": {
                            "query": {
                                "neural": {
                                    "embedding": {
                                        "query_text": query,
                                        "model": model_id,
                                        "k": k,
                                    },
                                },
                            },
                            "script": {
                                "source": f"_score * {neural_score}",
                            },
                        },
                    },
                ],
            },
        },
        "size": size,
        "from": from_,
    }
    if filters:
        payload["query"]["bool"]["filter"] = filters
    return request("get", f"{index}/_search", json=payload)


def get_document(id: str, index: str = "documents"):
    """
    Get a document from the OpenSearch index
    """
    return request("get", f"{index}/_doc/{id}")


def index_document(
    id: str,
    content: str,
    content_type: str = "text/plain",
    meta: dict = None,
    index: str = "documents",
    pipeline: str = None,
):
    """
    Index a document in the OpenSearch index
    """
    params = {}
    if pipeline:
        params["pipeline"] = pipeline
    return request(
        "put",
        f"{index}/_doc/{id}",
        params=params,
        json={
            "content": content,
            "content_type": content_type,
            "meta": meta or {},
        },
    )


def delete_document(id: str, index: str = "documents"):
    """
    Delete a document from the OpenSearch index
    """
    return request("delete", f"{index}/_doc/{id}")


def embedding_pipeline(id: str, model_id: str):
    """
    Create an embedding pipeline in the OpenSearch service
    """
    return request(
        "put",
        f"_ingest/pipeline/{id}",
        json={
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
        },
    )


def delete_pipeline(id: str):
    """
    Delete a pipeline from the OpenSearch service
    """
    return request("delete", f"_ingest/pipeline/{id}")


def embedding_template(
    id: str,
    default_pipeline: str,
    dimension: int = 768,
    name: str = "hnsw",
    space_type: str = "l2",
    engine: str = "lucene",
    parameters: dict = None,
    index_patterns: list = ["documents*"],
):
    """
    Update or create an index template in the OpenSearch service
    """
    parameters = parameters or {}

    return request(
        "put",
        f"_template/{id}",
        json={
            "index_patterns": index_patterns,
            "settings": {
                "default_pipeline": default_pipeline,
                "index.knn": True,
                "number_of_shards": 1,
                "number_of_replicas": 0,
            },
            "mappings": {
                "properties": {
                    "content": {"type": "text"},
                    "content_type": {"type": "keyword"},
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
                    "meta": {"type": "object"},
                    "title": {"type": "text"},
                }
            },
        },
    )


def delete_index_template(id: str):
    """
    Delete an index template from the OpenSearch service
    """
    return request("delete", f"_index_template/{id}")


def ml_task(task: dict):
    """
    Handle a task from the OpenSearch ML service
    """
    if task['status'] == 'COMPLETED':
        return task

    task_id = task["task_id"]

    while True:
        task = request("get", f"_plugins/_ml/tasks/{task_id}")

        if task["state"] in ["COMPLETED", "FAILED", "CREATED"]:
            return task

        raise Exception(f"Unknown task state: {task}")


def upload_model(
    name: str, version: str, model_format: str, model_config: dict, url: str
):
    """
    Upload a model to the OpenSearch service
    """
    return ml_task(
        request(
            "post",
            "_plugins/_ml/models/_upload",
            json={
                "name": name,
                "version": version,
                "model_format": model_format,
                "model_config": model_config,
                "url": url,
            },
        )
    )


def load_model(model_id: str):
    """
    Load a model in the OpenSearch service
    """
    return ml_task(
        request(
            "post",
            f"_plugins/_ml/models/{model_id}/_load",
        )
    )


def unload_model(model_id: str):
    """
    Unload a model from the OpenSearch service
    """
    return request(
        "post",
        f"_plugins/_ml/models/{model_id}/_unload",
    )


def search_connectors(name: str = None):
    """
    Search for connectors in the OpenSearch service
    """
    if name:
        query = {
            "match": {
                "name": name,
            },
        }
    else:
        query = {
            "match_all": {},
        }

    return request(
        "get",
        "_plugins/_ml/connectors/_search",
        json={
            "query": query,
        }
    )


def create_openai_connector(name: str, api_key: str, organization_id: str = None, model: str = 'text-embedding-3-small'):
    """
    Create an OpenAI connector in the OpenSearch service
    """
    headers = {
        "Authorization": "Bearer ${credential.api_key}",
    }

    if organization_id:
        headers["OpenAI-Organization"] = organization_id

    return request(
        "post",
        "_plugins/_ml/connectors/_create",
        json={
            "name": name,
            "description": "OpenAI Embeddings",
            "version": "1",
            "protocol": "http",
            "parameters": {
                "model": model,
            },
            "credential": {
                "api_key": api_key,
            },
            "actions": [
                {
                    "action_type": "predict",
                    "method": "POST",
                    "url": "https://api.openai.com/v1/embeddings",
                    "headers": headers,
                    "request_body": "{ \"input\": ${parameters.input}, \"model\": \"${parameters.model}\" }",
                    "pre_process_function": "connector.pre_process.openai.embedding",
                    "post_process_function": "connector.post_process.openai.embedding"
                },
            ],
        }
    )


def delete_connectors(name: str):
    """
    Delete connectors from the service by name.
    """
    responses = []
    connectors = search_connectors(name)['hits']['hits']
    for connector in connectors:
        connector_id = connector['_id']
        responses.append(
            request(
                "delete",
                f"_plugins/_ml/connectors/{connector_id}"
            )
        )

    return responses


def update_trusted_endpoints():
    """
    Update the trusted endpoints in the OpenSearch service
    """
    return request(
        "put",
        "_cluster/settings",
        json={
            "persistent": {
                "plugins.ml_commons.trusted_connector_endpoints_regex": [
                    "^https://api\\.openai\\.com/.*$",
                ]
            }
        }
    )


def update_cluster_settings():
    """
    Update the cluster settings in the OpenSearch service
    with basic settings for local development
    """
    return request(
        "put",
        "_cluster/settings",
        json={
            "persistent": {
                "plugins.ml_commons.allow_registering_model_via_url": True,
                "plugins.ml_commons.only_run_on_ml_node": False,
            },
        }
    )


def register_model_group(name: str, description: str):
    """
    Register a model group in the OpenSearch service
    """
    return request(
        "post",
        "_plugins/_ml/model_groups/_register",
        json={
            "name": name,
            "description": description,
        }
    )


def search_model_groups(name: str = None):
    """
    Search for model groups in the OpenSearch service
    """
    if name:
        query = {
            "match": {
                "name": name,
            },
        }
    else:
        query = {
            "match_all": {},
        }

    return request(
        "get",
        "_plugins/_ml/model_groups/_search",
        json={
            "query": query,
        }
    )


def delete_model_group(id: str):
    """
    Delete a model group from the OpenSearch service
    """
    return request(
        "delete",
        f"_plugins/_ml/model_groups/{id}"
    )


def register_model(name: str, description: str, model_group_id: str, connector_id: str):
    """
    Register a model in the OpenSearch service
    """
    return ml_task(request(
        "post",
        "_plugins/_ml/models/_register",
        json={
            "name": name,
            "function_name": "remote",
            "model_group_id": model_group_id,
            "description": description,
            "connector_id": connector_id,
        }
    ))


def deploy_model(model_id: str):
    """
    Deploy a model in the OpenSearch service
    """
    return request(
        "post",
        f"_plugins/_ml/models/{model_id}/_deploy",
    )


def undeploy_model(model_id: str):
    """
    Undeploy a model from the OpenSearch service
    """
    return request(
        "post",
        f"_plugins/_ml/models/{model_id}/_undeploy",
    )


def search_models():
    """
    Search for models in the OpenSearch service
    """
    return request(
        "get",
        "_plugins/_ml/models/_search",
        json={
            "query": {
                "match_all": {},
            }
        }
    )


def delete_model(id: str):
    """
    Delete a model from the OpenSearch service
    """
    return request(
        "delete",
        f"_plugins/_ml/models/{id}"
    )


def delete_index(index: str):
    """
    Delete an index from the OpenSearch service
    """
    return request("delete", index)

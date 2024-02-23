import os
import sys
import time

from dotenv import load_dotenv

load_dotenv()

from documents.animals import documents

from crud_ai.opensearch import (
    create_openai_connector,
    delete_index,
    delete_model,
    delete_model_group,
    deploy_model,
    embedding_pipeline,
    embedding_template,
    index_document,
    register_model,
    register_model_group,
    search_models,
    search_model_groups,
    undeploy_model,
    update_trusted_endpoints,
)

response = search_models()

if response['hits']['total']['value']:
    for hit in response['hits']['hits']:
        print(hit)

        model_id = hit['_id']
        response = undeploy_model(model_id)
        response = delete_model(model_id)
        print(response)
        time.sleep(1)

update_trusted_endpoints()

response = search_model_groups("remote-models")

if response['hits']['total']['value']:
    model_group_id = response['hits']['hits'][0]['_id']
    response = delete_model_group(model_group_id)
    print(response)
    time.sleep(1)

response = register_model_group("remote-models", "A remote model group")

if response['status'] != 'CREATED':
    print(response)
    sys.exit(1)

model_group_id = response['model_group_id']

response = create_openai_connector(os.environ.get('OPENAI_API_KEY'))
connector_id = response['connector_id']

response = register_model('openai-text-embedding-ada-002', 'Embedding model', model_group_id, connector_id)
print(response)
model_id = response['model_id']

response = deploy_model(model_id)
print(response)

embedding_pipeline('embedding', model_id)

embedding_template('embedding', 'embedding')

delete_index('documents*')

for document in documents:
    response = index_document(**document)
    print(response)

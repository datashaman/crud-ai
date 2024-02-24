import json
import os
import sys
import time

import click
from dotenv import load_dotenv

load_dotenv()

from documents.animals import documents

from crud_ai.opensearch import (
    create_openai_connector,
    delete_connectors,
    delete_index,
    delete_model,
    delete_model_group,
    deploy_model,
    embedding_pipeline,
    embedding_template,
    index_document,
    register_model,
    register_model_group,
    search_connectors,
    search_models,
    search_model_groups,
    undeploy_model,
    update_cluster_settings,
    update_trusted_endpoints,
)


class Config:
    def __init__(self):
        pass


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = Config()


@cli.command()
@click.pass_obj
def setup(config):
    click.echo("Updating cluster settings")
    response = update_cluster_settings()
    click.echo(json.dumps(response, indent=2))

    click.echo("Updating trusted endpoints")
    response = update_trusted_endpoints()
    click.echo(json.dumps(response, indent=2))

    click.echo("Setting up model group for remote models")
    response = register_model_group("remote-models", "A remote model group")
    click.echo(json.dumps(response, indent=2))

    model_group_id = response['model_group_id']

    click.echo("Setting up OpenAI connector")
    response = create_openai_connector(
        'openai-connector',
        os.environ.get('OPENAI_API_KEY'),
        os.environ.get('OPENAI_ORGANIZATION')
    )
    click.echo(json.dumps(response, indent=2))

    connector_id = response['connector_id']

    click.echo("Registering OpenAI text embedding model")
    response = register_model('openai-text-embedding-ada-002', 'Embedding model', model_group_id, connector_id)
    click.echo(json.dumps(response, indent=2))
    time.sleep(2)

    model_id = response['model_id']

    click.echo("Deploying OpenAI text embedding model")
    response = deploy_model(model_id)
    click.echo(json.dumps(response, indent=2))

    sys.exit()

    embedding_pipeline('embedding', model_id)

    embedding_template('embedding', 'embedding')

    delete_index('documents*')

    for document in documents:
        response = index_document(**document)
        print(response)


def teardown_models():
    click.echo("Tearing down models")

    response = search_models()

    if response['hits']['total']['value']:
        for hit in response['hits']['hits']:
            model_id = hit['_id']
            response = undeploy_model(model_id)
            click.echo(json.dumps(response, indent=2))
            response = delete_model(model_id)
            click.echo(json.dumps(response, indent=2))


def teardown_model_groups():
    click.echo("Tearing down model groups")

    response = search_model_groups('remote-models')

    if response['hits']['total']['value']:
        model_group_id = response['hits']['hits'][0]['_id']
        response = delete_model_group(model_group_id)
        click.echo(json.dumps(response, indent=2))


def teardown_openai_connector():
    click.echo("Tearing down OpenAI connectors")
    response = delete_connectors('openai-connector')

    if response:
        click.echo(json.dumps(response, indent=2))


@cli.command()
@click.pass_obj
def teardown(config):
    teardown_models()
    time.sleep(2)
    teardown_model_groups()
    time.sleep(2)
    teardown_openai_connector()
    delete_index('documents*')


@cli.command()
@click.pass_obj
def models(config):
    response = search_models()
    click.echo(json.dumps(response, indent=2))


@cli.command()
@click.pass_obj
def model_groups(config):
    response = search_model_groups()
    click.echo(json.dumps(response, indent=2))


@cli.command()
@click.pass_obj
def connectors(config):
    response = search_connectors()
    click.echo(json.dumps(response, indent=2))


if __name__ == "__main__":
    cli()

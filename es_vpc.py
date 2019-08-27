import boto3
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection


def es_config():
    session = boto3.session.Session()
    credentials = session.get_credentials().get_frozen_credentials()
    print(credentials.access_key)
    print(credentials.secret_key)
    print(session.region_name)

    es_host = 'vpc-es-cluster-1-k2q764gewwgbshvntv6rpz5noe.us-east-1.es.amazonaws.com'

    aws_auth = AWSRequestsAuth(
        aws_access_key=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        aws_host=es_host,
        aws_region=session.region_name,
        aws_service='es'
    )
    es = Elasticsearch(
        hosts=[{'host': es_host, 'port': 443}],
        http_auth=aws_auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection)

    document = {
        "title": "Moneyball",
        "director": "Bennett Miller",
        "year": "2011"
    }

    es.index(index="movies", doc_type="_doc", id="5", body=document)

    print(es.get(index="movies", doc_type="_doc", id="5"))


def main():
    es_config()


if __name__ == "__main__":
    main()

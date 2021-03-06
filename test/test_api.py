from rdflib.plugin import register, Parser, Serializer
register('json-ld', Parser, 'rdflib_jsonld.parser', 'JsonLDParser')
register('json-ld', Serializer, 'rdflib_jsonld.serializer', 'JsonLDSerializer')

from rdflib import Graph, Literal, URIRef

def test_parse():
    test_json = '''
    {
        "@context": {
            "dc": "http://purl.org/dc/terms/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
        },
        "@id": "http://example.org/about",
        "dc:title": {
            "@language": "en",
            "@value": "Someone's Homepage"
        }
    }
    '''
    g = Graph().parse(data=test_json, format='json-ld')
    assert list(g) == [(
        URIRef('http://example.org/about'),
        URIRef('http://purl.org/dc/terms/title'),
        Literal("Someone's Homepage", lang='en'))]


def test_prefix():
    test_json = '''
    {
        "@context": {
            "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "@vocab": "http://example.org"
        },
        "CHEBI:33709": {
            "rdf:label": "Amino Acid"
        }
    }
    '''
    g = Graph().parse(data=test_json, format="json-ld", prefix=True)
    assert '@prefix CHEBI: <http://purl.obolibrary.org/obo/CHEBI_>' in g.serialize(format="turtle").decode()

    g = Graph().parse(data=test_json, format="json-ld", prefix=False)
    assert '@prefix CHEBI: <http://purl.obolibrary.org/obo/CHEBI_>' not in g.serialize(format="turtle").decode()

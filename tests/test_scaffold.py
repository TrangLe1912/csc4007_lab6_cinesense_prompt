from pathlib import Path
import sys
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from src.retriever import Retriever,load_chunks
from src.evaluation import validate_output

def test_retriever():
    assert len(load_chunks())==20
    assert len(Retriever().search('slow pacing',top_k=3))==3

def test_output_schema():
    review='A lovely ending.'
    assert validate_output('{"sentiment":"positive","evidence":["lovely ending"],"short_explanation":"Praise","confidence":"high"}',review)['schema_valid']
    assert not validate_output('{not-json}',review)['schema_valid']

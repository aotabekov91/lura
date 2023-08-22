import pytest
from lura import Lura

@pytest.fixture
def app(): 

    Lura.setConnection=lambda *a, **k: print()

    return Lura(listen_port=False)

def test_app_initiated(app): 
    assert app.__class__.__name__=='Lura'

def test_intent_and_entity_properties(app):

    for name, plug in app.plugs.plugs.items():
        c1=hasattr(plug, 'intents')
        c2=hasattr(plug, 'entities')
        assert c1 and c2

@pytest.mark.skip(reason='at least one plugin has intents')
def test_intents_are_none(app):

    for name, plug in app.plugs.plugs.items():
        assert plug.intents is None



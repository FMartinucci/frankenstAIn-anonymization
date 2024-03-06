from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.nlp_engine import NlpEngine

stanza_config = {
                "nlp_engine_name": "stanza",
                "models": [{"lang_code": "it", "model_name": "it"},
                        {"lang_code": "en", "model_name": "en"}]
            }
    
spacy_config = {
                "nlp_engine_name": "spacy",
                "models": [{"lang_code": "it", "model_name": "it_core_news_sm"},
                            {"lang_code": "en", "model_name": "en_core_web_sm"}],
            }

stanza_engine : NlpEngine = None
spacy_engine : NlpEngine = None

def _initialize_engine(engine):
    config = spacy_config if engine == "spacy" else stanza_config
    provider = NlpEngineProvider(nlp_configuration=config)
    return provider.create_engine()

def get_engine(name):
    engine = stanza_engine if name == "stanza" else spacy_engine
    if engine is None:
        engine = _initialize_engine(name)
    return engine

    
import string
import random
import pandas as pd
from csv_analyzer import CSVAnalyzer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import BatchAnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer.nlp_engine import NlpEngine
from faker import Faker

import stanza

stanza.download("it")
stanza.download("en")

ANONYMIZATION_BASE_PATH = '/home/martinuccif/Scrivania/anonymization'

nlp_engine : NlpEngine = None
fake_maker = Faker('it_IT')

def get_spacy_engine(nlp_engine):
    if nlp_engine is None:
        spacy_config = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "it", "model_name": "it_core_news_sm"},
                        {"lang_code": "en", "model_name": "en_core_web_sm"}],
        }
        spacy_provider = NlpEngineProvider(nlp_configuration=spacy_config)
        nlp_engine = spacy_provider.create_engine()
    return nlp_engine

def get_stanza_engine(nlp_engine):
    if nlp_engine is None:
        stanza_config = {
            "nlp_engine_name": "stanza",
            "models": [{"lang_code": "it", "model_name": "it"},
                       {"lang_code": "en", "model_name": "en"}]
        }
        stanza_provider = NlpEngineProvider(nlp_configuration=stanza_config)
        nlp_engine = stanza_provider.create_engine()
    return nlp_engine

def generate_name(x):
    return fake_maker.name()

def generate_phone_number(x):
    return fake_maker.phone_number()

def generate_fiscal_code(x):
    return fake_maker.ssn()

def generate_email(x):
    return fake_maker.free_email()

def generate_location(x):
    return fake_maker.city()


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

operators = {
    "PERSON": OperatorConfig("custom", {"lambda": generate_name }), 
    "PHONE_NUMBER" : OperatorConfig("custom", {"lambda": generate_phone_number }),
    "IT_FISCAL_CODE" : OperatorConfig("custom", {"lambda": generate_fiscal_code }),
    "EMAIL_ADDRESS" : OperatorConfig("custom", {"lambda": generate_email }),
    "LOCATION" : OperatorConfig("custom", {"lambda": generate_location})
}

# CON STANZA 
analyzer_engine = AnalyzerEngine(nlp_engine=get_stanza_engine(nlp_engine), supported_languages=["en", "it"])
# CON SPACY
analyzer_engine = AnalyzerEngine(nlp_engine=get_spacy_engine(nlp_engine), supported_languages=["en", "it"])
csv_analyzer = CSVAnalyzer(analyzer_engine)
analyzer_results = csv_analyzer.analyze_csv(ANONYMIZATION_BASE_PATH + '/datasets/data_export_3.csv',
                                            language="it")

anonymizer = BatchAnonymizerEngine()
anonymized_results = anonymizer.anonymize_dict(analyzer_results, operators=operators)
out_file = ANONYMIZATION_BASE_PATH + '/results/output_' + id_generator(size=4) + '.csv'
pd.DataFrame(anonymized_results).to_csv(out_file, index=False)
print(out_file)
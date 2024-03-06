import pandas as pd
from csv_analyzer import CSVAnalyzer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import BatchAnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer.nlp_engine import NlpEngine
from faker import Faker
from datetime import datetime

import stanza

fake_maker = Faker('it_IT')

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




class CSVProcessor(): 
    
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

    
    nlp_engine : NlpEngine = None

    def __init__(self, engine="spacy") :
        if engine=="stanza":
            stanza.download("it")
            stanza.download("en")
        self.operators = {
        "PERSON": OperatorConfig("custom", {"lambda": generate_name }), 
        "PHONE_NUMBER" : OperatorConfig("custom", {"lambda": generate_phone_number }),
        "IT_FISCAL_CODE" : OperatorConfig("custom", {"lambda": generate_fiscal_code }),
        "EMAIL_ADDRESS" : OperatorConfig("custom", {"lambda": generate_email }),
        "LOCATION" : OperatorConfig("custom", {"lambda": generate_location})
        }
        self.nlp_engine = self.initialize_engine(engine)


    def initialize_engine(self, engine="spacy"):
        config = self.spacy_config if engine == "spacy" else self.stanza_config
        provider = NlpEngineProvider(nlp_configuration=config)
        return provider.create_engine()

    def process_csv(self, filepath, out_file):
        print("PROCESS CSV -START! At " + datetime.now().strftime("%H:%M:%S"))
        analyzer_engine = AnalyzerEngine(nlp_engine=self.nlp_engine, supported_languages=["en", "it"])
        csv_analyzer = CSVAnalyzer(analyzer_engine)
        analyzer_results = csv_analyzer.analyze_csv(filepath,
                                                    language="it")

        anonymizer = BatchAnonymizerEngine()
        anonymized_results = anonymizer.anonymize_dict(analyzer_results, operators=self.operators)
        pd.DataFrame(anonymized_results).to_csv(out_file, index=False)
        print("PROCESS CSV - END! At " + datetime.now().strftime("%H:%M:%S"))
        return out_file
    
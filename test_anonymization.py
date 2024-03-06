from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer.nlp_engine import NlpEngineProvider
from faker import Faker

configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "it", "model_name": "it_core_news_sm"},
                {"lang_code": "en", "model_name": "en_core_web_sm"}],
}
# Initialize the engine:
provider = NlpEngineProvider(nlp_configuration=configuration)

nlp_engine = provider.create_engine()

text = "Ciao, mi chiamo Francesca Martinucci e il mio numero è 3469423001. Lui è Giovanni Rana e il suo numero è 3447785552"

analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en", "it"])
analyzer_results = analyzer.analyze(text=text, language="it", return_decision_process=True)

fake_maker = Faker('it_IT')

def generate_name(x):
    return fake_maker.name()

def generate_phone_number(x):
    return fake_maker.phone_number()

anonymizer = AnonymizerEngine()
result = anonymizer.anonymize(
    text,
    analyzer_results,
    operators={"PERSON": OperatorConfig("custom", {"lambda": generate_name }), 
               "PHONE_NUMBER" : OperatorConfig("custom", {"lambda": generate_phone_number })},
)

print(result.text)




from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser


class ParsingTemplateManager:
    # Initializer
    def __init__(self, parsing_template_type):
        self.parsing_template_type = parsing_template_type

    # Template Getter
    def get_parsing_template(self):
        template = """
            You are an assistant that converts raw English test text into a valid JSON array.

            Schema per question:
            [
            {{
                "ask": {{ "text": "string" }},
                "choices": [ {{ "text": "string" }}, {{ "text": "string" }}, ... ],
                "materials": [ {{ "text": "string" }}, {{ "text": "string" }}, ... ]
            }}
            ]

            Rules (strict):
            - Output ONLY a valid JSON array (no extra text or explanations).
            - Do NOT invent, modify, infer, or reorder any content.
            - Use double quotes for all strings and \\n for line breaks.
            - Preserve the full schema structure at all times.
            "ask", "choices", and "materials" must always appear, even if empty.

            - For every "text" field:
            * If the original content is missing, label-only, or contains no meaningful text
                (i.e., only punctuation, whitespace, numbering, or headings),
                then keep the key but set its value to an empty string: "text": "".
            * Never delete the key or its parent object.

            - Mapping:
            * ask.text ← actual question text (ignore labels such as "Question:", "Q:", etc.).
            * choices[].text ← each answer option, removing only label markers like A./B./C./D.
            * materials[].text ← all remaining context (e.g., passage, dialogue, summary) not used in ask or choices.

            - Multiple questions → multiple objects.

            <Raw Input>
            {output}
            </Raw Input>

            Return ONLY the final JSON array.
            """
        return template


# Function to generate LLM parser
def generate_llm_parser(chain_config):
    # Create generator object
    llm_parser = ChatOpenAI(
        openai_api_key=chain_config.parser.api_key,
        model=chain_config.parser.model_id,
        temperature=chain_config.parser.temperature,
        top_p=chain_config.parser.top_p,
    )

    return llm_parser


# Function to define prompt template
def define_parsing_prompt(parsing_template_type):
    # Define a question generation template using TemplateManager
    parsing_template_manager = ParsingTemplateManager(
        parsing_template_type=parsing_template_type
    )
    parsing_template = parsing_template_manager.get_parsing_template()

    # Create a PromptTemplate object
    parsing_prompt = PromptTemplate(
        input_variables=["output"], template=parsing_template
    )

    return parsing_prompt


# Function to build LLM parser chain
def build_parsing_chain(chain_config, parsing_template_type):
    # Get LLM parser
    llm_parser = generate_llm_parser(chain_config)
    # Get prompt template
    parsing_prompt = define_parsing_prompt(parsing_template_type)

    # Build LLM parser chain
    output_parser = JsonOutputParser()
    parser_chain = LLMChain(
        llm=llm_parser, prompt=parsing_prompt, output_parser=output_parser
    )

    return parser_chain

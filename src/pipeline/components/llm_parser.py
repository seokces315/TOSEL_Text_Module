from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser


class ParsingTemplateManager:
    # Initializer
    def __init__(self):
        pass

    # Template Getter
    def get_parsing_template(self):
        template = """
        You are a parser that transforms raw English test text into a strict JSON array.

        Schema per question:
        [
            {{
                "materials": [
                    {{ "text": "string" }},
                    ...
                ],
                "ask": {{ "text": "string" }},
                "choices": [
                    {{ "text": "string" }},
                    {{ "text": "string" }},
                    {{ "text": "string" }},
                    ...
                ]
            }}
        ]

        Rules (STRICT):
        - Output ONLY a valid JSON array (no extra text of any kind).
        - Do NOT invent, modify, infer, or paraphrase any content.
        - Keep the original order of all text segements without rearranging.
        - Use double quotes for all strings and \\n for line breaks exactly as shown.
        - Always preserve the full schema structure. The keys "materials", "ask", and "choices" must appear even when their arrays or objects are empty.
        
        - Mapping:
        * materials[].text : All remaining context not used in ask or choices (e.g., passage, dialouge, summary). Ignore labels such as "passage:", "dialouge:", "summary:" or numbering.
        * ask.text : The actual question text only. Ignore labels such as "Question:", "Q", or numbering.
        * choices[].text : Each answer option, removing only the label markers (A., B., C., D., etc.).

        * Multiple questions -> Multiple JSON objects in the array.

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
def define_parsing_prompt():
    # Define a question generation template using TemplateManager
    parsing_template_manager = ParsingTemplateManager()
    parsing_template = parsing_template_manager.get_parsing_template()

    # Create a PromptTemplate object
    parsing_prompt = PromptTemplate(
        input_variables=["output"], template=parsing_template
    )

    return parsing_prompt


# Function to build LLM parser chain
def build_parsing_chain(chain_config):
    # Get LLM parser
    llm_parser = generate_llm_parser(chain_config)
    # Get prompt template
    parsing_prompt = define_parsing_prompt()

    # Build LLM parser chain
    output_parser = JsonOutputParser()
    parser_chain = LLMChain(
        llm=llm_parser, prompt=parsing_prompt, output_parser=output_parser
    )

    return parser_chain

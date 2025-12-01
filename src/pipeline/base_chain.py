from .components.llm_generator import build_generator_chain
from .components.llm_parser import build_parsing_chain

from .schema import Content, Material, Ask, Choice, Item


# Function to build the complete LLM pipeline (Generator + Parser)
def build_complete_chain(chain_config, prompt, example):
    # Get LLM generator chain - 1st chain
    generator_chain = build_generator_chain(chain_config, prompt, example)

    # Execute the generator chain to generate a response
    items = generator_chain.invoke({})
    items_text = items.get("text")

    # Get LLM parser chain - 2nd chain
    parser_chain = build_parsing_chain(chain_config)

    return items_text, parser_chain


# Function to dynamically build a list of objects based on the provided schema definition
def build_objects_from_schema(results):
    # Create a list to store item objects
    item_list = list()

    # Iterate through each result item and initialize containers for parsing
    for result in results:
        materials = []

        # Generate materials
        materials = [
            Material(index=idx, content=Content(text=material["text"]))
            for idx, material in enumerate(result["materials"])
        ]

        # Generate ask
        ask = Ask(text=result["ask"]["text"])

        # Generate choices
        choices = [
            Choice(
                index=idx,
                content=Content(text=choice["text"]),
                isCorrect=(idx == 0),
            )
            for idx, choice in enumerate(result["choices"])
        ]

        # Build item
        item = Item(materials=materials, ask=ask, choices=choices)

        # Append the parsed item to the result list
        item_list.append(item)

    return item_list

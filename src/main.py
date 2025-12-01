from parser import parse_args

from loaders.prompt_loader import load_prompt
from loaders.example_loader import load_example

from utils.config import ChainConfig, GeneratorConfig, ParserConfig

from pipeline.base_chain import build_complete_chain, build_objects_from_schema

import warnings

warnings.filterwarnings(action="ignore")

import time

import json


def main(args):
    # Measure execution time
    start_time = time.time()

    # Load prompt & example
    comprehension_type = args.comprehension_type
    problem_type = args.problem_type
    level = args.level
    prompt_path = (
        f"./bank/prompt/{comprehension_type}_{problem_type}_{level}_prompt.txt"
    )
    example_path = (
        f"./bank/example/{comprehension_type}_{problem_type}_{level}_example.txt"
    )
    prompt = load_prompt(prompt_path=prompt_path)
    example = load_example(example_path=example_path)

    # Initialize LLM chain pipeline
    model_id = args.model_id
    generation_template_type = args.generation_template_type
    parsing_template_type = args.parsing_template_type

    chain_config = ChainConfig(
        generator=GeneratorConfig(model_id=model_id),
        parser=ParserConfig(model_id=model_id),
    )

    output, complete_chain = build_complete_chain(
        chain_config, generation_template_type, prompt, example, parsing_template_type
    )  # 생성된 문항, chain

    result = complete_chain.invoke({"output": output})
    print("result\n", result["text"])

    item_list = build_objects_from_schema(result=result["text"])

    # Print the final results
    print()
    print(
        json.dumps(
            [item.model_dump() for item in item_list], indent=2, ensure_ascii=False
        )
    )

    # Print execution time
    end_time = time.time()
    elapsed = end_time - start_time
    print()
    print("==============================")
    print()
    print(f"Elapsed time: {elapsed:.2f}초")


if __name__ == "__main__":
    args = parse_args()
    main(args)

import argparse
import inspect
import json
import os
import sys
from typing import Any, List, Union

import prmpt
from prmpt.metric import *
from prmpt.pcomp import *

def write_data(data: Union[object, List[object]], file_path: str) -> None:
    """
    Writes data to a file in JSON format.

    Args:
        data (Union[object, List[object]]): The data to be written. It can be a single object or a list of objects.
        file_path (str): The path to the file where the data will be written.

    Returns:
        None
    """
    if not isinstance(data, (list, object)):
        raise TypeError("The 'data' argument must be an object or a list of objects.")

    if not isinstance(data, list):
        data = [data]

    try:
        with open(file_path, "a+") as f:
            for obj in data:
                f.write(json.dumps(obj) + "\n")
    except IOError:
        raise IOError("An error occurred while writing to the file.")
    
def read_jsonl(file_path: str) -> List[object]:
    """
    Reads a file in JSONL format and returns a list of JSON objects.

    Args:
        file_path (str): The path to the JSONL file.

    Returns:
        List[object]: A list of JSON objects parsed from the file.
    """
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            json_list = []
            for line in lines:
                try:
                    json_obj = json.loads(line)
                    json_list.append(json_obj)
                except json.JSONDecodeError as e:
                    raise json.JSONDecodeError(
                        f"Error decoding JSON object: {e.msg}", e.doc, e.pos
                    )
    except IOError:
        raise IOError("An error occurred while reading the file.")

    return json_list

def read_txt(file_path: str) -> List[str]:
    """
    Reads a text file and returns a list of lines.

    Args:
        file_path (str): The path to the text file.

    Returns:
        List[str]: A list of lines read from the file.
    """
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except IOError:
        raise IOError("An error occurred while reading the file.")

    return lines

def read_data(file_path: str, json: bool) -> List[object]:
    """
    Reads data from a file either in JSONL format or plain text format.

    Args:
        file_path (str): The path to the file.
        json (bool): Specifies whether the file is in JSONL format (True) or plain text format (False).

    Returns:
        List[object]: A list of objects parsed from the file.
    """
    if json:
        return read_jsonl(file_path)
    else:
        return read_txt(file_path)
    
def run_compress(
    compressor_obj: prmpt.pcomp,
    prompt: str,
    json: bool,
    skip_system: bool,
) -> Any:
    """
    Runs a compressor object with the specified parameters.

    Args:
        compressor_obj (prmpt.PromptComp): The compressor object to be run.
        prompt (str): The prompt for the compressor.
        json (bool): Specifies whether to process the prompt as JSON (True) or plain text (False).
        skip_system (bool): Specifies whether to skip the system response in the compression (True) or include it (False).

    Returns:
        Any: The result of running the compressor object.
    """
    print(f"!!! prompt: {prompt}")
    return compressor_obj(prompt, json=json, skip_system=skip_system)

def print_result(res: Any) -> None:
    """
    Prints the result or a list of results.

    Args:
        res (Any): The result to be printed. It can be a single result object or a list of results.
    """
    if isinstance(res, list):
        for r in res:
            print(r)
    else:
        print(res)

def run(args: argparse.Namespace) -> None:
    """
    Runs the compression process based on the provided CLI arguments.

    Args:
        args (argparse.Namespace): The CLI arguments for running the compression.

    Returns:
        None
    """
    try:
        pcomp_class = getattr(sys.modules[__name__], args.compressor_name)
    except AttributeError:
        implemented_comps = inspect.getmembers(prmpt.pcomp)
        implemented_comps = [
            member[0] for member in implemented_comps if inspect.isclass(member[1])
        ]
        raise NotImplementedError(
            f"Compressor `{args.compressor_name}` not implemented.\nChoose one of: {implemented_comps}"
        )
    
    metrics = []
    for metric in args.metrics:
        try:
            metrics.append(getattr(sys.modules[__name__], metric)())
        except AttributeError:
            implemented_metrics = inspect.getmembers(prmpt.metric)
            implemented_metrics = [
                member[0]
                for member in implemented_metrics
                if inspect.isclass(member[1])
            ]
            raise NotImplementedError(
                f"Metric `{metric}` not implemented!\nChoose one of: {implemented_metrics}"
            )
        
    pcomp = pcomp_class(*args.compressor_args, verbose=False, metrics=metrics)

    current_directory = os.getcwd()
    full_path = os.path.join(current_directory, args.prompt_data_or_path)
    print(f"full_path: {full_path}")
    if os.path.exists(full_path):
        prompts = read_data(full_path, args.json)
        res = [
            run_compress(pcomp, prompt, args.json, args.skip_system)
            for prompt in prompts
        ]
    else:
        res = run_compress(
            pcomp, args.prompt_data_or_path, args.json, args.skip_system
        )

    if args.log_file is not None:
        write_data(res, args.log_file)
    else:
        print_result(res)

def main():
    """Main entrypoint for the Prmpt CLI."""
    parser = argparse.ArgumentParser(description="Prmpt CLI")

    parser.add_argument(
        "prompt_data_or_path",
        help="Either the prompt data (string or json string) or path to a file containing new line separated prompt data.",
    )

    parser.add_argument("compressor_name", help="Name of the compressor.")
    parser.add_argument("--json", default=False, help="Prompt format JSON or not.")
    parser.add_argument(
        "--skip_system",
        default=False,
        help="Skip system prompts or not. Only valid if `json` is True.",
    )
    parser.add_argument(
        "--compressor_args",
        nargs="*",
        default=[],
        help="Additional arguments for the compressor.",
    )
    parser.add_argument(
        "--metrics", nargs="*", default=[], help="List of metrics to compute."
    )
    parser.add_argument(
        "--log_file",
        default=None,
        help="Output file to append results to. Prints on `stdout` if `None`.",
    )

    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    main()
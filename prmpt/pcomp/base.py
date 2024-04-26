import copy
from abc import ABC, abstractmethod

from .logger import logger
from .utils import DotDict, protected_runner

class PromptComp(ABC):
    """
    PromptComp is an abstract base class for prompt compression techniques.
    It defines the common structure and interface for prompt compression.
    This class inherits from ABC (Abstract Base Class).
    """
    
    def __init__(self, verbose: bool = False, metrics: list = [], protect_tag: str = None):
        """
        Initializes the PromptComp.

        Args:
            verbose (bool, optional): Flag indicating whether to enable verbose output. Defaults to False.
            metrics (list, optional): A list of metric names to evaluate during compression. Defaults to an empty list.
            protect_tag (str, optional): markup style tag string to indicate protected content that can't be deleted or modified. Defaults to `None`.
        """
        self.verbose = verbose
        self.metrics = metrics
        self.protect_tag = protect_tag

    @abstractmethod
    def compress(self, prompt: str) -> str:
        """
        Abstract method to run the prompt compression technique on a prompt.

        This method must be implemented by subclasses.

        Args:
            prompt (str): The prompt text.

        Returns:
            str: The compressed prompt text.
        """
        pass

    @protected_runner
    def run(self, prompt: str) -> str:
        """
        Wrapper around `compress` to do protected compression.

        Args:
            prompt (str): The prompt text.

        Returns:
            str: The protected compressed prompt text.
        """
        return self.compress(prompt)
    
    def run_json(self, json_data: list, skip_system: bool = False) -> dict:
        """
        Applies prompt compression to the JSON request object.

        Args:
            json_data (dict): The JSON data object.

        Returns:
            dict: The JSON data object with the content field replaced by the compressed prompt text.
        """
        comp_json_data = copy.deepcopy(json_data)

        for data in comp_json_data:
            if skip_system and data["role"] == "system":
                continue
            data["content"] = self.run(data["content"])
        return comp_json_data
    
    def run_langchain(self, langchain_data: list, skip_system: bool = False):
        """
        Runs the PromptComp on langchain chat data.

        Args:
            langchain_data (list): The langchain data containing 'type' and 'content' fields.
            skip_system (bool, optional): Whether to skip data with type 'system'. Defaults to False.

        Returns:
            list: The modified langchain data.

        """

        comp_langchain_data = copy.deepcopy(langchain_data)

        for data in comp_langchain_data:
            if skip_system and data.type == "system":
                continue
            data.content = self.run(data.content)

        return comp_langchain_data
    
    def __call__(
        self,
        prompt_data: list,
        skip_system: bool = False,
        json: bool = False,
        langchain: bool = False,
    ) -> list:
        """
        Process the prompt data and return compressed prompt data.

        Args:
            prompt_data: A list of prompt data.
            skip_system: A boolean indicating whether to skip system prompts. Default is False.
            json: A boolean indicating whether the prompt data is in JSON format. Default is False.
            langchain: A boolean indicating whether the prompt data is in langchain format. Default is False.

        Returns:
            A list of compressed prompt data.

        Raises:
            AssertionError: If skip_system is True and json is False.

        """

        assert not (json and langchain), "Data type can't be both json and langchain"

        if skip_system:
            assert (
                json or langchain
            ), "Can't skip system prompts without batched json format"

        if json:
            comp_prompt_data = self.run_json(prompt_data, skip_system)
        elif langchain:
            comp_prompt_data = self.run_langchain(prompt_data, skip_system)
        else:
            comp_prompt_data = self.run(prompt_data)

        metric_results = []
        for metric in self.metrics:
            if json or langchain:
                metric_result = metric.batch_run(
                    prompt_data, comp_prompt_data, skip_system, json, langchain
                )
            else:
                metric_result = metric.run(prompt_data, comp_prompt_data)

            metric_results.append(metric_result)

        if self.verbose:
            logger.info(f"Prompt Data Before: {prompt_data}")
            logger.info(f"Prompt Data After: {comp_prompt_data}")
            for metric_result in metric_results:
                for key in metric_result:
                    logger.info(f"{key}: {metric_result[key]:.3f}")

        result = DotDict()
        result.content = comp_prompt_data
        result.metrics = metric_results

        return result

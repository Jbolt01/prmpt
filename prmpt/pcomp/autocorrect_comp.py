from autocorrect import Speller

from prmpt.pcomp.base import PromptComp

class AutocorrectComp(PromptComp):
    """
    AutocorrectComp is a prompt compression technique that applies autocorrection to the prompt text.
    Correctly spelled words have less token count than incorrect ones. This is useful in scenarios where
    human client types the text.

    It inherits from the PromptComp base class.

    Example:
        >>> from prmpt.pcomp import AutocorrectComp
        >>> p_comp = AutocorrectComp()
        >>> res = p_comp("example prompt...")
        >>> compressed_prompt = res.content
    """

    def __init__(self, fast: bool = False, verbose: bool = False, metrics: list = []):
        """
        Initializes the AutocorrectComp.

        Args:
            fast (bool, optional): Flag indicating whether to use a fast autocorrect implementation. Defaults to False.
            verbose (bool, optional): Flag indicating whether to enable verbose output. Defaults to False.
            metrics (list, optional): A list of metric names to evaluate during compression. Defaults to an empty list.
        """
        super().__init__(verbose, metrics)
        self.spell = Speller(lang="en", fast=fast)

    def compress(self, prompt: str) -> str:
        """
        Applies autocorrection to the prompt text.

        Args:
            prompt (str): The prompt text.

        Returns:
            str: The compressed prompt text after applying autocorrection.
        """
        words = prompt.split()
        autocorrected_words = [self.spell(word) for word in words]
        comp_prompt = " ".join(autocorrected_words)
        return comp_prompt

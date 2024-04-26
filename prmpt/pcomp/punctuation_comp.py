import string

from prmpt.pcomp.base import PromptComp

class PunctuationComp(PromptComp):
    """
    PunctuationComp is a prompt compression technique that removes punctuation marks from the prompt.
    LLMs can infer punctuations themselves in most cases, so we canremove them.

    It inherits from the PromptComp base class.

    Example:
        >>> from prmpt.pcomp import PunctuationComp
        >>> p_compressor = PunctuationComp()
        >>> res = p_compressor("example prompt...")
        >>> compressed_prompt = res.content
    """

    def __init__(self, verbose: bool = False, metrics: list = [], **kwargs):
        """
        Initializes the PunctuationComp.

        Args:
            verbose (bool, optional): Flag indicating whether to enable verbose output. Defaults to False.
            metrics (list, optional): A list of metric names to evaluate during compression. Defaults to an empty list.
        """
        super().__init__(verbose, metrics, **kwargs)

    def compress(self, prompt: str) -> str:
        """
        Runs the prompt compression technique on the prompt.

        Args:
            prompt (str): The prompt text.

        Returns:
            str: The compressed prompt text with punctuation marks removed.
        """
        comp_prompt = prompt.translate(str.maketrans("", "", string.punctuation))
        return comp_prompt
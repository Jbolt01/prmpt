import tiktoken

from prmpt.metric.base import Metric

class TokenMetric(Metric):
    """
    TokenMetric is a metric that calculates the compression ratio based on the number of tokens reduced.
    It uses `tiktoken` to tokenize strings and count the number of tokens.

    It inherits from the Metric base class.

    Example:
        >>> from prmpt.metric import TokenMetric
        >>> metric = TokenMetric()
        >>> res = metric("default prompt...", "compressed prompt...")
    """
    
    def __init__(self, tokenizer: str = "cl100k_base"):
        """
        Initializes the TokenMetric.

        Args:
            tokenizer (str, optional): The tokenizer to use. Defaults to "cl100k_base".
        """
        super().__init__()
        self.tokenizer = tiktoken.get_encoding(tokenizer)
        self.key = "num_token_comp_ratio"

    def run(self, prompt_before: str, prompt_after: str) -> dict:
        """
        Calculates the compression ratio based on the number of tokens.

        Args:
            prompt_before (str): The text before the prompt.
            prompt_after (str): The text after the prompt.

        Returns:
            dict: A dictionary containing the compression ratio.
        """
        n_tokens_before = len(self.tokenizer.encode(prompt_before))
        n_tokens_after = len(self.tokenizer.encode(prompt_after))
        comp_ratio = (n_tokens_before - n_tokens_after) / n_tokens_before
        return {self.key: comp_ratio}

    def __call__(self, prompt_before: str, prompt_after: str) -> dict:
        """
        Calls the run method to calculate the compression ratio.

        Args:
            prompt_before (str): The text before the prompt.
            prompt_after (str): The text after the prompt.

        Returns:
            dict: A dictionary containing the compression ratio.
        """
        return self.run(prompt_before, prompt_after)
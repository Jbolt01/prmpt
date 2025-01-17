import numpy as np
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

from prmpt.pcomp.base import PromptComp

class EntropyComp(PromptComp):
    """
    EntropyComp is a prompt compression technique based on entropy values of tokens.
    A masked language model (`bert-base-cased` by default) is used to compute probabilities
    of observing the current token based on right and left context. These probability values
    are further used to compute the entropy values. Compressor then moves on to remove the
    tokens corresponding to lowest `p` percentile entropies.

    The intuition of this method is that the model can infill low entropy i.e. low surprise
    or highly probable tokens through the context.

    `EntropyComp` inherits from the PromptComp base class.

    Example:
        >>> from prmpt.pcomp import EntropyComp
        >>> p_compressor = EntropyComp(p=0.1)
        >>> res = p_compressor("example prompt...")
        >>> compressed_prompt = res.content
    """
    
    def __init__(
        self,
        model_name: str = "bert-base-cased",
        p: float = 0.1,
        verbose: bool = False,
        metrics: list = [],
        **kwargs,
    ):
        """
        Initializes the EntropyComp.

        Args:
            model_name (str, optional): The name of the pretrained masked language model. Defaults to "bert-base-cased".
            p (float, optional): The percentile cutoff value for selecting tokens. Defaults to `0.1`. Higher `p` means more compression.
            verbose (bool, optional): Flag indicating whether to enable verbose output. Defaults to False.
            metrics (list, optional): A list of metric names to evaluate during compression. Defaults to an empty list.
        """
        super().__init__(verbose, metrics, **kwargs)
        self.p = p * 100
        self.model_name = model_name
        self.load_mlm_model_tokenizer()

    def load_mlm_model_tokenizer(self):
        """
        Loads the masked language model and tokenizer.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForMaskedLM.from_pretrained(self.model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate_confidence_values(self, sentence: str) -> list:
        """
        Generates entropy values for each token in the sentence.

        Args:
            sentence (str): The input sentence.

        Returns:
            list: A list of tuples containing token IDs and their corresponding entropy values.
        """
        inputs = self.tokenizer.encode_plus(
            sentence, return_tensors="pt", add_special_tokens=False
        )
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits[0]

        probs = torch.softmax(logits, dim=-1)
        entropy_mapping = []
        for i, input_id in enumerate(input_ids[0].detach().cpu().numpy()):
            entropy = -torch.log2(probs[i, input_id]).detach().cpu().item()
            entropy_mapping.append((input_id, entropy))
        return entropy_mapping

    def percentile_cutoff_tokens(self, entropy_mapping: list) -> list:
        """
        Selects tokens with entropy values above a percentile cutoff.

        Args:
            entropy_mapping (list): A list of tuples containing token IDs and their corresponding entropy values.

        Returns:
            list: A list of selected token IDs.
        """
        surprise_cutoff = np.percentile([cm[1] for cm in entropy_mapping], self.p)
        filtered_tokens = [cm[0] for cm in entropy_mapping if cm[1] >= surprise_cutoff]
        return filtered_tokens
    
    def run_chunk(self, prompt: str) -> str:
        """
        Runs the prompt compression technique on a chunk of the prompt.

        Args:
            prompt (str): The chunk of the prompt.

        Returns:
            str: The compressed chunk of the prompt.
        """
        entropy_mapping = self.generate_confidence_values(prompt)
        filtered_tokens = self.percentile_cutoff_tokens(entropy_mapping)
        compressed_prompt = self.tokenizer.decode(filtered_tokens)
        return compressed_prompt
    
    def compress(self, prompt: str) -> str:
        """
        Runs the prompt compression technique on the prompt.
            Args:
            prompt (str): The prompt text.

        Returns:
            str: The compressed prompt text.
        """
        max_l = int(0.7 * self.model.config.max_position_embeddings)
        tokens = prompt.split()
        comp_prompt = ""
        for idx in range(0, len(tokens), max_l):
            part_prompt = " ".join(tokens[idx : idx + max_l])
            part_comp_prompt = self.run_chunk(part_prompt)
            comp_prompt += part_comp_prompt
        return comp_prompt

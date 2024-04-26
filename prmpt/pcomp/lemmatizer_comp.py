import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

from prmpt.pcomp.base import PromptComp

class LemmatizerComp(PromptComp):
    """
    LemmatizerComp is a prompt compression technique based on lemmatization.

    It inherits from the PromptComp base class.

    Example:
        >>> from prmpt.pcomp import LemmatizerComp
        >>> p_compressor = LemmatizerComp()
        >>> res = p_compressor("example prompt...")
        >>> compressed_prompt = res.content
    """

    def __init__(self, verbose: bool = False, metrics: list = []):
        """
        Initializes the LemmatizerComp.

        Args:
            verbose (bool, optional): Flag indicating whether to enable verbose output. Defaults to False.
            metrics (list, optional): A list of metric names to evaluate during compression. Defaults to an empty list.
        """
        super().__init__(verbose, metrics)
        self.lemmatizer = WordNetLemmatizer()
        nltk.download("averaged_perceptron_tagger")
        nltk.download("wordnet")

    def get_wordnet_pos(self, word: str) -> str:
        """
        Maps the POS tag from NLTK to WordNet POS tags.

        Args:
            word (str): The word to determine the POS tag.

        Returns:
            str: The WordNet POS tag.
        """
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {
            "J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV,
        }
        return tag_dict.get(tag, wordnet.NOUN)
    
    def compress(self, prompt: str) -> str:
        """
        Runs the lemmatizer prompt compression technique on the prompt.

        Args:
            prompt (str): The prompt text.

        Returns:
            str: The compressed prompt text.
        """
        words = prompt.split()
        lemmatized_words = [
            self.lemmatizer.lemmatize(word, self.get_wordnet_pos(word))
            for word in words
        ]
        comp_prompt = " ".join(lemmatized_words)
        return comp_prompt
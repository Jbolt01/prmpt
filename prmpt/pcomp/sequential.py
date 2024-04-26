from typing import Any, List

from prmpt.pcomp.base import PromptComp

from .utils import DotDict

class Sequential:
    """
    Sequential is a class that represents a sequential composition of prompt compression techniques.

    It applies a series of compression techniques in sequence to the prompt.

    Example:
        >>> comp1 = SomeCompressionTechnique()
        >>> comp2 = AnotherCompressionTechnique()
        >>> seq = Sequential(comp1, comp2)
        >>> compressed_prompt = seq(prompt)

    Args:
        *comps: Variable-length argument list of prompt compression techniques.

    Attributes:
        comps (list): A list of prompt compression techniques.
    """

    def __init__(self, *comps: PromptComp):
        """
        Initializes the Sequential object with the specified prompt compression techniques.

        Args:
            *comps: Variable-length argument list of prompt compressino techniques.
        """
        self.comps: List[PromptComp] = list(comps)

    def __call__(self, x: Any) -> Any:
        """
        Applies the sequential composition of prompt compression techniques to the prompt.

        Args:
            x (Any): The input prompt.

        Returns:
            Any: The compressed prompt after applying the sequential compression.
        """
        d = DotDict()
        d.content = x
        for comp in self.comps:
            d = comp(d.content)
        return d

    
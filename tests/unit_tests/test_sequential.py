from tests.unit_tests import utils
from prmpt.pcomp import (
    AutocorrectComp,
    LemmatizerComp,
    PunctuationComp,
    Sequential,
)


def test_sequential():
    prompt = utils.load_prompt("prompt1.txt")

    p_compressor = Sequential(
        LemmatizerComp(verbose=True),
        PunctuationComp(verbose=True),
        AutocorrectComp(verbose=True),
    )
    compressed_prompt = p_compressor(prompt)
    assert len(compressed_prompt) > 0, "Failed!"

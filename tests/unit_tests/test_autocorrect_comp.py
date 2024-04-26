from tests.unit_tests import utils
from prmpt.metric import BERTMetric, TokenMetric
from prmpt.pcomp import AutocorrectComp


def test_autocorrect_comp():
    prompt = utils.load_prompt("prompt1.txt")
    p_compressor = AutocorrectComp(
        verbose=True, metrics=[TokenMetric(), BERTMetric()]
    )
    compressed_prompt = p_compressor(prompt)
    assert len(compressed_prompt) > 0, "Failed!"
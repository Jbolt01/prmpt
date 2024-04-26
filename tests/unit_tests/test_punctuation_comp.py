from tests.unit_tests import utils
from prmpt.metric import TokenMetric
from prmpt.pcomp import PunctuationComp

def test_punctuation_comp():
    prompt = utils.load_prompt("prompt1.txt")
    p_compressor = PunctuationComp(verbose=True, metrics=[TokenMetric()])
    compressed_prompt = p_compressor(prompt)
    assert len(compressed_prompt) > 0, "Failed!"

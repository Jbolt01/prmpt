from tests.unit_tests import utils
from prmpt.metric import TokenMetric
from prmpt.pcomp import EntropyComp

def test_entropy_comp():
    prompt = utils.load_prompt("prompt1.txt")
    p_compressor = EntropyComp(verbose=True, p=0.1, metrics=[TokenMetric()])
    compressed_prompt = p_compressor(prompt)
    assert len(compressed_prompt) > 0, "Failed!"


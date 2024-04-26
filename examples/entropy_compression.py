from prmpt.metric import TokenMetric
from prmpt.pcomp import EntropyComp
from prmpt.viz import StringDiff


prompt = """The Belle Tout Lighthouse is a decommissioned lighthouse and British landmark located at Beachy Head, East Sussex, close to the town of Eastbourne."""
p_compressor = EntropyComp(verbose=False, p=0.1, metrics=[TokenMetric()])
compressed_prompt = p_compressor(prompt).content
sd = StringDiff()
sd(prompt, compressed_prompt)


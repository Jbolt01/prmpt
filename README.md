# prmpt: Prompt Compression For LLM Inference

## Overview

The `prmpt` library is designed to compress prompts to large language models (LLMs) efficiently, thereby optimizing token utilization, increasing inference speed, and reducing operational costs. This library supports various compression techniques and metrics to evaluate the efficacy of compression algorithms.

## Installation

To install the library, you can use the following command:

```bash
pip install prmpt
```

## Usage
### Basic Usage
You can use `prmpt` to compress prompts directly by creating an instance of a compression class and invoking it with a prompt:

```python
from prmpt.pcomp import AutocorrectComp

compressor = AutocorrectComp()
prompt = "Example prompt that needs to be compressed..."
compressed_prompt = compressor(prompt)
print(compressed_prompt)
```

### Advanced Usage
For more advanced usage, such as batch processing of prompts or using different compression techniques sequentially, refer to the following examples:
```python
from prmpt.pcomp import Sequential, PunctuationComp, LemmatizerComp

comp1 = PunctuationComp()
comp2 = LemmatizerComp()
seq = Sequential(comp1, comp2)

compressed_prompt = seq("This is a sample prompt with unnecessary punctuation...")
print(compressed_prompt)
```

### Command-Line Interface
`prmpt` also includes a CLI to process prompts from a file or direct input:
```python
python main.py "path/to/prompt_data.txt" AutocorrectComp --json --skip_system
```

## Features

### Compression Techniques

- **AutocorrectComp**: Utilizes autocorrection to minimize token count by correcting spelling errors.
- **EntropyComp**: Eliminates predictable tokens using entropy thresholds, enhancing model prediction efficiency.
- **LemmatizerComp**: Standardizes and potentially reduces token counts by converting words to their base forms.
- **PunctuationComp**: Removes superfluous punctuation, leveraging the model's ability to infer such elements.

### Metrics

- **BERTScoreMetric**: Assesses the semantic preservation between the original and compressed prompts using BERT embeddings, providing metrics like precision, recall, and F1 score.
- **TokenMetric**: Calculates the compression ratio by comparing token counts before and after compression, aiming for minimal loss of meaning with maximum reduction of tokens.
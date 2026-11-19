
# Swiss German Speech Recognition Using Fine-Tuned Whisper

## Project Overview

This project focuses on developing an Automatic Speech Recognition (ASR) system for Swiss German speech using OpenAI's pretrained Whisper Base model.

The model is fine-tuned using the SwissDial dataset, which contains Swiss German speech samples and their corresponding transcriptions across eight dialects.

The objective is to improve speech recognition performance for regional Swiss German dialects.

## Model Used

- **Model:** OpenAI Whisper Base
- **Pretrained model:** `openai/whisper-base`
- **Architecture:** Transformer-based Encoder-Decoder
- **Task:** Automatic Speech Recognition (Speech-to-Text)
- **Language setting:** German (`de`)
- **Fine-tuning framework:** Hugging Face Transformers
- **Training environment:** Google Colab
- **GPU:** NVIDIA Tesla T4
- **Training epochs:** 2

## Dataset

**Dataset:** SwissDial

The dataset contains Swiss German speech recordings with corresponding text transcriptions.

Eight dialects are included:

| Code | Dialect     |
| ---- | ----------- |
| ag   | Aargau      |
| be   | Bern        |
| bs   | Basel       |
| gr   | Graubünden |
| lu   | Lucerne     |
| sg   | St. Gallen  |
| vs   | Valais      |
| zh   | Zurich      |

### Original Dataset Split

| Split           |          Samples |
| --------------- | ---------------: |
| Training        |           18,475 |
| Validation      |            2,319 |
| Testing         |            2,401 |
| **Total** | **23,195** |

### Pilot Experiment

For the Colab fine-tuning experiment, a smaller subset was used:

- Training: 500 samples
- Validation: 100 samples
- Testing: 1,000 samples
- Test distribution: 125 samples per dialect
- Training duration: 2 epochs

The pilot test subset was sampled from the original test split.

## Methodology

1. Load and inspect the SwissDial dataset.
2. Prepare and preprocess audio recordings.
3. Convert audio to 16 kHz mono format.
4. Extract Whisper-compatible audio features.
5. Tokenize the corresponding text transcriptions.
6. Evaluate the pretrained Whisper Base model.
7. Fine-tune Whisper Base using the training subset.
8. Evaluate the fine-tuned model on the test subset.
9. Compare performance using Word Error Rate (WER) and Character Error Rate (CER).

## Evaluation Results

### Overall Performance

| Metric | Original Whisper | Fine-Tuned Whisper |
| ------ | ---------------: | -----------------: |
| WER    |           87.28% |             77.24% |
| CER    |           35.54% |             26.01% |

The fine-tuned model achieved:

- 11.50% relative reduction in WER.
- Approximately 26.81% relative reduction in CER.

These results indicate an improvement in recognition accuracy after fine-tuning.

**Note:** These are pilot experiment results based on 1,000 test samples, not a full-dataset evaluation.

## Repository Structure

```text
swiss-german-asr/
│
├── README.md
├── .gitignore
│
├── baseline_evaluation.py
├── check_audio_formats.py
├── convert_audio.py
├── inspect_audio.py
├── inspect_dataset.py
├── prepare_dataset.py
├── split_dataset.py
├── test_whisper.py
├── transcribe.py
├── verify_audio.py
│
├── notebooks/
│   └── SwissDial_Whisper_Finetuning_NewAccount.ipynb
│
└── results/
    ├── overall_metrics.csv
    └── dialect_metrics.csv
```

## Technologies Used

- Python
- OpenAI Whisper
- PyTorch
- Hugging Face Transformers
- Hugging Face Datasets
- Librosa
- Pandas
- Google Colab
- Git and GitHub

## Running the Project

Clone the repository:

```bash
git clone https://github.com/VrushaliAPoojary/swiss-german-asr.git
cd swiss-german-asr
```

Install dependencies using the requirements file (pip install -r requirements.txt).

Run the Python scripts from the project directory as required.

The fine-tuning notebook is available in the `notebooks/` directory.

## Limitations

- The reported fine-tuning experiment uses a pilot subset rather than the entire training and test datasets.
- Only two training epochs were used.
- The fine-tuned model checkpoint is not included in this repository.
- The original audio dataset is not included because of its size and licensing restrictions.
- Further training and evaluation are required before considering this a production-ready ASR system.

## Dataset Attribution

The SwissDial dataset is used for this research project.

Please refer to the original SwissDial dataset documentation and its **CC BY-NC 4.0** licence for attribution and permitted use. This project does not redistribute the original dataset.

## Author

**Vrushali A Poojary**

GitHub: [VrushaliAPoojary](https://github.com/VrushaliAPoojary)

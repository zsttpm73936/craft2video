# Craft2Video: Text-to-Code-to-Video Generation

This repository provides a **basic implementation** of the Craft2Video framework, which converts textual problem descriptions into executable **Manim animation code** and renders them as educational videos.

---

# 1. Overview

The current implementation supports a simplified pipeline:

```text
Text Input → Code Generation → Video Rendering
```

Specifically:

* A textual problem is given as input
* A large language model (LLM) is used to generate Manim code
* The generated code is executed to produce a visualization video

This repository focuses on demonstrating the **text-to-code-to-video workflow** described in the paper.

---

# 2. Repository Structure

The repository contains the following files and directories:

├── run.py                         # Main entry point for the pipeline
├── generate_code.py              # Core module: text → Manim code generation
├── generated_scene.py            # Auto-generated Manim script (overwritten each run)
├── example.py                    # Basic example script
├── example_scenes.py             # Example Manim scenes for reference
├── math.json                     # Sample math problems (input data)
│
├── manimlib/                     # Manim rendering engine (local implementation)
│   ├── __init__.py
│   ├── animation/                # Animation-related modules
│   ├── camera/                   # Camera system
│   ├── config.py                 # Configuration settings
│   ├── constants.py              # Global constants
│   ├── container/                # Base container classes
│   ├── mobject/                  # Core graphical objects
│   │   ├── geometry/             # Geometric primitives
│   │   ├── svg/                  # SVG-based objects
│   │   └── types/                # Specialized object types
│   ├── scene/                    # Scene definitions and rendering logic
│   ├── utils/                    # Utility functions
│   └── ...                       # Other internal Manim modules
│
├── docs/                         # Documentation (if provided)
│   └── (documentation files)
│
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup script
├── pyproject.toml                # Project configuration
│
├── dataset/                      # Dataset root directory
│   ├── physics_study.jsonl       # Core dataset for physics pilot study
│   ├── example_problem.jsonl     # Example physics problems (input format reference)
│   ├── example_samples.jsonl     # Sample instances illustrating data structure
│   ├── source.json               # Original source data for query construction
│   ├── query.json                # Processed query inputs for experiments
│   ├── test.json                 # Full test set used in evaluation
│   ├── testmini.json             # Reduced test subset for quick validation
│   ├── annot_testmini.json       # Annotated labels for testmini subset
│   │
│   ├── data_prepro/              # Data preprocessing scripts
│   │   ├── generate_caption.py   # Caption generation using ViT-GPT2
│   │   ├── generate_caption_bard.py  # Caption generation using Bard/VLM
│   │   ├── generate_text_easyocr.py  # OCR-based text extraction
│   │   └── utils.py              # Utility functions for preprocessing
│   │
│   ├── texts/                    # Intermediate multimodal text data
│   │   ├── captions/             # Generated image captions
│   │   │   ├── vitgpt2_captions.json  # Captions from ViT-GPT2
│   │   │   └── bard_captions.json     # Captions from Bard
│   │   ├── ocr/                  # OCR extracted text
│   │   │   └── easyocr_texts.json     # OCR results
│   │   └── merged/               # Combined multimodal textual inputs
│   │       └── merged_texts.json      # Final merged text features
│   │
│   ├── splits/                   # Dataset split definitions
│   │   ├── train_ids.json        # Training split indices
│   │   ├── val_ids.json          # Validation split indices
│   │   └── test_ids.json         # Test split indices
│   │
│   └── README.md                 # Dataset description and usage instructions


---

## File Descriptions

### `run.py`

* The main script to run the system
* Takes a text input and triggers code generation
* Calls `generate_code.py` internally

---

### `generate_code.py`

* Core module of the system
* Responsible for:

  * Constructing prompts
  * Calling the language model
  * Generating Manim code

---

### `generated_scene.py`

* Automatically generated output file
* Contains the Manim scene code
* Overwritten each time the system runs

---

### `example_scenes.py`

* Provides example Manim animations
* Used as references for code structure

---

### `math.json`

* Contains example mathematical problems
* Serves as a **minimal dataset for demonstration purposes**

---

### `manimlib/`

* Local copy of the Manim rendering engine
* Used to execute animation scripts and generate videos

---

# 3. Dataset Information









---

# 4. Installation

## Requirements

* Python ≥ 3.8

Install dependencies:

```bash
pip install -r requirements.txt
```

If Manim is not available in your environment:

```bash
pip install manim
```

---

# 5. How to Run (Reproducibility Instructions)

This section describes how to reproduce the main functionality of the repository.

---

## Step 1: Generate Manim Code

Run the main script:

```bash
python run.py
```

This step:

* Accepts a text input (or uses predefined input)
* Calls `generate_code.py`
* Produces a Manim script

Output:

```text
generated_scene.py
```

---

## Step 2: Inspect Generated Code

The generated animation code is saved in:

```text
generated_scene.py
```

You can review or modify it before rendering.

---

## Step 3: Render the Video

Run the generated script using Manim:

```bash
python generated_scene.py
```

or:

```bash
manim generated_scene.py GeneratedScene -p
```

---

## Step 4: Output

The rendered video will be saved in Manim’s default output directory, typically:

```text
media/videos/
```

---

# 6. Example Usage

Run:

```bash
python run.py
```

Example input:

```text
Draw the line y = 3x - 1 and mark the point (1,2)
```

The system will:

1. Generate corresponding Manim code
2. Save it as `generated_scene.py`
3. Render the animation video

---

# 7. Reproducibility Summary

To reproduce the results in this repository:

1. Use `math.json` as input data
2. Run `python run.py`
3. Render output via `generated_scene.py`

Key scripts:

* Entry point: `run.py`
* Code generation: `generate_code.py`
* Rendering: `generated_scene.py`

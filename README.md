# chatPDF
AI that answers from PDF using chatGPT. ([chatPDF](https://www.chatpdf.com/) clone)

# Project Task Description

In this project, you will develop a question-answering system similar to [chatPDF](https://www.chatpdf.com/), focused on research papers in the field of AI. Your system should be able to answer the following types of questions related to the input PDF file:

1. Direct query questions that can be matched to the text in the paragraph 

        e.g.
        "What is CDE?"
        "Which datasets are used for evaluation?"
2. Indirect query questions without specific keywords in the text 
        
        e.g.
        "Why should we use the proposed method?"
        
3. Identification of key references that inspire the proposed methodology in the paper.

## Command-Line Interface

Create a simple command-line interface for your system using the following format: `ChatPDF.py file.pdf`. Users should be able to ask questions through a text prompt.

## Requirements and Limitations

You are expected to use the ChatGPT API to complete this project, but other alternative large language models are also welcome. However, we will impose a limitation of using at most 800 tokens as input to ChatGPT for each question, as we aim to minimize costs.

## How To Run?

- Change `OPENAI_API_KEY` to your API Key.
- Install required Dependency with `pip`.
- Run python chatPDF.py test.py 

## Testing

Use `test.pdf` for testing, ask these questions:

Example Question 1:

    (1) what kind of neural network architecture is used in this paper?

    (2) what datasets have been used for evaluation

Example Question 2:

    (1) what are the main discoveries of this paper?

    (2) what is the key insight of the proposed method?
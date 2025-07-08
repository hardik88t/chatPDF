# chatPDF
AI that answers from PDF using chatGPT. ([chatPDF](https://www.chatpdf.com/) clone)
Here is Gemini API key: AIzaSyDhu_53or7bktMHSOeO39zY40NNebvDKmA
Use it instead of OpenAI API key for chatGPT.

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

Create a simple command-line interface for your system. Users should be able to ask questions through a text prompt.

## Requirements and Limitations

You are expected to use the ChatGPT API to complete this project, but other alternative large language models are also welcome. However, as we aim to minimize costs, make sure to do most of the processing on your side before sending the request to the API. for that you can limit the context to small number of tokens, like 800 tokens.

## Testing

For testing, ask these questions to bert_research_paper.pdf (16 pages):

Example Question 1:

    (1) what kind of neural network architecture is used in this paper?

    (2) what datasets have been used for evaluation

Example Question 2:

    (1) what are the main discoveries of this paper?

    (2) what is the key insight of the proposed method?

Similarly test ai_application_research_paper.pdf & ml_in_ai_research_paper.pdf by making appropriate questions.
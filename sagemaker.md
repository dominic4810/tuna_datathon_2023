# Sagemaker Setup

In this markdown file, we will describe how to setup the sagemaker endpoints for our project.
We use the following two foundation models from AWS Sagemaker:
1. `GPT-J 6B Embedding FP16`
1. `FLAN-T5 XL`


# FLAN-T5 XL
We use `FLAN-T5 XL` to perform question answering.
To set up the endpoint:
1. In Sagemaker Studio's Jumpstart, search for `FLAN-T5 XL`
2. Configure the endpoint under `Deployment Configuration`. We use the following configurations. Other options are left as default.
```json
{
    "SageMaker hosting instance": ml.p3.2xlarge,
    "Endpoint name": jumpstart-dft-flan-t5-xl-endpoint
}
```

# GPT-J 6B Embedding FP16
We use `GPT-J 6B Embedding FP16` to embed articles in swiss law and questions.
This allows us to match questions to certain law, and using these laws to prompt `FLAN-T5 XL`.
To set up the endpoint:
1. In Sagemaker Studio's Jumpstart, search for `GPT-J 6B Embedding FP16`
2. Configure the endpoint under `Deployment Configuration`. We use the following configurations. Other options are left as default.
```json
{
    "SageMaker hosting instance": ml.g5.2xlarge,
    "Endpoint name": jumpstart-dft-hf-gpt-j-6b-fp16-endpoint
}
```
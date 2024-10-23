# Efficiently Download Large Files into AWS S3 with Step Functions and Lambda

This project demonstrates how to efficiently download large files from an SFTP server and upload them to AWS S3 using AWS Step Functions and Lambda functions.

![Stepfunction graph](./stepfunctions_graph.svg)

## Article

For a detailed explanation of the architecture and implementation, check out my Medium article: [Efficiently Download Large Files into AWS S3 with Step Functions and Lambda](<https://medium.com/@tammura/efficiently-download-large-files-into-aws-s3-with-step-functions-and-lambda-2d33466336bd>).



## Prerequisites

Make sure you have the following installed:

- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [AWS CLI](https://aws.amazon.com/cli/)
- Python 3.12 or above

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/efficient-s3-download-step-functions.git
   cd efficient-s3-dwnload-step-functions
   ```
2. Create virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Configure AWS credentials
    ```bash
    aws configure
    ```
4. Build the stack using SAM
    ```bash
    aws build
    aws deploy --guided
    ```

## Conclusion
This project provides an efficient solution for downloading large files to AWS S3 using Step Functions and Lambda. Feel free to __explore__, __contribute__, and __suggest improvements__! Open pull requests and issues are welcome.
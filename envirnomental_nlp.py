from transformers import AutoTokenizer, AutoModelForSequenceClassification
import boto3
import torch
import os
from dotenv import load_dotenv

load_dotenv()

class ESGValidator:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("EnvironmentalBERT")
        self.model = AutoModelForSequenceClassification.from_pretrained("EnvironmentalBERT")
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
        )
        self.bucket = os.getenv('S3_BUCKET')

    def analyze_project(self, project_id):
        document = self.s3.get_object(Bucket=self.bucket, Key=f"{project_id}.pdf")['Body'].read()
        inputs = self.tokenizer(document.decode(), return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        return self._convert_to_esg_percentage(outputs.logits)

    def _convert_to_esg_percentage(self, logits):
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        return float(probabilities[0][1] * 100)
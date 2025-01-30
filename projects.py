from fastapi import APIRouter, UploadFile, HTTPException
from ..models.environmental_nlp import ESGValidator
from ..models.blockchain import BlockchainManager
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/projects", tags=["projects"])

nlp_processor = ESGValidator()
innovator_blockchain = BlockchainManager(
    os.getenv('BLOCKCHAIN_NODE_URL'),
    os.getenv('INNOVATOR_CONTRACT_ADDR'),
    'InnovatorContract'
)


@router.post("/submit")
async def submit_project(file: UploadFile):
    project_id = str(uuid.uuid4())

    # Save to S3
    nlp_processor.s3.upload_fileobj(file.file, nlp_processor.bucket, f"{project_id}.pdf")

    # ESG Analysis
    try:
        esg_score = nlp_processor.analyze_project(project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Blockchain Registration
    if esg_score >= float(os.getenv('MIN_ESG_SCORE')):
        try:
            innovator_blockchain.register_project(project_id, int(esg_score))
            return {"status": "approved", "project_id": project_id, "esg_score": esg_score}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Blockchain error: {str(e)}")
    return {"status": "rejected", "reason": "ESG score below minimum threshold"}
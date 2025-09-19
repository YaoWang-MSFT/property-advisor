from fastapi import APIRouter, Request, File, UploadFile
from pydantic import BaseModel
from typing import List
from app.ai.advisor import AdvisorAgent
from app.services.property_data_provider import get_property_data
from app.services.calculations import calculate_property_metrics
import os

router = APIRouter()

# Initialize the advisor agent (you may want to move this to a config file)
agent = AdvisorAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY", "your-api-key"),
    deployment_name=os.getenv("OPENAI_DEPLOYMENT_NAME", "your-deployment-name"),
    api_base=os.getenv("OPENAI_API_BASE")
)

class PropertyInsightRequest(BaseModel):
    address: str

class SimilarProperty(BaseModel):
    address: str

class PropertyInsightResponse(BaseModel):
    proper_address: str
    county: str
    zip_code: str
    state: str
    estimate_monthly_rent: float
    similar_properties: List[SimilarProperty]
    # Add property metrics
    cap_rate: float
    noi: float
    gross_income: float
    effective_gross_income: float
    vacancy_loss: float
    total_expenses: float
    expense_breakdown: dict

class ContractReviewResponse(BaseModel):
    summary: str
    highlights: List[str]
    warnings: List[str]
    suggestions: List[str]

class ContractReviewRequest(BaseModel):
    file_content: str

@router.post("/get_property_insight", response_model=PropertyInsightResponse)
async def get_property_insight(request: PropertyInsightRequest):
    # Get property data using the property data provider
    property_data = get_property_data(request.address)
    
    # Calculate property metrics using the data
    metrics = calculate_property_metrics(
        purchase_price=property_data.financial.current_market_value,
        annual_rental_income=property_data.financial.annual_rental_income,
        other_income=property_data.financial.other_monthly_income * 12,
        property_taxes=property_data.financial.monthly_property_taxes * 12 if property_data.financial.monthly_property_taxes else None,
        insurance=property_data.financial.monthly_insurance * 12 if property_data.financial.monthly_insurance else None,
        property_management=property_data.financial.monthly_property_management * 12 if property_data.financial.monthly_property_management else None,
        maintenance_repairs=property_data.financial.monthly_maintenance * 12 if property_data.financial.monthly_maintenance else None,
        utilities=property_data.financial.monthly_utilities * 12,
        vacancy_rate=property_data.market.vacancy_rate
    )
    
    return PropertyInsightResponse(
        proper_address=property_data.address.full_address,
        county=property_data.address.county,
        zip_code=property_data.address.zip_code,
        state=property_data.address.state,
        estimate_monthly_rent=property_data.financial.monthly_rent,
        similar_properties=[
            SimilarProperty(address="124 Main St, Anytown, CA 12345"),
            SimilarProperty(address="125 Main St, Anytown, CA 12345"),
            SimilarProperty(address="126 Main St, Anytown, CA 12345")
        ],
        # Include all calculated metrics
        cap_rate=metrics["cap_rate"],
        noi=metrics["noi"],
        gross_income=metrics["gross_income"],
        effective_gross_income=metrics["effective_gross_income"],
        vacancy_loss=metrics["vacancy_loss"],
        total_expenses=metrics["total_expenses"],
        expense_breakdown=metrics["expense_breakdown"]
    )

@router.post("/ai_contract_review", response_model=ContractReviewResponse)
async def ai_contract_review(request: ContractReviewRequest):
    # Use AdvisorAgent to analyze the contract
    analysis = agent.analyze_contract(request.file_content)
    
    return ContractReviewResponse(
        summary=analysis.get("summary", ""),
        highlights=analysis.get("highlights", []),
        warnings=analysis.get("warnings", []),
        suggestions=analysis.get("suggestions", [])
    )
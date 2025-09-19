from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class PropertyAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    county: str
    full_address: str

class PropertyDetails(BaseModel):
    property_type: str  # "single_family", "condo", "multi_family", etc.
    bedrooms: int
    bathrooms: float
    square_feet: int
    lot_size: Optional[float] = None
    year_built: Optional[int] = None
    parking_spaces: Optional[int] = None

class FinancialData(BaseModel):
    # Purchase/Market data
    current_market_value: float
    purchase_price: Optional[float] = None
    
    # Income data
    monthly_rent: float
    annual_rental_income: float
    other_monthly_income: float = 0.0  # parking, laundry, etc.
    
    # Expense data
    monthly_property_taxes: Optional[float] = None
    monthly_insurance: Optional[float] = None
    monthly_hoa_fees: float = 0.0
    monthly_property_management: Optional[float] = None
    monthly_maintenance: Optional[float] = None
    monthly_utilities: float = 0.0
    
    # Additional financial metrics
    property_tax_rate: Optional[float] = None
    cap_rate: Optional[float] = None
    cash_flow: Optional[float] = None

class MarketData(BaseModel):
    median_rent_per_sqft: Optional[float] = None
    average_rent_nearby: Optional[float] = None
    vacancy_rate: float = 0.05  # Default 5%
    rent_growth_rate: Optional[float] = None
    market_appreciation_rate: Optional[float] = None

class PropertyData(BaseModel):
    address: PropertyAddress
    details: PropertyDetails
    financial: FinancialData
    market: MarketData
    last_updated: datetime
    data_sources: List[str] = []

def get_property_data(address: Union[str, Dict[str, Any]]) -> PropertyData:
    """
    Retrieve comprehensive property data for cap rate calculation and analysis.
    
    Args:
        address: Property address as string or address components dict
        
    Returns:
        PropertyData object with all property information
    """
    # TODO: Implement actual data retrieval from multiple sources:
    # - MLS data
    # - Public records
    # - Rental listing sites (Zillow, Rent.com, etc.)
    # - Tax assessor data
    # - Market analytics APIs
    
    # Parse address if string
    if isinstance(address, str):
        # TODO: Implement address parsing logic
        parsed_address = {
            "street": "123 Main St",
            "city": "Anytown", 
            "state": "CA",
            "zip_code": "12345",
            "county": "Sample County"
        }
    else:
        parsed_address = address
    
    # Return dummy data for now
    return PropertyData(
        address=PropertyAddress(
            street=parsed_address.get("street", "123 Main St"),
            city=parsed_address.get("city", "Anytown"),
            state=parsed_address.get("state", "CA"),
            zip_code=parsed_address.get("zip_code", "12345"),
            county=parsed_address.get("county", "Sample County"),
            full_address=f"{parsed_address.get('street', '123 Main St')}, {parsed_address.get('city', 'Anytown')}, {parsed_address.get('state', 'CA')} {parsed_address.get('zip_code', '12345')}"
        ),
        details=PropertyDetails(
            property_type="single_family",
            bedrooms=3,
            bathrooms=2.0,
            square_feet=1500,
            lot_size=0.25,
            year_built=1995,
            parking_spaces=2
        ),
        financial=FinancialData(
            current_market_value=450000.0,
            purchase_price=430000.0,
            monthly_rent=2500.0,
            annual_rental_income=30000.0,
            other_monthly_income=100.0,
            monthly_property_taxes=562.50,  # ~1.5% annually
            monthly_insurance=125.0,        # ~0.3% annually
            monthly_hoa_fees=0.0,
            monthly_property_management=200.0,  # 8% of rent
            monthly_maintenance=250.0,      # 10% of rent
            monthly_utilities=50.0,
            property_tax_rate=0.015,
            cap_rate=6.2,
            cash_flow=1312.50
        ),
        market=MarketData(
            median_rent_per_sqft=1.67,
            average_rent_nearby=2400.0,
            vacancy_rate=0.05,
            rent_growth_rate=0.03,
            market_appreciation_rate=0.04
        ),
        last_updated=datetime.now(),
        data_sources=["dummy_data", "placeholder"]
    )
from typing import Optional

def calculate_property_metrics(
    purchase_price: float,
    annual_rental_income: float,
    # Income components
    other_income: float = 0.0,  # parking, laundry, storage, etc.
    
    # Operating expenses
    property_taxes: Optional[float] = None,
    insurance: Optional[float] = None,
    property_management: Optional[float] = None,
    maintenance_repairs: Optional[float] = None,
    utilities: float = 0.0,
    advertising_marketing: float = 0.0,
    legal_accounting: float = 0.0,
    landscaping: float = 0.0,
    pest_control: float = 0.0,
    other_expenses: float = 0.0,
    
    # Vacancy and collection loss
    vacancy_rate: float = 0.05,  # 5% default vacancy rate
    
    # Default percentages for estimates
    default_property_tax_rate: float = 0.015,  # 1.5% of property value
    default_insurance_rate: float = 0.003,     # 0.3% of property value
    default_management_rate: float = 0.08,     # 8% of gross income
    default_maintenance_rate: float = 0.10     # 10% of gross income
) -> dict:
    """
    Calculate the capitalization rate of a property.
    
    Cap Rate = Net Operating Income (NOI) / Purchase Price
    
    NOI = Gross Income - Operating Expenses
    Gross Income = Rental Income + Other Income - Vacancy Loss
    
    Args:
        purchase_price: The acquisition cost of the property
        annual_rental_income: Annual rental income from the property
        other_income: Additional income (parking, laundry, etc.)
        property_taxes: Annual property taxes (estimated if not provided)
        insurance: Annual insurance cost (estimated if not provided)
        property_management: Annual management fees (estimated if not provided)
        maintenance_repairs: Annual maintenance costs (estimated if not provided)
        utilities: Annual utility costs paid by owner
        advertising_marketing: Annual advertising/marketing costs
        legal_accounting: Annual legal and accounting fees
        landscaping: Annual landscaping costs
        pest_control: Annual pest control costs
        other_expenses: Other miscellaneous expenses
        vacancy_rate: Expected vacancy rate (default 5%)
        default_property_tax_rate: Default property tax rate if not provided
        default_insurance_rate: Default insurance rate if not provided
        default_management_rate: Default management fee rate if not provided
        default_maintenance_rate: Default maintenance rate if not provided
    
    Returns:
        dict: Contains cap_rate, noi, gross_income, total_expenses, and breakdown
    """
    
    # Calculate gross income
    gross_income = annual_rental_income + other_income
    vacancy_loss = gross_income * vacancy_rate
    effective_gross_income = gross_income - vacancy_loss
    
    # Estimate missing expenses using defaults
    if property_taxes is None:
        property_taxes = purchase_price * default_property_tax_rate
    
    if insurance is None:
        insurance = purchase_price * default_insurance_rate
    
    if property_management is None:
        property_management = effective_gross_income * default_management_rate
    
    if maintenance_repairs is None:
        maintenance_repairs = effective_gross_income * default_maintenance_rate
    
    # Calculate total operating expenses
    total_expenses = (
        property_taxes +
        insurance +
        property_management +
        maintenance_repairs +
        utilities +
        advertising_marketing +
        legal_accounting +
        landscaping +
        pest_control +
        other_expenses
    )
    
    # Calculate Net Operating Income (NOI)
    noi = effective_gross_income - total_expenses
    
    # Calculate Cap Rate
    cap_rate = (noi / purchase_price) * 100 if purchase_price > 0 else 0
    
    return {
        "cap_rate": round(cap_rate, 2),
        "noi": round(noi, 2),
        "gross_income": round(gross_income, 2),
        "effective_gross_income": round(effective_gross_income, 2),
        "vacancy_loss": round(vacancy_loss, 2),
        "total_expenses": round(total_expenses, 2),
        "expense_breakdown": {
            "property_taxes": round(property_taxes, 2),
            "insurance": round(insurance, 2),
            "property_management": round(property_management, 2),
            "maintenance_repairs": round(maintenance_repairs, 2),
            "utilities": round(utilities, 2),
            "advertising_marketing": round(advertising_marketing, 2),
            "legal_accounting": round(legal_accounting, 2),
            "landscaping": round(landscaping, 2),
            "pest_control": round(pest_control, 2),
            "other_expenses": round(other_expenses, 2)
        }
    }

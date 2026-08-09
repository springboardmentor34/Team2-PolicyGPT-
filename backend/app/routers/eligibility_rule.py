from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.eligibility_rule import (
    EligibilityRuleCreate,
    EligibilityRuleUpdate,
    EligibilityRuleResponse,
)
from app.services.eligibility_rule_service import (
    create_eligibility_rule_service,
    get_all_eligibility_rules_service,
    get_eligibility_rule_by_id_service,
    update_eligibility_rule_service,
    delete_eligibility_rule_service,
)

router = APIRouter(
    prefix="/eligibility-rules",
    tags=["Eligibility Rules"]
)


@router.post("/", response_model=EligibilityRuleResponse)
def create_eligibility_rule(rule: EligibilityRuleCreate, db: Session = Depends(get_db)):
    return create_eligibility_rule_service(db, rule)


@router.get("/", response_model=list[EligibilityRuleResponse])
def get_all_eligibility_rules(db: Session = Depends(get_db)):
    return get_all_eligibility_rules_service(db)


@router.get("/{rule_id}", response_model=EligibilityRuleResponse)
def get_eligibility_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = get_eligibility_rule_by_id_service(db, rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="Eligibility rule not found")
    return rule


@router.put("/{rule_id}", response_model=EligibilityRuleResponse)
def update_eligibility_rule(
    rule_id: int,
    rule: EligibilityRuleUpdate,
    db: Session = Depends(get_db)
):
    updated_rule = update_eligibility_rule_service(db, rule_id, rule)
    if updated_rule is None:
        raise HTTPException(status_code=404, detail="Eligibility rule not found")
    return updated_rule


@router.delete("/{rule_id}")
def delete_eligibility_rule(rule_id: int, db: Session = Depends(get_db)):
    deleted_rule = delete_eligibility_rule_service(db, rule_id)
    if deleted_rule is None:
        raise HTTPException(status_code=404, detail="Eligibility rule not found")
    return {"message": "Eligibility rule deleted successfully"}

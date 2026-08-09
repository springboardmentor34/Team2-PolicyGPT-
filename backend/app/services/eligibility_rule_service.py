from sqlalchemy.orm import Session
from app.repositories.eligibility_rule_repository import (
    create_eligibility_rule,
    get_all_eligibility_rules,
    get_eligibility_rule_by_id,
    update_eligibility_rule,
    delete_eligibility_rule,
)
from app.schemas.eligibility_rule import EligibilityRuleCreate, EligibilityRuleUpdate


def create_eligibility_rule_service(db: Session, rule: EligibilityRuleCreate):
    return create_eligibility_rule(db, rule)


def get_all_eligibility_rules_service(db: Session):
    return get_all_eligibility_rules(db)


def get_eligibility_rule_by_id_service(db: Session, rule_id: int):
    return get_eligibility_rule_by_id(db, rule_id)


def update_eligibility_rule_service(db: Session, rule_id: int, rule: EligibilityRuleUpdate):
    return update_eligibility_rule(db, rule_id, rule)


def delete_eligibility_rule_service(db: Session, rule_id: int):
    return delete_eligibility_rule(db, rule_id)

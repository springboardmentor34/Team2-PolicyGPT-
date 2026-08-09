from sqlalchemy.orm import Session
from app.models.eligibility_rule import EligibilityRule
from app.schemas.eligibility_rule import EligibilityRuleCreate, EligibilityRuleUpdate


def create_eligibility_rule(db: Session, rule: EligibilityRuleCreate):
    new_rule = EligibilityRule(**rule.model_dump())
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule


def get_all_eligibility_rules(db: Session):
    return db.query(EligibilityRule).all()


def get_eligibility_rule_by_id(db: Session, rule_id: int):
    return db.query(EligibilityRule).filter(EligibilityRule.id == rule_id).first()


def update_eligibility_rule(db: Session, rule_id: int, rule: EligibilityRuleUpdate):
    db_rule = get_eligibility_rule_by_id(db, rule_id)
    if db_rule is None:
        return None
    update_data = rule.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_rule, key, value)
    db.commit()
    db.refresh(db_rule)
    return db_rule


def delete_eligibility_rule(db: Session, rule_id: int):
    db_rule = get_eligibility_rule_by_id(db, rule_id)
    if db_rule is None:
        return None
    db.delete(db_rule)
    db.commit()
    return db_rule

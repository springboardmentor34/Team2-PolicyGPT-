from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class KeyMetrics(BaseModel):
    total_users: int
    active_users: int
    total_policies: int
    published_policies: int
    pending_policies: int
    approved_policies: int
    rejected_policies: int
    total_schemes: int
    policy_searches: int
    eligibility_checks: int
    policy_comparisons: int
    total_feedback: int

class TrendPoint(BaseModel):
    date: str
    count: int

class PolicyStatusDistribution(BaseModel):
    draft: int
    pending_approval: int
    approved: int
    rejected: int
    published: int

class CategoryDistribution(BaseModel):
    category: str
    count: int

class UsageActivity(BaseModel):
    searches: int
    eligibility_checks: int
    comparisons: int
    feedback: int
    notifications: int

class AIInsight(BaseModel):
    trend: str
    observation: str
    anomaly: str
    recommendation: str

class AnalyticsOverviewResponse(BaseModel):
    metrics: KeyMetrics
    policy_status_distribution: PolicyStatusDistribution
    policy_creation_trend: List[TrendPoint]
    scheme_category_distribution: List[CategoryDistribution]
    usage_activity: UsageActivity
    insights: AIInsight

class DepartmentKPIs(BaseModel):
    total_policies: int
    draft: int
    pending_approval: int
    approved: int
    rejected: int
    published: int
    total_schemes: int

class DepartmentAnalyticsResponse(BaseModel):
    department: str
    kpis: DepartmentKPIs
    policy_status_distribution: PolicyStatusDistribution
    policy_creation_trend: List[TrendPoint]
    policy_category_distribution: List[CategoryDistribution]
    scheme_category_distribution: List[CategoryDistribution]


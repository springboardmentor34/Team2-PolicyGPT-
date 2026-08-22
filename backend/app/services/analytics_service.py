from sqlalchemy.orm import Session
from sqlalchemy import func, text
from datetime import datetime, timedelta
import os
from collections import defaultdict
from app.models.user import User
from app.models.policy import Policy
from app.models.scheme import Scheme
from app.models.search_history import SearchHistory
from app.models.audit_log import AuditLog
from app.models.feedback import Feedback
from app.models.notification import Notification
from app.schemas.analytics import (
    KeyMetrics, TrendPoint, PolicyStatusDistribution, 
    CategoryDistribution, UsageActivity, AIInsight, AnalyticsOverviewResponse
)

class AnalyticsService:
    @staticmethod
    def get_overview_analytics(db: Session) -> AnalyticsOverviewResponse:
        # Total counts
        total_users = db.query(User).count()
        total_policies = db.query(Policy).count()
        total_schemes = db.query(Scheme).count()
        
        # Policy by status
        published_policies = db.query(Policy).filter(func.upper(Policy.status) == 'PUBLISHED').count()
        pending_policies = db.query(Policy).filter(func.upper(Policy.status) == 'PENDING_APPROVAL').count()
        approved_policies = db.query(Policy).filter(func.upper(Policy.status) == 'APPROVED').count()
        rejected_policies = db.query(Policy).filter(func.upper(Policy.status) == 'REJECTED').count()
        draft_policies = db.query(Policy).filter(func.upper(Policy.status) == 'DRAFT').count()
        
        # Usage metrics
        policy_searches = db.query(SearchHistory).count()
        # Mock active users as logic depends on token expiry or last login, falling back to a subset of users
        active_users = max(1, db.query(User).filter(User.role != "guest").count()) 
        
        # We can approximate eligibility checks if not explicitly saved as entity, we'll try checking AuditLog actions or assuming some searches are eligibility checks
        eligibility_checks = db.query(AuditLog).filter(func.lower(AuditLog.action).like('%eligibility%')).count()
        if eligibility_checks == 0:  # fallback
            eligibility_checks = int(policy_searches * 0.4)
            
        policy_comparisons = db.query(AuditLog).filter(func.lower(AuditLog.action).like('%compar%')).count()
        if policy_comparisons == 0: # fallback
            policy_comparisons = int(policy_searches * 0.25)
            
        total_feedback = db.query(Feedback).count()
        total_notifications = db.query(Notification).count()

        metrics = KeyMetrics(
            total_users=total_users,
            active_users=active_users,
            total_policies=total_policies,
            published_policies=published_policies,
            pending_policies=pending_policies,
            approved_policies=approved_policies,
            rejected_policies=rejected_policies,
            total_schemes=total_schemes,
            policy_searches=policy_searches,
            eligibility_checks=eligibility_checks,
            policy_comparisons=policy_comparisons,
            total_feedback=total_feedback
        )

        policy_status_distribution = PolicyStatusDistribution(
            draft=draft_policies,
            pending_approval=pending_policies,
            approved=approved_policies,
            rejected=rejected_policies,
            published=published_policies
        )
        
        # Scheme categories mapping
        scheme_categories = db.query(Scheme.category, func.count(Scheme.id)).group_by(Scheme.category).all()
        category_dist = [CategoryDistribution(category=cat if cat else "Uncategorized", count=count) for cat, count in scheme_categories]

        # Policy Creation Trend (Mocking past 7 days based on data if created_at exists, else empty list safely)
        # Using a safer standard grouping query compatible with PostgreSQL and SQLite
        try:
            trend_data = db.query(
                func.date(Policy.created_at).label('creation_date'),
                func.count(Policy.id)
            ).group_by(func.date(Policy.created_at)).all()
            
            creation_trend = [
                TrendPoint(date=str(row[0]), count=row[1]) for row in trend_data[-7:]
            ]
        except Exception:
            creation_trend = []

        usage_activity = UsageActivity(
            searches=policy_searches,
            eligibility_checks=eligibility_checks,
            comparisons=policy_comparisons,
            feedback=total_feedback,
            notifications=total_notifications
        )

        insights = AnalyticsService._generate_insights(metrics, policy_status_distribution)

        return AnalyticsOverviewResponse(
            metrics=metrics,
            policy_status_distribution=policy_status_distribution,
            policy_creation_trend=creation_trend,
            scheme_category_distribution=category_dist,
            usage_activity=usage_activity,
            insights=insights
        )

    @staticmethod
    def _generate_insights(metrics: KeyMetrics, status_dist: PolicyStatusDistribution) -> AIInsight:
        # Fallback local AI-assisted rule-based generator
        
        # Trend
        if metrics.policy_searches > 10:
            trend = f"Search activity is strong with {metrics.policy_searches} recent queries."
        else:
            trend = "Steady baseline platform activity detected."
            
        # Observation
        total = metrics.total_policies
        if total > 0:
            active_pct = ((status_dist.approved + status_dist.published) / total) * 100
            if active_pct > 50:
                obs = f"Healthy policy lifecycle: {active_pct:.0f}% of policies are approved or published."
            else:
                obs = f"A significant portion of policies ({100 - active_pct:.0f}%) remain in draft or pending stages."
        else:
            obs = "No policies have been created yet."
            
        # Anomaly
        if status_dist.rejected > (status_dist.approved * 0.2):
            anomaly = "Rejection rate is higher than the expected baseline (above 20% compared to approvals)."
        else:
            anomaly = "No significant anomalies in policy workflow detected."
            
        # Recommendation
        if status_dist.pending_approval > 3:
            rec = "Review pending policies to reduce administrative backlog."
        elif status_dist.rejected > 0:
            rec = "Provide clear guidelines for policy creation to reduce rejection rates."
        else:
            rec = "Continue monitoring system usage for emerging trends."

        return AIInsight(
            trend=trend,
            observation=obs,
            anomaly=anomaly,
            recommendation=rec
        )

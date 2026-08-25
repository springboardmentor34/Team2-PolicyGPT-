import sys
import os
from datetime import datetime, UTC

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal, engine
from app.database.base import Base

# Import all models so SQLAlchemy configures all mappers correctly
from app.models.user import User
from app.models.policy import Policy
from app.models.scheme import Scheme
from app.models.eligibility_rule import EligibilityRule
from app.models.notification import Notification
from app.models.feedback import Feedback
from app.models.report import Report
from app.models.audit_log import AuditLog
from app.models.search_history import SearchHistory
from app.auth.security import hash_password

# Ensure tables exist
Base.metadata.create_all(bind=engine)

from app.main import run_migrations
run_migrations()

def seed():
    db = SessionLocal()
    try:
        # 1. Create Default Official & Admin User if not exist
        official = db.query(User).filter(User.email == "official@india.gov.in").first()
        if not official:
            official = User(
                full_name="Rajesh Kumar (Ministry Officer)",
                email="official@india.gov.in",
                password=hash_password("official123"),
                role="government_official"
            )
            db.add(official)
            db.commit()
            db.refresh(official)

        admin = db.query(User).filter(User.email == "admin@india.gov.in").first()
        if not admin:
            admin = User(
                full_name="System Administrator",
                email="admin@india.gov.in",
                password=hash_password("admin123"),
                role="administrator"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

        # 2. Seed Published Policies
        db.query(AuditLog).delete()
        db.query(Policy).delete()
        policies_data = [
            {
                "title": "National Digital Health Mission Policy 2026",
                "description": "Comprehensive digital healthcare framework providing digital ABHA health IDs, unified health records, e-Pharmacies, and tele-consultation across all AIIMS & PHCs.",
                "category": "Healthcare",
                "department": "Ministry of Health & Family Welfare",
                "state": "All India",
                "status": "PUBLISHED",
                "created_by": official.id,
                "reviewed_by": admin.id,
            },
            {
                "title": "PM-KISAN Agricultural Subsidies Policy",
                "description": "Financial support of ₹6,000 per year directly transferred in 3 equal installments to small and marginal farmer families nationwide.",
                "category": "Agriculture",
                "department": "Ministry of Agriculture & Farmers Welfare",
                "state": "All India",
                "status": "PUBLISHED",
                "created_by": official.id,
                "reviewed_by": admin.id,
            },
            {
                "title": "National Education Policy (NEP) Skill Upgrade",
                "description": "Integration of vocational skill training, multi-disciplinary undergraduate degrees, credit transfer banks, and coding education from Grade 6.",
                "category": "Education",
                "department": "Ministry of Education",
                "state": "All India",
                "status": "PUBLISHED",
                "created_by": official.id,
                "reviewed_by": admin.id,
            },
            {
                "title": "Green Energy & Solar Rooftop Subsidy Policy 2026",
                "description": "Up to 40% central financial assistance subsidy for residential solar rooftop installations, net-metering benefits, and free green electricity up to 300 units.",
                "category": "Energy & Infrastructure",
                "department": "Ministry of New and Renewable Energy",
                "state": "All India",
                "status": "PUBLISHED",
                "created_by": official.id,
                "reviewed_by": admin.id,
            },
            {
                "title": "Startup India Innovation & Seed Support Policy",
                "description": "Collateral-free credit guarantees, tax exemption for 3 consecutive years, and seed capital grants up to ₹50 Lakhs for technology startups.",
                "category": "Commerce & Industry",
                "department": "Ministry of Commerce and Industry",
                "state": "All India",
                "status": "PUBLISHED",
                "created_by": official.id,
                "reviewed_by": admin.id,
            },
            {
                "title": "National Semiconductor & AI Mission Policy",
                "description": "Financial incentives up to 50% project cost for setting up semiconductor fabs, microchip design facilities, and sovereign AI compute infrastructure.",
                "category": "IT & Electronics",
                "department": "Ministry of Electronics and IT",
                "state": "All India",
                "status": "PUBLISHED",
                "created_by": official.id,
                "reviewed_by": admin.id,
            },
            {
                "title": "PM Gati Shakti National Master Plan Policy",
                "description": "Integrated multimodal connectivity platform synchronizing infrastructure development across Railways, Roadways, Ports, and Waterways.",
                "category": "Infrastructure",
                "department": "Ministry of Road Transport & Highways",
                "state": "All India",
                "status": "PUBLISHED",
                "created_by": official.id,
                "reviewed_by": admin.id,
            },
            {
                "title": "Production Linked Incentive (PLI) Scheme Policy",
                "description": "Financial incentives worth ₹1.97 Lakh Crore across 14 strategic sectors including electronics, EV batteries, solar modules, and pharmaceuticals.",
                "category": "Manufacturing & Trade",
                "department": "Ministry of Heavy Industries",
                "state": "All India",
                "status": "PUBLISHED",
                "created_by": official.id,
                "reviewed_by": admin.id,
            },
            {
                "title": "National Clean Air Programme (NCAP) Guidelines",
                "description": "Targeted 40% reduction in particulate matter concentration across 131 non-attainment cities through green transport and industrial emission norms.",
                "category": "Environment & Energy",
                "department": "Ministry of Environment, Forest and Climate Change",
                "state": "All India",
                "status": "PUBLISHED",
                "created_by": official.id,
                "reviewed_by": admin.id,
            },
            {
                "title": "Cyber Security & Data Governance Policy",
                "description": "National framework for critical information infrastructure protection, data privacy compliance, CERT-In incident reporting, and digital citizen protection.",
                "category": "IT & Electronics",
                "department": "Ministry of Electronics and IT",
                "state": "All India",
                "status": "PUBLISHED",
                "created_by": official.id,
                "reviewed_by": admin.id,
            }
        ]

        for p_info in policies_data:
            p = Policy(**p_info, published_at=datetime.now(UTC))
            db.add(p)
        db.commit()

        # 3. Seed Schemes (12 Comprehensive Welfare Schemes)
        db.query(EligibilityRule).delete()
        db.query(Scheme).delete()
        schemes_data = [
            {
                "title": "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
                "description": "The world's largest health assurance scheme providing a health cover of ₹5 Lakhs per family per year for secondary and tertiary care hospitalization to vulnerable families.",
                "category": "Healthcare",
                "department": "Ministry of Health & Family Welfare",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "Families listed under SECC database (Rural D1-D7 categories and Urban 11 occupational categories), Annual Income < ₹2.5 Lakhs.",
                "benefits": "₹5 Lakhs cashless health coverage per family per year, covers 1,949 medical procedures across empaneled hospitals."
            },
            {
                "title": "Pradhan Mantri Awas Yojana - Urban (PMAY-U)",
                "description": "Flagship housing scheme aimed at providing all-weather pucca houses to eligible urban households with basic civic infrastructure.",
                "category": "Housing & Urban",
                "department": "Ministry of Housing and Urban Affairs",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "EWS / LIG / MIG families with no existing pucca house anywhere in India. Annual household income < ₹18 Lakhs.",
                "benefits": "Interest subsidy up to 6.5% on housing loans up to ₹6 Lakhs, direct financial grant of ₹1.5 Lakhs per dwelling unit."
            },
            {
                "title": "Pradhan Mantri Mudra Yojana (PMMY)",
                "description": "Scheme for providing collateral-free loans up to ₹10 Lakhs to non-corporate, non-farm small/micro enterprises.",
                "category": "Finance & Business",
                "department": "Ministry of Finance",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "Any Indian citizen with a non-farm business plan in manufacturing, trading, or service sector. Age > 18 years.",
                "benefits": "Loans up to ₹50,000 (Shishu), ₹50,000 to ₹5 Lakhs (Kishore), and ₹5 Lakhs to ₹10 Lakhs (Tarun) without collateral."
            },
            {
                "title": "PM Vishwakarma Kaushal Samman Yojana",
                "description": "Central sector scheme to support traditional artisans and craftspeople with end-to-end holistic assistance.",
                "category": "Skill & Artisans",
                "department": "Ministry of Micro, Small and Medium Enterprises",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "Artisans working in 18 traditional trades (Carpenters, Blacksmiths, Goldsmiths, Potters, Tailors). One member per family.",
                "benefits": "Collateral-free credit support up to ₹3 Lakhs at 5% interest, ₹15,000 toolkit incentive, and stipend of ₹500/day during skill training."
            },
            {
                "title": "PM POSHAN Shakti Nirman (Mid-Day Meal)",
                "description": "National nutrition scheme providing hot cooked nutritious meals to children studying in government and government-aided primary schools.",
                "category": "Education & Nutrition",
                "department": "Ministry of Education",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "All children enrolled in Classes I to VIII in government, local body, and government-aided schools.",
                "benefits": "Free daily meal containing 450-700 calories and 12-20g of protein to promote school attendance and health."
            },
            {
                "title": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
                "description": "Comprehensive crop insurance scheme protecting farmers against crop failure due to non-preventable natural risks.",
                "category": "Agriculture",
                "department": "Ministry of Agriculture & Farmers Welfare",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "All farmers including sharecroppers and tenant farmers growing notified crops in notified areas.",
                "benefits": "Maximum premium rate of 2% for Kharif crops, 1.5% for Rabi crops, and 5% for commercial/horticultural crops with 100% claim settlement."
            },
            {
                "title": "Sukanya Samriddhi Yojana (Girl Child Welfare)",
                "description": "Government backed small savings scheme exclusively for the education and marriage expense security of a girl child.",
                "category": "Women & Child",
                "department": "Ministry of Women and Child Development",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "Girl child below 10 years of age. Maximum 2 accounts per family allowed.",
                "benefits": "High compound interest rate (8.2% p.a.), tax exemption under Section 80C, partial withdrawal at age 18 for higher education."
            },
            {
                "title": "Atal Pension Yojana (APY)",
                "description": "Guaranteed pension scheme for unorganized sector workers ensuring monthly income security after age 60.",
                "category": "Social Security",
                "department": "Ministry of Finance",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "Any Indian citizen in the unorganized sector aged between 18 and 40 years holding a bank account.",
                "benefits": "Guaranteed monthly pension of ₹1,000 to ₹5,000 after age 60, with pension continuation to spouse upon subscriber death."
            },
            {
                "title": "PM SVANidhi Scheme for Street Vendors",
                "description": "Special micro-credit facility providing affordable working capital loans to urban street vendors to resume livelihoods.",
                "category": "Employment & Livelihood",
                "department": "Ministry of Housing and Urban Affairs",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "Urban street vendors holding Vending Certificate / Identity Card or recommendation letter from Urban Local Body.",
                "benefits": "Collateral-free working capital loan of ₹10,000 (1st tranche), ₹20,000 (2nd tranche), and ₹50,000 (3rd tranche) with 7% interest subsidy."
            },
            {
                "title": "Pradhan Mantri Ujjwala Yojana (PMUY 2.0)",
                "description": "Flagship social welfare scheme providing deposit-free LPG connections to women from below poverty line households.",
                "category": "Energy & Social Welfare",
                "department": "Ministry of Petroleum and Natural Gas",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "Adult woman belonging to BPL household / SC / ST / Most Backward Classes with no existing LPG connection in household.",
                "benefits": "Free LPG connection with financial assistance of ₹1,600 per connection, first refill and hotplate free of cost."
            },
            {
                "title": "Stand-Up India Scheme",
                "description": "Promotes entrepreneurship at grassroot level among Women and SC/ST communities by facilitating bank loans.",
                "category": "Finance & Business",
                "department": "Ministry of Finance",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "SC/ST and/or woman entrepreneurs above 18 years of age setting up greenfield enterprises.",
                "benefits": "Bank loans between ₹10 Lakhs and ₹1 Crore for setting up manufacturing, services, trading, or agriculture-allied sector enterprises."
            },
            {
                "title": "National Apprenticeship Promotion Scheme (NAPS)",
                "description": "Initiative to promote apprenticeship training nationwide and incentivize employers to engage apprentices.",
                "category": "Skill & Youth",
                "department": "Ministry of Skill Development and Entrepreneurship",
                "state": "All India",
                "status": "Active",
                "eligibility_criteria": "Youth aged 14 years and above having completed minimum 5th standard to ITI/Diploma/Graduate.",
                "benefits": "Government shares 25% of prescribed stipend up to ₹1,500 per month per apprentice directly transferred via DBT."
            }
        ]

        for s_info in schemes_data:
            s = Scheme(**s_info)
            db.add(s)
        db.commit()

        # 4. Seed Sample Feedback entries
        if db.query(Feedback).count() == 0:
            sample_feedbacks = [
                Feedback(
                    user_name="Ravi",
                    rating=5,
                    message="Very useful",
                    subject="Feedback Rating: 5/5",
                    content="Very useful",
                    status="Open",
                    user_id=official.id
                ),
                Feedback(
                    user_name="Priya Sharma",
                    rating=5,
                    message="Great platform to compare government policies and eligibility rules.",
                    subject="Feedback Rating: 5/5",
                    content="Great platform to compare government policies and eligibility rules.",
                    status="Open"
                ),
                Feedback(
                    user_name="Amit Patel",
                    rating=4,
                    message="Easy to search schemes, please add more state-specific filter options.",
                    subject="Feedback Rating: 4/5",
                    content="Easy to search schemes, please add more state-specific filter options.",
                    status="Open"
                )
            ]
            db.add_all(sample_feedbacks)
            db.commit()

        print(f"Successfully seeded {len(policies_data)} policies, {len(schemes_data)} schemes, and sample feedback!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()

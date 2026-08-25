import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PolicyService, Policy } from '../../services/policy.service';
import { SchemeService, Scheme } from '../../services/scheme.service';

export interface EligibilityResult {
  isEligible: boolean;
  statusText: string;
  statusBadgeClass: string;
  reasons: string[];
  matchedPolicyTitle?: string;
  benefits?: string;
}

@Component({
  selector: 'app-eligibility-checker',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './eligibility-checker.html',
  styleUrl: './eligibility-checker.css'
})
export class EligibilityChecker implements OnInit {
  policies: Policy[] = [];
  schemes: Scheme[] = [];

  // Form Fields
  age: number | null = null;
  annualIncome: number | null = null;
  category: string = 'General';
  occupation: string = 'Employed';
  state: string = 'All India';
  selectedItemType: 'policy' | 'scheme' = 'policy';
  selectedItemId: number | null = null;

  result: EligibilityResult | null = null;
  isEvaluating = false;

  constructor(
    private policyService: PolicyService,
    private schemeService: SchemeService
  ) {}

  ngOnInit(): void {
    this.policyService.getPublishedPolicies().subscribe({
      next: (data) => this.policies = data,
      error: (err) => console.error(err)
    });

    this.schemeService.getSchemes().subscribe({
      next: (data) => this.schemes = data,
      error: (err) => console.error(err)
    });
  }

  evaluateEligibility(): void {
    if (this.age === null || this.age === undefined || this.annualIncome === null || this.annualIncome === undefined) {
      alert('Please fill in both Age and Annual Income fields.');
      return;
    }

    const currentAge = Number(this.age);
    const currentIncome = Number(this.annualIncome);
    const categoryName = this.category || 'General';
    const occupationName = this.occupation || 'Employed';

    this.isEvaluating = false;

    let reasons: string[] = [];
    let isEligible = true;
    const formattedIncome = new Intl.NumberFormat('en-IN').format(currentIncome);

    // Age Criteria Analysis
    if (currentAge < 18) {
      isEligible = false;
      reasons.push(`Applicant age of ${currentAge} years is below the standard adult eligibility age of 18 years for general schemes.`);
      reasons.push('Eligible for youth, student & child welfare programs (PM POSHAN, Sukanya Samriddhi, NEP Skill Initiative).');
    } else if (currentAge >= 60) {
      reasons.push(`Applicant age of ${currentAge} years qualifies for Senior Citizen social security & pension benefits (Atal Pension Yojana).`);
    } else {
      reasons.push(`Applicant age of ${currentAge} years meets standard adult eligibility criteria (18–60 years).`);
    }

    // Income & Social Category Analysis
    if (currentIncome <= 250000) {
      reasons.push(`Annual household income of ₹${formattedIncome} qualifies for SECC / BPL primary healthcare (Ayushman Bharat PM-JAY) & free gas connection (PMUY).`);
    } else if (currentIncome <= 600000) {
      reasons.push(`Annual household income of ₹${formattedIncome} qualifies under Economically Weaker Section (EWS) / LIG housing interest subsidies (PMAY-Urban).`);
    } else if (currentIncome <= 1800000) {
      reasons.push(`Annual household income of ₹${formattedIncome} qualifies under Middle Income Group (MIG) priority assistance.`);
    } else {
      reasons.push(`Annual income of ₹${formattedIncome} exceeds subsidized BPL/EWS income caps, but qualifies for collateral-free business loans (PMMY, Stand-Up India, Startup India).`);
    }

    // Occupation / Category Specific Matching
    if (occupationName.toLowerCase().includes('farmer') || occupationName.toLowerCase().includes('agriculture')) {
      reasons.push(`Occupation (${occupationName}): Direct eligibility for PM-KISAN ₹6,000/yr income support & PM Fasal Bima Yojana crop insurance.`);
    } else if (occupationName.toLowerCase().includes('self') || occupationName.toLowerCase().includes('entrepreneur')) {
      reasons.push(`Occupation (${occupationName}): Eligible for PM Mudra Yojana collateral-free loans up to ₹10 Lakhs.`);
    } else if (occupationName.toLowerCase().includes('student')) {
      reasons.push(`Occupation (${occupationName}): Eligible for National Apprenticeship Promotion Scheme (NAPS) stipends & NEP skill upgrades.`);
    }

    if (categoryName === 'SC' || categoryName === 'ST' || categoryName === 'OBC' || categoryName === 'EWS') {
      reasons.push(`Social Category (${categoryName}): Qualifies for affirmative action sub-schemes, Stand-Up India greenfield business loans & reduced margin money requirements.`);
    }

    // Target Item Selection Handling
    let title = 'All Active Government Schemes & Policies';
    let benefits = 'Access to official public welfare assistance, credit guarantees, health coverage & direct benefit transfers (DBT).';

    const itemId = this.selectedItemId ? Number(this.selectedItemId) : null;

    if (this.selectedItemType === 'policy' && itemId && !isNaN(itemId)) {
      const item = this.policies.find(p => p.id === itemId);
      if (item) {
        title = item.title;
        benefits = item.description || benefits;
      }
    } else if (this.selectedItemType === 'scheme' && itemId && !isNaN(itemId)) {
      const item = this.schemes.find(s => s.id === itemId);
      if (item) {
        title = item.title;
        benefits = item.benefits || item.description || benefits;
      }
    }

    this.result = {
      isEligible: isEligible,
      statusText: isEligible ? 'ELIGIBLE FOR ASSISTANCE' : 'SPECIAL YOUTH ELIGIBILITY APPLIES',
      statusBadgeClass: isEligible ? 'badge-success' : 'badge-danger',
      reasons: reasons,
      matchedPolicyTitle: title,
      benefits: benefits
    };
  }
}

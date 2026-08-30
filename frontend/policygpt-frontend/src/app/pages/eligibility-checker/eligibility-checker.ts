import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PolicyService, Policy } from '../../services/policy.service';
import { SchemeService, Scheme } from '../../services/scheme.service';
import { AnalyticsService } from '../../services/analytics.service';

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
    private schemeService: SchemeService,
    private analyticsService: AnalyticsService
  ) { }

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
    if (this.age === null || this.annualIncome === null) {
      alert('Please fill in both Age and Annual Income fields.');
      return;
    }

    const currentAge: number = this.age;
    const currentIncome: number = this.annualIncome;

    this.isEvaluating = true;
    setTimeout(() => {
      let reasons: string[] = [];
      let isEligible = true;

      // Age check
      if (currentAge < 18) {
        isEligible = false;
        reasons.push('Minimum applicant age requirement is 18 years.');
      } else {
        reasons.push(`Applicant age of ${currentAge} meets standard eligibility criteria.`);
      }

      // Income check
      if (currentIncome <= 600000) {
        reasons.push(`Annual income of ₹${currentIncome.toLocaleString('en-IN')} qualifies under Economically Weaker Section (EWS) / Priority tier.`);
      } else if (currentIncome <= 1200000) {
        reasons.push(`Annual income of ₹${currentIncome.toLocaleString('en-IN')} qualifies under Middle Income Group (MIG) tier.`);
      } else {
        reasons.push(`Annual income of ₹${currentIncome.toLocaleString('en-IN')} is above subsidized priority income limits for certain schemes.`);
      }

      // Selected item lookup
      let title = 'Selected Scheme / Policy';
      let benefits = 'Access to official government citizen benefits and direct assistance.';

      if (this.selectedItemType === 'policy' && this.selectedItemId) {
        const item = this.policies.find(p => p.id === Number(this.selectedItemId));
        if (item) {
          title = item.title;
          benefits = item.description || benefits;
        }
      } else if (this.selectedItemType === 'scheme' && this.selectedItemId) {
        const item = this.schemes.find(s => s.id === Number(this.selectedItemId));
        if (item) {
          title = item.title;
          benefits = item.benefits || item.description || benefits;
        }
      }

      this.result = {
        isEligible: isEligible,
        statusText: isEligible ? 'ELIGIBLE' : 'NOT ELIGIBLE',
        statusBadgeClass: isEligible ? 'badge-success' : 'badge-danger',
        reasons: reasons,
        matchedPolicyTitle: title,
        benefits: benefits
      };

      this.analyticsService.logEligibilityCheck(this.selectedItemId ? Number(this.selectedItemId) : 0).subscribe({
        error: err => console.warn('Eligibility logging failed', err)
      });

      this.isEvaluating = false;
    }, 400);
  }
}

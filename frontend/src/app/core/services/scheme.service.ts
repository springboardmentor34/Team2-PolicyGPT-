import { Injectable } from '@angular/core';
import { Observable, delay, of } from 'rxjs';
import { EligibilityRule, Scheme, SchemeCategory } from '../models/scheme.model';

export interface SchemeFilters {
  keyword?: string;
  category?: SchemeCategory | 'All';
  state?: string;
}

export interface EligibilityProfile {
  age: number;
  gender: 'Male' | 'Female' | 'Any';
  income: number;
  occupation: string;
  education: string;
  location: string;
  socialCategory: string;
  disabilityStatus: boolean;
}

/**
 * SchemeService — MOCK DATA ONLY (no real API calls yet).
 * Swap method bodies for HttpClient calls to FastAPI's Scheme
 * & Eligibility microservices when the backend is available.
 */
@Injectable({ providedIn: 'root' })
export class SchemeService {
  private mockSchemes: Scheme[] = [
    {
      id: 1,
      name: 'National Merit Scholarship',
      description: 'Financial assistance for meritorious students from economically weaker sections.',
      category: 'Scholarships',
      department: 'Department of School Education & Literacy',
      state: 'All India',
      status: 'Active',
      benefits: '₹12,000 per year for 4 years',
      eligibility: { minAge: 14, maxAge: 20, maxIncome: 350000, education: '10th Pass', gender: 'Any' },
      applicationDeadline: '2026-09-30',
    },
    {
      id: 2,
      name: 'PM Kisan Samman Nidhi',
      description: 'Direct income support of ₹6,000 per year to landholding farmer families.',
      category: 'Farmer Welfare',
      department: 'Department of Agriculture & Farmers Welfare',
      state: 'All India',
      status: 'Active',
      benefits: '₹6,000 per year in 3 instalments',
      eligibility: { minAge: 18, occupation: 'Farmer', gender: 'Any' },
      applicationDeadline: '2026-12-31',
    },
    {
      id: 3,
      name: 'Ayushman Bharat - PMJAY',
      description: 'Health insurance cover of ₹5 lakh per family per year for secondary and tertiary care.',
      category: 'Healthcare',
      department: 'National Health Authority',
      state: 'All India',
      status: 'Active',
      benefits: '₹5,00,000 health cover per family/year',
      eligibility: { maxIncome: 250000, gender: 'Any' },
      applicationDeadline: '2026-11-15',
    },
    {
      id: 4,
      name: 'Pradhan Mantri Awas Yojana',
      description: 'Interest subsidy on home loans for first-time home buyers in EWS/LIG categories.',
      category: 'Housing',
      department: 'Ministry of Housing & Urban Affairs',
      state: 'Gujarat',
      status: 'Active',
      benefits: 'Up to ₹2.67 lakh interest subsidy',
      eligibility: { maxIncome: 600000, gender: 'Any' },
      applicationDeadline: '2026-10-01',
    },
    {
      id: 5,
      name: 'Stand-Up India Scheme',
      description: 'Bank loans between ₹10 lakh and ₹1 crore for SC/ST and women entrepreneurs.',
      category: 'Business Support',
      department: 'Department of Financial Services',
      state: 'All India',
      status: 'Active',
      benefits: '₹10 lakh – ₹1 crore loan facility',
      eligibility: { minAge: 18, socialCategory: 'SC/ST/Women', gender: 'Any' },
      applicationDeadline: '2026-08-31',
    },
    {
      id: 6,
      name: 'Mahila Shakti Kendra',
      description: 'Skill development and community engagement support for rural women.',
      category: 'Women Empowerment',
      department: 'Department of Women & Child Development',
      state: 'All India',
      status: 'Active',
      benefits: 'Free skill training + stipend',
      eligibility: { minAge: 18, gender: 'Female' },
      applicationDeadline: '2026-09-15',
    },
    {
      id: 7,
      name: 'Indira Gandhi National Old Age Pension',
      description: 'Monthly pension for senior citizens living below the poverty line.',
      category: 'Senior Citizen Welfare',
      department: 'Ministry of Rural Development',
      state: 'All India',
      status: 'Active',
      benefits: '₹1,000 per month pension',
      eligibility: { minAge: 60, maxIncome: 200000, gender: 'Any' },
      applicationDeadline: '2026-12-31',
    },
    {
      id: 8,
      name: 'National Means-cum-Merit Scholarship',
      description: 'Scholarship to reduce dropout rate at the secondary stage for economically weaker students.',
      category: 'Student Schemes',
      department: 'Department of School Education & Literacy',
      state: 'All India',
      status: 'Active',
      benefits: '₹12,000 per annum',
      eligibility: { minAge: 12, maxAge: 17, maxIncome: 150000, education: '8th Pass', gender: 'Any' },
      applicationDeadline: '2026-09-20',
    },
    {
      id: 9,
      name: 'Deen Dayal Upadhyaya Grameen Kaushalya Yojana',
      description: 'Skill training and placement-linked employment programme for rural youth.',
      category: 'Employment Programs',
      department: 'Ministry of Rural Development',
      state: 'All India',
      status: 'Active',
      benefits: 'Free skill training + job placement',
      eligibility: { minAge: 15, maxAge: 35, gender: 'Any' },
      applicationDeadline: '2026-10-31',
    },
    {
      id: 10,
      name: 'Atal Pension Yojana',
      description: 'Guaranteed monthly pension after age 60 for workers in the unorganised sector.',
      category: 'Social Security',
      department: 'Department of Financial Services',
      state: 'All India',
      status: 'Active',
      benefits: '₹1,000 – ₹5,000 monthly pension',
      eligibility: { minAge: 18, maxAge: 40, gender: 'Any' },
      applicationDeadline: '2026-12-31',
    },
  ];

  getAll(): Observable<Scheme[]> {
    return of(this.mockSchemes).pipe(delay(300));
  }

  getById(id: number): Observable<Scheme | undefined> {
    return of(this.mockSchemes.find((s) => s.id === id)).pipe(delay(200));
  }

  search(filters: SchemeFilters): Observable<Scheme[]> {
    let results = [...this.mockSchemes];

    if (filters.keyword) {
      const kw = filters.keyword.toLowerCase();
      results = results.filter(
        (s) => s.name.toLowerCase().includes(kw) || s.description.toLowerCase().includes(kw)
      );
    }
    if (filters.category && filters.category !== 'All') {
      results = results.filter((s) => s.category === filters.category);
    }
    if (filters.state && filters.state !== 'All') {
      results = results.filter((s) => s.state === filters.state);
    }

    return of(results).pipe(delay(300));
  }

  checkEligibility(profile: EligibilityProfile): Observable<Scheme[]> {
    const matches = this.mockSchemes.filter((s) => this.matchesRule(profile, s.eligibility));
    return of(matches).pipe(delay(500));
  }

  private matchesRule(profile: EligibilityProfile, rule: EligibilityRule): boolean {
    if (rule.minAge != null && profile.age < rule.minAge) return false;
    if (rule.maxAge != null && profile.age > rule.maxAge) return false;
    if (rule.maxIncome != null && profile.income > rule.maxIncome) return false;
    if (rule.gender && rule.gender !== 'Any' && rule.gender !== profile.gender) return false;
    return true;
  }

  getCategories(): SchemeCategory[] {
    return [
      'Scholarships',
      'Farmer Welfare',
      'Healthcare',
      'Housing',
      'Business Support',
      'Women Empowerment',
      'Senior Citizen Welfare',
      'Student Schemes',
      'Employment Programs',
      'Social Security',
    ];
  }

  getStates(): string[] {
    return Array.from(new Set(this.mockSchemes.map((s) => s.state)));
  }
}

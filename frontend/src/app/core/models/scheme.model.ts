export type SchemeCategory =
  | 'Scholarships'
  | 'Farmer Welfare'
  | 'Healthcare'
  | 'Housing'
  | 'Business Support'
  | 'Women Empowerment'
  | 'Senior Citizen Welfare'
  | 'Student Schemes'
  | 'Employment Programs'
  | 'Social Security';

export interface EligibilityRule {
  minAge?: number;
  maxAge?: number;
  gender?: 'Male' | 'Female' | 'Any';
  maxIncome?: number;
  occupation?: string;
  education?: string;
  socialCategory?: string;
  disabilityAllowed?: boolean;
}

export interface Scheme {
  id: number;
  name: string;
  description: string;
  category: SchemeCategory;
  department: string;
  state: string;
  status: 'Active' | 'Draft' | 'Closed';
  benefits: string;
  eligibility: EligibilityRule;
  applicationDeadline: string;
}

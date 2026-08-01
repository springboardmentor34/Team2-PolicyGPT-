export type PolicyCategory =
  | 'Education'
  | 'Healthcare'
  | 'Agriculture'
  | 'Employment'
  | 'Finance'
  | 'Women & Child Welfare'
  | 'Housing'
  | 'Environment'
  | 'Digital Governance'
  | 'Infrastructure';

export type PolicyStatus = 'Active' | 'Draft' | 'Closed';

export interface Policy {
  id: number;
  title: string;
  description: string;
  category: PolicyCategory;
  department: string;
  ministry: string;
  state: string;
  status: PolicyStatus;
  publicationDate: string;
  tags: string[];
}

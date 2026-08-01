import { Injectable } from '@angular/core';
import { Observable, delay, of } from 'rxjs';
import { Policy, PolicyCategory } from '../models/policy.model';

export interface PolicyFilters {
  keyword?: string;
  category?: PolicyCategory | 'All';
  state?: string;
  status?: string;
}

/**
 * PolicyService — MOCK DATA ONLY (no real API calls yet).
 * Swap the bodies of these methods for HttpClient calls against
 * FastAPI's Policy microservice (see architecture diagram) later.
 */
@Injectable({ providedIn: 'root' })
export class PolicyService {
  private mockPolicies: Policy[] = [
    {
      id: 1,
      title: 'National Education Policy Implementation Framework',
      description: 'Guidelines for states to roll out the revised school curriculum, teacher training, and digital classrooms.',
      category: 'Education',
      department: 'Department of School Education & Literacy',
      ministry: 'Ministry of Education',
      state: 'All India',
      status: 'Active',
      publicationDate: '2025-04-10',
      tags: ['education', 'curriculum', 'schools'],
    },
    {
      id: 2,
      title: 'Ayushman Bharat Digital Health Mission Guidelines',
      description: 'Framework for creating digital health IDs and interoperable health records across hospitals.',
      category: 'Healthcare',
      department: 'National Health Authority',
      ministry: 'Ministry of Health & Family Welfare',
      state: 'All India',
      status: 'Active',
      publicationDate: '2025-02-18',
      tags: ['health', 'digital-id', 'hospitals'],
    },
    {
      id: 3,
      title: 'Soil Health Card Scheme Revision',
      description: 'Updated norms for issuing soil health cards to farmers every two cropping cycles.',
      category: 'Agriculture',
      department: 'Department of Agriculture & Farmers Welfare',
      ministry: 'Ministry of Agriculture',
      state: 'Gujarat',
      status: 'Active',
      publicationDate: '2025-01-05',
      tags: ['agriculture', 'soil', 'farmers'],
    },
    {
      id: 4,
      title: 'Startup India Employment Generation Policy',
      description: 'Tax incentives and compliance relaxations for startups hiring first-time job seekers.',
      category: 'Employment',
      department: 'Department for Promotion of Industry and Internal Trade',
      ministry: 'Ministry of Commerce & Industry',
      state: 'All India',
      status: 'Draft',
      publicationDate: '2025-06-22',
      tags: ['startup', 'jobs', 'employment'],
    },
    {
      id: 5,
      title: 'Priority Sector Lending Norms for MSMEs',
      description: 'Revised lending targets for banks to support micro, small and medium enterprises.',
      category: 'Finance',
      department: 'Department of Financial Services',
      ministry: 'Ministry of Finance',
      state: 'All India',
      status: 'Active',
      publicationDate: '2024-12-01',
      tags: ['finance', 'msme', 'lending'],
    },
    {
      id: 6,
      title: 'Beti Bachao Beti Padhao Extension Policy',
      description: 'Continuation of the scheme with added focus on girl child STEM education.',
      category: 'Women & Child Welfare',
      department: 'Department of Women & Child Development',
      ministry: 'Ministry of Women & Child Development',
      state: 'All India',
      status: 'Active',
      publicationDate: '2025-03-08',
      tags: ['women', 'child', 'education'],
    },
    {
      id: 7,
      title: 'Pradhan Mantri Awas Yojana Urban 2.0',
      description: 'Affordable housing policy extension for urban poor and middle-income groups.',
      category: 'Housing',
      department: 'Ministry of Housing & Urban Affairs',
      ministry: 'Ministry of Housing & Urban Affairs',
      state: 'Maharashtra',
      status: 'Active',
      publicationDate: '2025-05-14',
      tags: ['housing', 'urban', 'affordable'],
    },
    {
      id: 8,
      title: 'Single-Use Plastic Phase-Out Notification',
      description: 'Timeline and penalties for phasing out identified single-use plastic items.',
      category: 'Environment',
      department: 'Central Pollution Control Board',
      ministry: 'Ministry of Environment, Forest & Climate Change',
      state: 'All India',
      status: 'Active',
      publicationDate: '2024-10-30',
      tags: ['environment', 'plastic', 'pollution'],
    },
    {
      id: 9,
      title: 'Digital India Data Governance Framework',
      description: 'Guidelines for secure handling and sharing of non-personal government data.',
      category: 'Digital Governance',
      department: 'Ministry of Electronics and IT',
      ministry: 'Ministry of Electronics and IT',
      state: 'All India',
      status: 'Draft',
      publicationDate: '2025-07-02',
      tags: ['digital', 'data', 'governance'],
    },
    {
      id: 10,
      title: 'National Highways Land Acquisition Fast-Track Policy',
      description: 'Simplified compensation and dispute-resolution process for highway land acquisition.',
      category: 'Infrastructure',
      department: 'National Highways Authority of India',
      ministry: 'Ministry of Road Transport & Highways',
      state: 'Rajasthan',
      status: 'Closed',
      publicationDate: '2024-09-11',
      tags: ['infrastructure', 'highways', 'land'],
    },
  ];

  getAll(): Observable<Policy[]> {
    return of(this.mockPolicies).pipe(delay(300));
  }

  getById(id: number): Observable<Policy | undefined> {
    return of(this.mockPolicies.find((p) => p.id === id)).pipe(delay(200));
  }

  search(filters: PolicyFilters): Observable<Policy[]> {
    let results = [...this.mockPolicies];

    if (filters.keyword) {
      const kw = filters.keyword.toLowerCase();
      results = results.filter(
        (p) =>
          p.title.toLowerCase().includes(kw) ||
          p.description.toLowerCase().includes(kw) ||
          p.tags.some((t) => t.toLowerCase().includes(kw))
      );
    }
    if (filters.category && filters.category !== 'All') {
      results = results.filter((p) => p.category === filters.category);
    }
    if (filters.state && filters.state !== 'All') {
      results = results.filter((p) => p.state === filters.state);
    }
    if (filters.status && filters.status !== 'All') {
      results = results.filter((p) => p.status === filters.status);
    }

    return of(results).pipe(delay(300));
  }

  getCategories(): PolicyCategory[] {
    return [
      'Education',
      'Healthcare',
      'Agriculture',
      'Employment',
      'Finance',
      'Women & Child Welfare',
      'Housing',
      'Environment',
      'Digital Governance',
      'Infrastructure',
    ];
  }

  getStates(): string[] {
    return Array.from(new Set(this.mockPolicies.map((p) => p.state)));
  }
}

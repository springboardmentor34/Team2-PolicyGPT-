import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { SchemeService, Scheme } from '../../services/scheme.service';
import { AuthService, AuthUser } from '../../services/auth.service';

const FALLBACK_SCHEMES: Scheme[] = [
  {
    id: 1,
    title: "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
    description: "The world's largest health assurance scheme providing a health cover of ₹5 Lakhs per family per year for secondary and tertiary care hospitalization to vulnerable families.",
    category: "Healthcare",
    department: "Ministry of Health & Family Welfare",
    state: "All India",
    status: "Active",
    eligibility_criteria: "Families listed under SECC database (Rural D1-D7 categories and Urban 11 occupational categories), Annual Income < ₹2.5 Lakhs.",
    benefits: "₹5 Lakhs cashless health coverage per family per year, covers 1,949 medical procedures across empaneled hospitals."
  },
  {
    id: 2,
    title: "Pradhan Mantri Awas Yojana - Urban (PMAY-U)",
    description: "Flagship housing scheme aimed at providing all-weather pucca houses to eligible urban households with basic civic infrastructure.",
    category: "Housing & Urban",
    department: "Ministry of Housing and Urban Affairs",
    state: "All India",
    status: "Active",
    eligibility_criteria: "EWS / LIG / MIG families with no existing pucca house anywhere in India. Annual household income < ₹18 Lakhs.",
    benefits: "Interest subsidy up to 6.5% on housing loans up to ₹6 Lakhs, direct financial grant of ₹1.5 Lakhs per dwelling unit."
  },
  {
    id: 3,
    title: "Pradhan Mantri Mudra Yojana (PMMY)",
    description: "Scheme for providing collateral-free loans up to ₹10 Lakhs to non-corporate, non-farm small/micro enterprises.",
    category: "Finance & Business",
    department: "Ministry of Finance",
    state: "All India",
    status: "Active",
    eligibility_criteria: "Any Indian citizen with a non-farm business plan in manufacturing, trading, or service sector. Age > 18 years.",
    benefits: "Loans up to ₹50,000 (Shishu), ₹50,000 to ₹5 Lakhs (Kishore), and ₹5 Lakhs to ₹10 Lakhs (Tarun) without collateral."
  },
  {
    id: 4,
    title: "PM-KISAN Samman Nidhi Direct Transfer Scheme",
    description: "Direct income support of ₹6,000 per year to small and marginal farmer families across the country.",
    category: "Agriculture",
    department: "Ministry of Agriculture & Farmers Welfare",
    state: "All India",
    status: "Active",
    eligibility_criteria: "Small and marginal farmer families having cultivable land holding up to 2 hectares.",
    benefits: "₹6,000 per year transferred in 3 equal installments directly to bank account via DBT."
  },
  {
    id: 5,
    title: "PM Vishwakarma Kaushal Samman Yojana",
    description: "Central sector scheme to support traditional artisans and craftspeople with end-to-end holistic assistance.",
    category: "Skill & Artisans",
    department: "Ministry of Micro, Small and Medium Enterprises",
    state: "All India",
    status: "Active",
    eligibility_criteria: "Artisans working in 18 traditional trades (Carpenters, Blacksmiths, Goldsmiths, Potters, Tailors). One member per family.",
    benefits: "Collateral-free credit support up to ₹3 Lakhs at 5% interest, ₹15,000 toolkit incentive, and stipend of ₹500/day during skill training."
  },
  {
    id: 6,
    title: "Stand-Up India Scheme",
    description: "Promotes entrepreneurship at grassroot level among Women and SC/ST communities by facilitating bank loans.",
    category: "Finance & Business",
    department: "Ministry of Finance",
    state: "All India",
    status: "Active",
    eligibility_criteria: "SC/ST and/or woman entrepreneurs above 18 years of age setting up greenfield enterprises.",
    benefits: "Bank loans between ₹10 Lakhs and ₹1 Crore for setting up manufacturing, services, trading, or agriculture-allied sector enterprises."
  }
];

@Component({
  selector: 'app-scheme-list',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './scheme-list.html',
  styleUrl: './scheme-list.css'
})
export class SchemeList implements OnInit {
  schemes: Scheme[] = FALLBACK_SCHEMES;
  schemeForm: FormGroup;
  showForm = false;
  isEditing = false;
  currentEditingId: number | null = null;
  isLoading = false;
  isLoadingData = false;
  currentUser: AuthUser | null = null;

  get canManageSchemes(): boolean {
    if (!this.currentUser) return false;
    const r = (this.currentUser.role || '').toLowerCase();
    return r === 'government_official' || r === 'administrator' || r === 'official';
  }

  constructor(
    private fb: FormBuilder,
    private schemeService: SchemeService,
    private authService: AuthService
  ) {
    this.schemeForm = this.fb.group({
      title: ['', Validators.required],
      description: [''],
      category: [''],
      department: [''],
      eligibility_criteria: [''],
      benefits: [''],
      status: ['Active']
    });
  }

  ngOnInit(): void {
    this.currentUser = this.authService.getUser();
    this.authService.getCurrentUser().subscribe({
      next: (user) => this.currentUser = user,
      error: (err) => console.error(err)
    });
    this.loadSchemes();
  }

  loadSchemes(): void {
    this.schemeService.getSchemes().subscribe({
      next: (data) => {
        if (data && data.length > 0) {
          this.schemes = data;
        }
        this.isLoadingData = false;
      },
      error: (err) => {
        console.warn('Backend schemes fetch failed, using fallback schemes:', err);
        this.isLoadingData = false;
      }
    });
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
    if (!this.showForm) {
      this.resetForm();
    }
  }

  editScheme(scheme: Scheme): void {
    this.isEditing = true;
    this.showForm = true;
    this.currentEditingId = scheme.id;
    this.schemeForm.patchValue({
      title: scheme.title,
      description: scheme.description,
      category: scheme.category,
      department: scheme.department,
      eligibility_criteria: scheme.eligibility_criteria,
      benefits: scheme.benefits,
      status: scheme.status || 'Active'
    });
  }

  deleteScheme(id: number): void {
    if (confirm('Are you sure you want to delete this scheme?')) {
      this.schemeService.deleteScheme(id).subscribe({
        next: () => {
          this.schemes = this.schemes.filter(s => s.id !== id);
        },
        error: (err) => console.error(err)
      });
    }
  }

  onSubmit(): void {
    if (this.schemeForm.invalid) return;

    this.isLoading = true;
    if (this.isEditing && this.currentEditingId) {
      this.schemeService.updateScheme(this.currentEditingId, this.schemeForm.value).subscribe({
        next: (updatedScheme) => {
          const index = this.schemes.findIndex(s => s.id === this.currentEditingId);
          if (index !== -1) {
            this.schemes[index] = updatedScheme;
          }
          this.resetForm();
        },
        error: (err) => {
          console.error(err);
          this.isLoading = false;
        }
      });
    } else {
      this.schemeService.createScheme(this.schemeForm.value).subscribe({
        next: (newScheme) => {
          this.schemes.unshift(newScheme);
          this.resetForm();
        },
        error: (err) => {
          console.error(err);
          this.isLoading = false;
        }
      });
    }
  }

  resetForm(): void {
    this.showForm = false;
    this.isEditing = false;
    this.currentEditingId = null;
    this.isLoading = false;
    this.schemeForm.reset({ status: 'Active' });
  }
}

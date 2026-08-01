import { Component, OnInit, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';

import { HeaderComponent } from '../../shared/components/header/header.component';
import { SearchBarComponent } from '../../shared/components/search-bar/search-bar.component';
import { PolicyCardComponent } from '../../shared/components/policy-card/policy-card.component';
import { SchemeCardComponent } from '../../shared/components/scheme-card/scheme-card.component';
import { LoaderComponent } from '../../shared/components/loader/loader.component';

import { AuthService } from '../../core/services/auth.service';
import { PolicyService } from '../../core/services/policy.service';
import { SchemeService } from '../../core/services/scheme.service';
import { Policy } from '../../core/models/policy.model';
import { Scheme } from '../../core/models/scheme.model';

interface StatCard {
  icon: string;
  label: string;
  value: number;
  accent: string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatCardModule,
    MatFormFieldModule,
    MatSelectModule,
    HeaderComponent,
    SearchBarComponent,
    PolicyCardComponent,
    SchemeCardComponent,
    LoaderComponent,
  ],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent implements OnInit {
  loading = signal(true);

  allPolicies = signal<Policy[]>([]);
  allSchemes = signal<Scheme[]>([]);

  keyword = signal('');
  categoryFilter = signal('All');

  categories: string[] = ['All'];

  filteredPolicies = computed(() => {
    const kw = this.keyword().toLowerCase();

    return this.allPolicies().filter(
      (p) =>
        (this.categoryFilter() === 'All' ||
          p.category === this.categoryFilter()) &&
        (kw === '' ||
          p.title.toLowerCase().includes(kw) ||
          p.description.toLowerCase().includes(kw))
    );
  });

  recentSchemes = computed(() => this.allSchemes().slice(0, 3));

  recentPolicies = computed(() => this.filteredPolicies().slice(0, 4));

  stats = computed<StatCard[]>(() => [
    {
      icon: 'gavel',
      label: 'Total Policies',
      value: this.allPolicies().length,
      accent: 'navy',
    },
    {
      icon: 'volunteer_activism',
      label: 'Total Schemes',
      value: this.allSchemes().length,
      accent: 'teal',
    },
    {
      icon: 'fiber_new',
      label: 'Active Schemes',
      value: this.allSchemes().filter((s) => s.status === 'Active').length,
      accent: 'gold',
    },
    {
      icon: 'pending_actions',
      label: 'Draft Policies',
      value: this.allPolicies().filter((p) => p.status === 'Draft').length,
      accent: 'muted',
    },
  ]);

  constructor(
    public auth: AuthService,
    private policyService: PolicyService,
    private schemeService: SchemeService
  ) {}

  ngOnInit(): void {
    // ✅ FIX: service is available only after constructor
    this.categories = ['All', ...this.policyService.getCategories()];

    this.loading.set(true);

    this.policyService.getAll().subscribe((policies) => {
      this.allPolicies.set(policies);

      this.schemeService.getAll().subscribe((schemes) => {
        this.allSchemes.set(schemes);
        this.loading.set(false);
      });
    });
  }

  onSearch(term: string): void {
    this.keyword.set(term);
  }
}
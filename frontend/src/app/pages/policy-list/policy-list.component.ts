import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';

import { HeaderComponent } from '../../shared/components/header/header.component';
import { SearchBarComponent } from '../../shared/components/search-bar/search-bar.component';
import { PolicyCardComponent } from '../../shared/components/policy-card/policy-card.component';
import { LoaderComponent } from '../../shared/components/loader/loader.component';

import { PolicyService } from '../../core/services/policy.service';
import { Policy } from '../../core/models/policy.model';

@Component({
  selector: 'app-policy-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatSelectModule,
    HeaderComponent,
    SearchBarComponent,
    PolicyCardComponent,
    LoaderComponent,
  ],
  templateUrl: './policy-list.component.html',
  styleUrl: './policy-list.component.scss',
})
export class PolicyListComponent implements OnInit {
  loading = signal(true);
  policies = signal<Policy[]>([]);

  keyword = '';
  category = 'All';
  state = 'All';
  status = 'All';

  categories: string[] = ['All'];
  states: string[] = ['All'];
  statuses = ['All', 'Active', 'Draft', 'Closed'];

  constructor(private policyService: PolicyService) {}

  ngOnInit(): void {
    // Initialize after dependency injection
    this.categories = ['All', ...this.policyService.getCategories()];
    this.states = ['All', ...this.policyService.getStates()];

    this.runSearch();
  }

  runSearch(): void {
    this.loading.set(true);

    this.policyService
      .search({
        keyword: this.keyword,
        category: this.category as never,
        state: this.state,
        status: this.status,
      })
      .subscribe((res) => {
        this.policies.set(res);
        this.loading.set(false);
      });
  }

  onKeywordSearch(term: string): void {
    this.keyword = term;
    this.runSearch();
  }

  resetFilters(): void {
    this.keyword = '';
    this.category = 'All';
    this.state = 'All';
    this.status = 'All';

    this.runSearch();
  }
}
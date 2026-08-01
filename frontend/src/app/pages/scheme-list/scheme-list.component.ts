import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { MatIconModule } from '@angular/material/icon';

import { HeaderComponent } from '../../shared/components/header/header.component';
import { SearchBarComponent } from '../../shared/components/search-bar/search-bar.component';
import { SchemeCardComponent } from '../../shared/components/scheme-card/scheme-card.component';
import { LoaderComponent } from '../../shared/components/loader/loader.component';

import { SchemeService } from '../../core/services/scheme.service';
import { Scheme } from '../../core/models/scheme.model';

@Component({
  selector: 'app-scheme-list',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatButtonModule,
    MatTabsModule,
    MatIconModule,
    HeaderComponent,
    SearchBarComponent,
    SchemeCardComponent,
    LoaderComponent,
  ],
  templateUrl: './scheme-list.component.html',
  styleUrl: './scheme-list.component.scss',
})
export class SchemeListComponent implements OnInit {
  loading = signal(true);
  schemes = signal<Scheme[]>([]);

  keyword = '';
  category = 'All';

  categories: string[] = ['All'];

  // Eligibility checker
  checking = signal(false);
  checked = signal(false);
  eligibleSchemes = signal<Scheme[]>([]);

  eligibilityForm: FormGroup;

  constructor(
    private schemeService: SchemeService,
    private fb: FormBuilder
  ) {
    this.eligibilityForm = this.fb.group({
      age: [25, [Validators.required, Validators.min(0), Validators.max(120)]],
      gender: ['Any', Validators.required],
      income: [200000, [Validators.required, Validators.min(0)]],
      occupation: ['Salaried', Validators.required],
      education: ['Graduate', Validators.required],
      location: ['Urban', Validators.required],
      socialCategory: ['General', Validators.required],
      disabilityStatus: [false],
    });
  }

  ngOnInit(): void {
    // Initialize after Angular injects the service
    this.categories = ['All', ...this.schemeService.getCategories()];

    this.runSearch();
  }

  runSearch(): void {
    this.loading.set(true);

    this.schemeService
      .search({
        keyword: this.keyword,
        category: this.category as never,
      })
      .subscribe((res) => {
        this.schemes.set(res);
        this.loading.set(false);
      });
  }

  onKeywordSearch(term: string): void {
    this.keyword = term;
    this.runSearch();
  }

  checkEligibility(): void {
    if (this.eligibilityForm.invalid) {
      this.eligibilityForm.markAllAsTouched();
      return;
    }

    this.checking.set(true);

    const raw = this.eligibilityForm.getRawValue();

    this.schemeService
      .checkEligibility({
        age: raw.age!,
        gender: raw.gender as 'Male' | 'Female' | 'Any',
        income: raw.income!,
        occupation: raw.occupation!,
        education: raw.education!,
        location: raw.location!,
        socialCategory: raw.socialCategory!,
        disabilityStatus: !!raw.disabilityStatus,
      })
      .subscribe((matches) => {
        this.eligibleSchemes.set(matches);
        this.checking.set(false);
        this.checked.set(true);
      });
  }
}
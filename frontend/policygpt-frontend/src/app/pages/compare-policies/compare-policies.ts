import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PolicyService, Policy } from '../../services/policy.service';

@Component({
  selector: 'app-compare-policies',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './compare-policies.html',
  styleUrl: './compare-policies.css'
})
export class ComparePolicies implements OnInit {
  policies: Policy[] = [];
  selectedPolicyIds: (number | null)[] = [null, null, null, null];
  selectedPolicies: (Policy | null)[] = [null, null, null, null];
  isLoading = false;

  constructor(private policyService: PolicyService) {}

  ngOnInit(): void {
    this.fetchPolicies();
  }

  fetchPolicies(): void {
    this.isLoading = true;
    this.policyService.getPublishedPolicies().subscribe({
      next: (data) => {
        this.policies = data;
        // Auto select up to 4 policies by default if available
        for (let i = 0; i < 4; i++) {
          if (data[i]) {
            this.selectedPolicyIds[i] = data[i].id;
            this.selectedPolicies[i] = data[i];
          } else {
            this.selectedPolicyIds[i] = null;
            this.selectedPolicies[i] = null;
          }
        }
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Failed to load published policies', err);
        this.isLoading = false;
      }
    });
  }

  onPolicyChange(index: number): void {
    const id = Number(this.selectedPolicyIds[index]);
    if (id) {
      this.selectedPolicies[index] = this.policies.find(p => p.id === id) || null;
    } else {
      this.selectedPolicies[index] = null;
    }
  }

  clearSlot(index: number): void {
    this.selectedPolicyIds[index] = null;
    this.selectedPolicies[index] = null;
  }

  hasAnySelected(): boolean {
    return this.selectedPolicies.some(p => p !== null);
  }
}

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { PolicyService, Policy } from '../../services/policy.service';

@Component({
  selector: 'app-policy-list',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './policy-list.html',
  styleUrl: './policy-list.css'
})
export class PolicyList implements OnInit {
  policies: Policy[] = [];
  policyForm: FormGroup;
  showForm = false;
  isEditing = false;
  currentEditingId: number | null = null;
  isLoading = false;

  constructor(private fb: FormBuilder, private policyService: PolicyService) {
    this.policyForm = this.fb.group({
      title: ['', Validators.required],
      category: [''],
      department: [''],
      status: ['Draft']
    });
  }

  ngOnInit(): void {
    this.loadPolicies();
  }

  loadPolicies(): void {
    this.policyService.getPolicies().subscribe({
      next: (data) => {
        this.policies = data;
      },
      error: (err) => console.error(err)
    });
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
    if (!this.showForm) {
      this.resetForm();
    }
  }

  editPolicy(policy: Policy): void {
    this.isEditing = true;
    this.showForm = true;
    this.currentEditingId = policy.id;
    this.policyForm.patchValue({
      title: policy.title,
      category: policy.category,
      department: policy.department,
      status: policy.status
    });
  }

  deletePolicy(id: number): void {
    if (confirm('Are you sure you want to delete this policy?')) {
      this.policyService.deletePolicy(id).subscribe({
        next: () => {
          this.policies = this.policies.filter(p => p.id !== id);
        },
        error: (err) => console.error(err)
      });
    }
  }

  onSubmit(): void {
    if (this.policyForm.invalid) return;

    this.isLoading = true;
    if (this.isEditing && this.currentEditingId) {
      this.policyService.updatePolicy(this.currentEditingId, this.policyForm.value).subscribe({
        next: (updatedPolicy) => {
          const index = this.policies.findIndex(p => p.id === this.currentEditingId);
          if (index !== -1) {
            this.policies[index] = updatedPolicy;
          }
          this.resetForm();
        },
        error: (err) => {
          console.error(err);
          this.isLoading = false;
        }
      });
    } else {
      this.policyService.createPolicy(this.policyForm.value).subscribe({
        next: (newPolicy) => {
          this.policies.unshift(newPolicy);
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
    this.policyForm.reset({ status: 'Draft' });
  }
}

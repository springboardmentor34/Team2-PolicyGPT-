import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators, FormsModule } from '@angular/forms';
import { PolicyService, Policy } from '../../services/policy.service';
import { AuthService, AuthUser } from '../../services/auth.service';

@Component({
    selector: 'app-policy-approval',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule, FormsModule],
    templateUrl: './policy-approval.html',
    styleUrl: './policy-approval.css'
})
export class PolicyApproval implements OnInit {
    policies: Policy[] = [];
    isLoading = false;
    currentUser: AuthUser | null = null;

    // Metric Counts
    get pendingCount(): number {
        return this.policies.filter(p => p.status === 'PENDING_APPROVAL').length;
    }

    get approvedCount(): number {
        return this.policies.filter(p => p.status === 'APPROVED').length;
    }

    get rejectedCount(): number {
        return this.policies.filter(p => p.status === 'REJECTED').length;
    }

    get publishedCount(): number {
        return this.policies.filter(p => p.status === 'PUBLISHED').length;
    }

    // Dialog & Review states
    selectedPolicy: Policy | null = null;
    selectedDetails: any = {};
    selectedPolicyAuditLogs: any[] = [];
    showApproveDialog = false;
    showRejectDialog = false;
    showPublishDialog = false;
    showDetailsDialog = false;

    rejectionForm: FormGroup;
    approvalComment = '';

    constructor(
        private fb: FormBuilder,
        private policyService: PolicyService,
        private authService: AuthService
    ) {
        this.rejectionForm = this.fb.group({
            comment: ['', [Validators.required, Validators.minLength(5)]]
        });
    }

    ngOnInit(): void {
        this.currentUser = this.authService.getUser();
        this.authService.getCurrentUser().subscribe({
            next: (user) => {
                this.currentUser = user;
                this.loadPolicies();
            },
            error: (err) => {
                console.error('Failed to resolve currentUser profile', err);
                this.loadPolicies();
            }
        });
    }

    loadPolicies(): void {
        if (this.currentUser?.role?.toUpperCase() !== 'ADMINISTRATOR') {
            alert('Unauthorized access. Only Administrators can view this page.');
            return;
        }

        this.isLoading = true;
        this.policyService.getPolicies().subscribe({
            next: (data) => {
                this.policies = data;
                this.isLoading = false;
            },
            error: (err) => {
                console.error('Error fetching policies', err);
                this.isLoading = false;
            }
        });
    }

    get pendingPolicies(): Policy[] {
        return this.policies.filter(p => p.status === 'PENDING_APPROVAL');
    }

    get approvedPolicies(): Policy[] {
        return this.policies.filter(p => p.status === 'APPROVED');
    }

    get recentlyRejectedPolicies(): Policy[] {
        return this.policies.filter(p => p.status === 'REJECTED');
    }

    get recentlyPublishedPolicies(): Policy[] {
        return this.policies.filter(p => p.status === 'PUBLISHED');
    }

    parsePolicyDescription(desc: string | null | undefined): any {
        if (!desc) return {};
        try {
            if (desc.trim().startsWith('{')) {
                return JSON.parse(desc);
            }
        } catch (e) {
            console.warn("Failed to parse description:", e);
        }
        return {
            executive_summary: desc,
            purpose: desc,
            problem_addressed: 'Not provided',
            objectives: 'Not provided'
        };
    }

    formatBeneficiaries(val: any): string {
        if (!val) return 'N/A';
        if (Array.isArray(val)) {
            return val.join(', ');
        }
        return val.toString();
    }

    getSnippet(policy: Policy): string {
        if (!policy.description) return '';
        const details = this.parsePolicyDescription(policy.description);
        return details.executive_summary || policy.description;
    }

    openDetailsDialog(policy: Policy): void {
        this.selectedPolicy = policy;
        this.selectedDetails = this.parsePolicyDescription(policy.description);
        this.selectedPolicyAuditLogs = [];
        this.policyService.getAuditLogs(policy.id).subscribe({
            next: (logs) => {
                this.selectedPolicyAuditLogs = logs;
            },
            error: (err) => {
                console.warn("Failed to load audit logs:", err);
            }
        });
        this.showDetailsDialog = true;
    }

    closeDetailsDialog(): void {
        this.showDetailsDialog = false;
        this.selectedPolicy = null;
        this.selectedDetails = {};
        this.selectedPolicyAuditLogs = [];
    }

    downloadPolicy(url: string | null | undefined): void {
        if (url) {
            window.open(url, '_blank');
        }
    }

    openApproveDialog(policy: Policy): void {
        this.selectedPolicy = policy;
        this.approvalComment = '';
        this.showApproveDialog = true;
    }

    closeApproveDialog(): void {
        this.showApproveDialog = false;
        this.selectedPolicy = null;
    }

    confirmApprove(): void {
        if (!this.selectedPolicy) return;
        this.isLoading = true;

        this.policyService.approvePolicy(this.selectedPolicy.id, this.approvalComment).subscribe({
            next: (updatedPolicy) => {
                const index = this.policies.findIndex(p => p.id === updatedPolicy.id);
                if (index !== -1) {
                    this.policies[index] = updatedPolicy;
                } else {
                    this.loadPolicies();
                }
                alert('Policy approved successfully.');
                this.closeApproveDialog();
                this.isLoading = false;
            },
            error: (err) => {
                console.error(err);
                this.isLoading = false;
                alert(err.error?.detail || 'Failed to approve policy.');
            }
        });
    }

    openRejectDialog(policy: Policy): void {
        this.selectedPolicy = policy;
        this.rejectionForm.reset();
        this.showRejectDialog = true;
    }

    closeRejectDialog(): void {
        this.showRejectDialog = false;
        this.selectedPolicy = null;
    }

    confirmReject(): void {
        if (!this.selectedPolicy || this.rejectionForm.invalid) return;
        this.isLoading = true;

        const comment = this.rejectionForm.value.comment;
        this.policyService.rejectPolicy(this.selectedPolicy.id, comment).subscribe({
            next: (updatedPolicy) => {
                const index = this.policies.findIndex(p => p.id === updatedPolicy.id);
                if (index !== -1) {
                    this.policies[index] = updatedPolicy;
                } else {
                    this.loadPolicies();
                }
                alert('Policy rejected successfully.');
                this.closeRejectDialog();
                this.isLoading = false;
            },
            error: (err) => {
                console.error(err);
                this.isLoading = false;
                alert(err.error?.detail || 'Failed to reject policy.');
            }
        });
    }

    openPublishDialog(policy: Policy): void {
        this.selectedPolicy = policy;
        this.showPublishDialog = true;
    }

    closePublishDialog(): void {
        this.showPublishDialog = false;
        this.selectedPolicy = null;
    }

    confirmPublish(): void {
        if (!this.selectedPolicy) return;
        this.isLoading = true;

        this.policyService.publishPolicy(this.selectedPolicy.id).subscribe({
            next: (updatedPolicy) => {
                const index = this.policies.findIndex(p => p.id === updatedPolicy.id);
                if (index !== -1) {
                    this.policies[index] = updatedPolicy;
                }
                alert('Policy published successfully!');
                this.closePublishDialog();
                this.isLoading = false;
            },
            error: (err) => {
                console.error(err);
                this.isLoading = false;
                alert(err.error?.detail || 'Failed to publish policy.');
            }
        });
    }
}

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService, AuthUser } from '../../services/auth.service';
import { PolicyService, Policy } from '../../services/policy.service';
import { SchemeService, Scheme } from '../../services/scheme.service';
import { NotificationService, Notification } from '../../services/notification.service';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-citizen-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './citizen-dashboard.html',
  styleUrl: './citizen-dashboard.css',
})
export class CitizenDashboard implements OnInit {
  currentUser: AuthUser | null = null;
  recentPolicies: Policy[] = [];
  recentSchemes: Scheme[] = [];
  notifications: Notification[] = [];
  totalSchemesCount: number = 12;
  totalPoliciesCount: number = 11;

  constructor(
    private authService: AuthService,
    private policyService: PolicyService,
    private schemeService: SchemeService,
    private notificationService: NotificationService
  ) { }

  ngOnInit(): void {
    this.currentUser = this.authService.getUser();

    this.authService.getCurrentUser().subscribe({
      next: (user) => this.currentUser = user,
      error: (err) => console.warn('Failed to get user profile', err)
    });

    this.policyService.getPublishedPolicies().subscribe({
      next: (data) => {
        if (data && data.length > 0) {
          this.totalPoliciesCount = data.length;
          this.recentPolicies = data.slice(0, 5);
        } else {
          this.totalPoliciesCount = 11;
        }
      },
      error: (err) => {
        console.warn('Error fetching policies for dashboard:', err);
        this.totalPoliciesCount = 11;
      }
    });

    this.schemeService.getSchemes().subscribe({
      next: (data) => {
        if (data && data.length > 0) {
          this.totalSchemesCount = data.length;
          this.recentSchemes = data.slice(0, 5);
        } else {
          this.totalSchemesCount = 12;
        }
      },
      error: (err) => {
        console.warn('Error fetching schemes for dashboard:', err);
        this.totalSchemesCount = 12;
      }
    });

    this.notificationService.getNotifications().subscribe({
      next: (data) => this.notifications = data ? data.slice(0, 3) : [],
      error: (err) => console.warn('Error fetching notifications:', err)
    });
  }
}

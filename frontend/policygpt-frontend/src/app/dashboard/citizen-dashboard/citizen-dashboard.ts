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

  constructor(
    private authService: AuthService,
    private policyService: PolicyService,
    private schemeService: SchemeService,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    this.authService.getCurrentUser().subscribe({
      next: (user) => this.currentUser = user,
      error: (err) => console.error('Failed to get user', err)
    });

    this.policyService.getPolicies().subscribe({
      next: (data) => this.recentPolicies = data.slice(0, 5),
      error: (err) => console.error(err)
    });

    this.schemeService.getSchemes().subscribe({
      next: (data) => this.recentSchemes = data.slice(0, 5),
      error: (err) => console.error(err)
    });

    this.notificationService.getNotifications().subscribe({
      next: (data) => this.notifications = data.slice(0, 3),
      error: (err) => console.error(err)
    });
  }
}

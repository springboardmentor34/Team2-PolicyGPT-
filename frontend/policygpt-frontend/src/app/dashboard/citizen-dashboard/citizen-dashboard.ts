import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService, AuthUser } from '../../services/auth.service';
import { PolicyService, Policy } from '../../services/policy.service';
import { SchemeService, Scheme } from '../../services/scheme.service';
import { NotificationService, Notification } from '../../services/notification.service';
import { ReportService, Report, ReportSummary } from '../../services/report.service';
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

  // Report & Analytics State for Researcher Dashboard
  reports: Report[] = [];
  summary: ReportSummary | null = null;
  isLoadingSummary = true;
  showReportViewer = false;
  selectedReportTitle = '';
  selectedReportDate = '';
  selectedReportType = 'System Summary';

  constructor(
    private authService: AuthService,
    private policyService: PolicyService,
    private schemeService: SchemeService,
    private notificationService: NotificationService,
    private reportService: ReportService
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

    // Fetch Analytics Report Summary & Historical Reports
    this.reportService.getReportSummary().subscribe({
      next: (sumData) => {
        this.summary = sumData;
        this.isLoadingSummary = false;
      },
      error: (err) => {
        console.warn('Summary fetch error:', err);
        this.isLoadingSummary = false;
      }
    });

    this.reportService.getReports().subscribe({
      next: (data) => this.reports = data,
      error: (err) => console.warn('Error fetching reports:', err)
    });
  }

  get isGovernmentOfficial(): boolean {
    return this.currentUser?.role === 'government_official';
  }

  get isAdministrator(): boolean {
    return this.currentUser?.role === 'administrator';
  }

  get canApprovePolicies(): boolean {
    return this.isGovernmentOfficial || this.isAdministrator;
  }

  openReportViewer(report?: Report): void {
    if (report) {
      this.selectedReportTitle = report.title;
      this.selectedReportDate = report.created_at;
      this.selectedReportType = report.content || 'System Analytics Report';
    } else {
      this.selectedReportTitle = 'PolicyGPT Master Intelligence Summary Report';
      this.selectedReportDate = new Date().toISOString();
      this.selectedReportType = 'Executive Analytics & Performance Report';
    }
    this.showReportViewer = true;
  }

  closeReportViewer(): void {
    this.showReportViewer = false;
  }

  openPdfTab(): void {
    this.reportService.openPdfInNewTab();
  }

  downloadPdf(): void {
    this.reportService.downloadPdfReport();
  }

  downloadExcel(): void {
    this.reportService.downloadExcelReport();
  }
}

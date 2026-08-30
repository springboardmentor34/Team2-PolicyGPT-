import { Component, OnInit, ElementRef, ViewChild, AfterViewInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DepartmentAnalyticsService, DepartmentAnalyticsResponse } from '../../services/department-analytics.service';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
    selector: 'app-department-analytics',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './department-analytics.html',
    styleUrls: ['./department-analytics.css']
})
export class DepartmentAnalyticsComponent implements OnInit, AfterViewInit {
    departments: string[] = [];
    selectedDepartment: string = '';
    analyticsData: DepartmentAnalyticsResponse | null = null;
    loading: boolean = false;
    error: string | null = null;

    @ViewChild('statusChart') statusChartRef!: ElementRef;
    @ViewChild('creationChart') creationChartRef!: ElementRef;
    @ViewChild('policyCategoryChart') policyCategoryChartRef!: ElementRef;
    @ViewChild('schemeCategoryChart') schemeCategoryChartRef!: ElementRef;

    statusChart: Chart | null = null;
    creationChart: Chart | null = null;
    policyCategoryChart: Chart | null = null;
    schemeCategoryChart: Chart | null = null;

    constructor(
        private analyticsService: DepartmentAnalyticsService,
        private cdr: ChangeDetectorRef
    ) { }

    ngOnInit(): void {
        this.analyticsService.getDepartments().subscribe({
            next: (depts) => {
                this.departments = depts;
                if (depts.length > 0) {
                    this.selectedDepartment = depts[0];
                    this.loadDepartmentData();
                } else {
                    this.error = "No departments found in existing policies.";
                }
            },
            error: (err) => {
                console.error(err);
                this.error = "Failed to load departments list.";
            }
        });
    }

    ngAfterViewInit(): void {
        // Only attempt if not loading; if loading, we render later
        if (this.analyticsData) {
            this.initCharts();
        }
    }

    onDepartmentChange(): void {
        if (this.selectedDepartment) {
            this.loadDepartmentData();
        }
    }

    loadDepartmentData(): void {
        this.loading = true;
        this.error = null;
        this.analyticsService.getDepartmentAnalytics(this.selectedDepartment).subscribe({
            next: (data) => {
                this.analyticsData = data;
                this.loading = false;
                this.cdr.detectChanges();
                setTimeout(() => this.initCharts(), 100);
            },
            error: (err) => {
                console.error(err);
                this.loading = false;
                this.error = "Failed to load department analytics.";
            }
        });
    }

    initCharts(): void {
        if (!this.analyticsData) return;
        this.renderStatusChart();
        this.renderCreationChart();
        this.renderPolicyCategoryChart();
        this.renderSchemeCategoryChart();
    }

    renderStatusChart(): void {
        if (this.statusChart) this.statusChart.destroy();
        if (this.statusChartRef) {
            const ctx = this.statusChartRef.nativeElement.getContext('2d');
            const dist = this.analyticsData!.policy_status_distribution;

            // Do not render empty chart
            if (dist.draft + dist.pending_approval + dist.approved + dist.rejected + dist.published === 0) return;

            this.statusChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Draft', 'Pending', 'Approved', 'Rejected', 'Published'],
                    datasets: [{
                        data: [dist.draft, dist.pending_approval, dist.approved, dist.rejected, dist.published],
                        backgroundColor: ['#e0e0e0', '#fbc02d', '#4caf50', '#f44336', '#2196f3']
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
            });
        }
    }

    renderCreationChart(): void {
        if (this.creationChart) this.creationChart.destroy();
        if (this.creationChartRef) {
            const ctx = this.creationChartRef.nativeElement.getContext('2d');
            const trend = this.analyticsData!.policy_creation_trend;
            if (trend.length === 0) return;

            this.creationChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: trend.map(t => t.date),
                    datasets: [{
                        label: 'Policies Created',
                        data: trend.map(t => t.count),
                        fill: false, borderColor: 'rgba(54, 162, 235, 1)', tension: 0.1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }
    }

    renderPolicyCategoryChart(): void {
        if (this.policyCategoryChart) this.policyCategoryChart.destroy();
        if (this.policyCategoryChartRef) {
            const ctx = this.policyCategoryChartRef.nativeElement.getContext('2d');
            const cats = this.analyticsData!.policy_category_distribution;
            if (cats.length === 0) return;

            this.policyCategoryChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: cats.map(c => c.category),
                    datasets: [{
                        label: 'Policies per Category',
                        data: cats.map(c => c.count),
                        backgroundColor: 'rgba(33, 150, 243, 0.7)'
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
            });
        }
    }

    renderSchemeCategoryChart(): void {
        if (this.schemeCategoryChart) this.schemeCategoryChart.destroy();
        if (this.schemeCategoryChartRef) {
            const ctx = this.schemeCategoryChartRef.nativeElement.getContext('2d');
            const cats = this.analyticsData!.scheme_category_distribution;
            if (cats.length === 0) return;

            this.schemeCategoryChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: cats.map(c => c.category),
                    datasets: [{
                        label: 'Schemes per Category',
                        data: cats.map(c => c.count),
                        backgroundColor: 'rgba(19, 136, 8, 0.6)'
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
            });
        }
    }
}

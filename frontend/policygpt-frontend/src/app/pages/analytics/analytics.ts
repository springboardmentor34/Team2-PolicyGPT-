import { Component, OnInit, ElementRef, ViewChild, AfterViewInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AnalyticsService, AnalyticsOverviewResponse } from '../../services/analytics.service';
import { Chart, registerables } from 'chart.js';
import { HttpErrorResponse } from '@angular/common/http';

Chart.register(...registerables);

@Component({
    selector: 'app-analytics',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './analytics.html',
    styleUrls: ['./analytics.css']
})
export class AnalyticsComponent implements OnInit, AfterViewInit {
    analyticsData: AnalyticsOverviewResponse | null = null;
    loading: boolean = true;
    error: string | null = null;

    @ViewChild('statusChart') statusChartRef!: ElementRef;
    @ViewChild('creationChart') creationChartRef!: ElementRef;
    @ViewChild('usageChart') usageChartRef!: ElementRef;
    @ViewChild('schemeChart') schemeChartRef!: ElementRef;

    statusChart: Chart | null = null;
    creationChart: Chart | null = null;
    usageChart: Chart | null = null;
    schemeChart: Chart | null = null;

    constructor(
        private analyticsService: AnalyticsService,
        private cdr: ChangeDetectorRef
    ) { }

    ngOnInit(): void {
        this.loadAnalyticsData();
    }

    ngAfterViewInit(): void {
        // Only attempt if not loading; if loading, we render later
        if (this.analyticsData) {
            this.initCharts();
        }
    }

    loadAnalyticsData(): void {
        this.loading = true;
        this.error = null;
        this.analyticsService.getAnalyticsOverview().subscribe({
            next: (data) => {
                this.analyticsData = data;
                this.loading = false;
                this.cdr.detectChanges();
                setTimeout(() => this.initCharts(), 100);
            },
            error: (err: HttpErrorResponse) => {
                console.error('Error fetching analytics:', err);
                if (err.status === 401) {
                    this.error = 'Your session has expired. Please log in again.';
                } else if (err.status === 403) {
                    this.error = 'You do not have permission to view administrative analytics.';
                } else if (err.status === 500) {
                    this.error = 'Analytics service is temporarily unavailable.';
                } else {
                    this.error = 'Unable to connect to the PolicyGPT server.';
                }
                this.loading = false;
                this.cdr.detectChanges();
            }
        });
    }

    fetchData(period: string): void {
        this.loadAnalyticsData();
    }

    initCharts(): void {
        if (!this.analyticsData) return;

        this.renderStatusChart();
        this.renderCreationChart();
        this.renderUsageChart();
        this.renderSchemeChart();
    }

    renderStatusChart(): void {
        if (this.statusChart) this.statusChart.destroy();

        if (this.statusChartRef) {
            const ctx = this.statusChartRef.nativeElement.getContext('2d');
            const dist = this.analyticsData!.policy_status_distribution;

            this.statusChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Draft', 'Pending', 'Approved', 'Rejected', 'Published'],
                    datasets: [{
                        label: 'Policies',
                        data: [dist.draft, dist.pending_approval, dist.approved, dist.rejected, dist.published],
                        backgroundColor: [
                            '#e0e0e0', // grey
                            '#fbc02d', // yellow
                            '#4caf50', // green
                            '#f44336', // red
                            '#2196f3'  // blue
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
        }
    }

    renderCreationChart(): void {
        if (this.creationChart) this.creationChart.destroy();

        if (this.creationChartRef) {
            const ctx = this.creationChartRef.nativeElement.getContext('2d');
            const trend = this.analyticsData!.policy_creation_trend;

            const labels = trend.map(t => t.date);
            const data = trend.map(t => t.count);

            this.creationChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Policies Created',
                        data: data,
                        fill: false,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }

    renderUsageChart(): void {
        if (this.usageChart) this.usageChart.destroy();

        if (this.usageChartRef) {
            const ctx = this.usageChartRef.nativeElement.getContext('2d');
            const usage = this.analyticsData!.usage_activity;

            this.usageChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Searches', 'Eligibility Checks', 'Comparisons', 'Feedback'],
                    datasets: [{
                        label: 'Total Activity',
                        data: [usage.searches, usage.eligibility_checks, usage.comparisons, usage.feedback],
                        backgroundColor: 'rgba(255, 153, 51, 0.7)' // saffron
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }

    renderSchemeChart(): void {
        if (this.schemeChart) this.schemeChart.destroy();

        if (this.schemeChartRef) {
            const ctx = this.schemeChartRef.nativeElement.getContext('2d');
            const schemeCat = this.analyticsData!.scheme_category_distribution;

            const labels = schemeCat.map(c => c.category);
            const data = schemeCat.map(c => c.count);

            this.schemeChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Schemes per Category',
                        data: data,
                        backgroundColor: 'rgba(19, 136, 8, 0.6)' // green
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }
}

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReportService, Report, ReportSummary } from '../../services/report.service';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './reports.html',
  styleUrl: './reports.css'
})
export class Reports implements OnInit {
  reports: Report[] = [];
  summary: ReportSummary | null = null;
  isLoadingSummary = true;

  // Report Preview Modal State
  showReportViewer = false;
  selectedReportTitle = '';
  selectedReportDate = '';
  selectedReportType = 'System Summary';

  constructor(private reportService: ReportService) {}

  ngOnInit(): void {
    this.reportService.getReports().subscribe({
      next: (data) => this.reports = data,
      error: (err) => console.error(err)
    });

    this.reportService.getReportSummary().subscribe({
      next: (sumData) => {
        this.summary = sumData;
        this.isLoadingSummary = false;
      },
      error: (err) => {
        console.warn("Summary fetch error:", err);
        this.isLoadingSummary = false;
      }
    });
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

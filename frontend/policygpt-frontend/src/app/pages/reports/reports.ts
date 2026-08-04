import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReportService, Report } from '../../services/report.service';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './reports.html',
  styleUrl: './reports.css'
})
export class Reports implements OnInit {
  reports: Report[] = [];

  constructor(private reportService: ReportService) {}

  ngOnInit(): void {
    this.reportService.getReports().subscribe({
      next: (data) => this.reports = data,
      error: (err) => console.error(err)
    });
  }
}

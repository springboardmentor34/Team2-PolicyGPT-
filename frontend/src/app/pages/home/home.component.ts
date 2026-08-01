import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { SearchBarComponent } from '../../shared/components/search-bar/search-bar.component';

interface Highlight {
  icon: string;
  title: string;
  desc: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink, MatButtonModule, MatIconModule, SearchBarComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent {
  stats = [
    { label: 'Active Policies', value: '1,240+' },
    { label: 'Public Schemes', value: '860+' },
    { label: 'Citizens Served', value: '2.4M+' },
    { label: 'Departments Onboarded', value: '58' },
  ];

  highlights: Highlight[] = [
    { icon: 'travel_explore', title: 'Intelligent Search', desc: 'Find the right policy or scheme by keyword, department, sector, or state in seconds.' },
    { icon: 'fact_check', title: 'Eligibility Checker', desc: 'Answer a few questions and instantly see the schemes you qualify for.' },
    { icon: 'compare_arrows', title: 'Compare Schemes', desc: 'Place benefits, eligibility, and application steps side by side.' },
    { icon: 'notifications_active', title: 'Stay Updated', desc: 'Get alerts on new policies, scheme updates, and application deadlines.' },
    { icon: 'insights', title: 'Analytics Dashboards', desc: 'Track usage, engagement, and department performance at a glance.' },
    { icon: 'verified_user', title: 'Role-Based Access', desc: 'Tailored experiences for citizens, officials, researchers, and admins.' },
  ];

  onHomeSearch(term: string): void {
    // Placeholder wiring — navigate to /policies with query param once routed
    console.log('search:', term);
  }
}

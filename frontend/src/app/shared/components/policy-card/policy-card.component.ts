import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Policy } from '../../../core/models/policy.model';

@Component({
  selector: 'app-policy-card',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatChipsModule, MatButtonModule, MatIconModule],
  templateUrl: './policy-card.component.html',
  styleUrl: './policy-card.component.scss',
})
export class PolicyCardComponent {
  @Input({ required: true }) policy!: Policy;
}

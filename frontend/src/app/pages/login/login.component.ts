import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterLink,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatSnackBarModule,
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent {
  loading = signal(false);
  hidePassword = signal(true);
  errorMsg = signal<string | null>(null);

  form: FormGroup;

  demoAccounts = [
    { role: 'Citizen', email: 'citizen@example.com', password: 'Citizen@123' },
    { role: 'Administrator', email: 'admin@example.com', password: 'Admin@123' },
    { role: 'Government Official', email: 'official@example.com', password: 'Official@123' },
  ];

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  fillDemo(email: string, password: string): void {
    this.form.patchValue({ email, password });
  }

  togglePassword(): void {
    this.hidePassword.set(!this.hidePassword());
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    this.errorMsg.set(null);

    const { email, password } = this.form.getRawValue();

    this.auth.login({
      email: email!,
      password: password!,
    }).subscribe({
      next: (res) => {
        this.auth.persistSession(res);
        this.loading.set(false);
        this.snackBar.open(`Welcome back, ${res.user.fullName}!`, 'Close', {
          duration: 3000,
        });
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.loading.set(false);
        this.errorMsg.set(err.message || 'Login failed. Please try again.');
      },
    });
  }
}
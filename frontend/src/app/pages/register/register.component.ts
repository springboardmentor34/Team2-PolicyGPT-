import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  AbstractControl,
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { AuthService } from '../../core/services/auth.service';
import { UserRole } from '../../core/models/user.model';

function passwordsMatchValidator(): ValidatorFn {
  return (group: AbstractControl): ValidationErrors | null => {
    const pass = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return pass && confirm && pass !== confirm
      ? { passwordMismatch: true }
      : null;
  };
}

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterLink,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatSnackBarModule,
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
})
export class RegisterComponent {
  loading = signal(false);
  hidePassword = signal(true);
  hideConfirm = signal(true);
  errorMsg = signal<string | null>(null);

  roles: UserRole[] = [
    'Citizen',
    'Researcher',
    'Organization',
    'Government Official',
  ];

  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.form = this.fb.group(
      {
        fullName: ['', [Validators.required, Validators.minLength(3)]],
        email: ['', [Validators.required, Validators.email]],
        role: ['Citizen' as UserRole, [Validators.required]],
        password: [
          '',
          [
            Validators.required,
            Validators.minLength(8),
            Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/),
          ],
        ],
        confirmPassword: ['', [Validators.required]],
      },
      {
        validators: passwordsMatchValidator(),
      }
    );
  }

  togglePassword(): void {
    this.hidePassword.set(!this.hidePassword());
  }

  toggleConfirm(): void {
    this.hideConfirm.set(!this.hideConfirm());
  }

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    this.errorMsg.set(null);

    const raw = this.form.getRawValue();

    this.auth
      .register({
        fullName: raw.fullName!,
        email: raw.email!,
        password: raw.password!,
        confirmPassword: raw.confirmPassword!,
        role: raw.role as UserRole,
      })
      .subscribe({
        next: () => {
          this.loading.set(false);
          this.snackBar.open(
            'Account created! Please log in.',
            'Close',
            {
              duration: 3000,
            }
          );
          this.router.navigate(['/login']);
        },
        error: (err) => {
          this.loading.set(false);
          this.errorMsg.set(
            err.message || 'Registration failed. Please try again.'
          );
        },
      });
  }
}
import { Injectable, signal } from '@angular/core';
import { Observable, delay, of, throwError } from 'rxjs';
import {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  User,
} from '../models/user.model';

/**
 * AuthService
 * NOTE: This uses in-memory MOCK DATA only. No real HTTP calls are made yet.
 * Replace the internals of login()/register() with HttpClient calls to the
 * FastAPI backend (see architecture diagram: /api/auth/*) when the backend
 * is ready — the public method signatures are designed to stay the same.
 */
@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly STORAGE_KEY = 'policygpt_token';
  private readonly USER_KEY = 'policygpt_user';

  private mockUsers: (User & { password: string })[] = [
    {
      id: 1,
      fullName: 'Anita Sharma',
      email: 'citizen@example.com',
      password: 'Citizen@123',
      role: 'Citizen',
      state: 'Gujarat',
      phone: '9876543210',
      createdAt: '2024-01-12',
    },
    {
      id: 2,
      fullName: 'Rajeev Menon',
      email: 'admin@example.com',
      password: 'Admin@123',
      role: 'Administrator',
      state: 'Delhi',
      phone: '9812345678',
      createdAt: '2023-11-02',
    },
    {
      id: 3,
      fullName: 'Dr. Kavita Rao',
      email: 'official@example.com',
      password: 'Official@123',
      role: 'Government Official',
      state: 'Maharashtra',
      phone: '9900112233',
      createdAt: '2023-08-20',
    },
  ];

  currentUser = signal<User | null>(this.restoreUser());
  isAuthenticated = signal<boolean>(!!this.getToken());

  private restoreUser(): User | null {
    const raw = localStorage.getItem(this.USER_KEY);
    return raw ? (JSON.parse(raw) as User) : null;
  }

  login(payload: LoginRequest): Observable<LoginResponse> {
    const match = this.mockUsers.find(
      (u) => u.email.toLowerCase() === payload.email.toLowerCase() && u.password === payload.password
    );

    if (!match) {
      return throwError(() => new Error('Invalid email or password.')).pipe(delay(500));
    }

    const { password, ...user } = match;
    const response: LoginResponse = {
      token: 'mock-jwt-' + btoa(user.email + Date.now()),
      user,
      expiresIn: 3600,
    };

    return of(response).pipe(
      delay(600),
      // side effect: persist session
      // (kept inside pipe via tap-like pattern using of().subscribe would be cleaner,
      // but this keeps the service dependency-free for the mock stage)
    );
  }

  persistSession(response: LoginResponse): void {
    localStorage.setItem(this.STORAGE_KEY, response.token);
    localStorage.setItem(this.USER_KEY, JSON.stringify(response.user));
    this.currentUser.set(response.user);
    this.isAuthenticated.set(true);
  }

  register(payload: RegisterRequest): Observable<User> {
    if (payload.password !== payload.confirmPassword) {
      return throwError(() => new Error('Passwords do not match.')).pipe(delay(400));
    }
    if (this.mockUsers.some((u) => u.email.toLowerCase() === payload.email.toLowerCase())) {
      return throwError(() => new Error('An account with this email already exists.')).pipe(delay(400));
    }

    const newUser: User & { password: string } = {
      id: this.mockUsers.length + 1,
      fullName: payload.fullName,
      email: payload.email,
      password: payload.password,
      role: payload.role,
      createdAt: new Date().toISOString().slice(0, 10),
    };
    this.mockUsers.push(newUser);
    const { password, ...user } = newUser;
    return of(user).pipe(delay(600));
  }

  logout(): void {
    localStorage.removeItem(this.STORAGE_KEY);
    localStorage.removeItem(this.USER_KEY);
    this.currentUser.set(null);
    this.isAuthenticated.set(false);
  }

  getToken(): string | null {
    return localStorage.getItem(this.STORAGE_KEY);
  }
}

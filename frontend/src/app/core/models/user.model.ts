export type UserRole =
  | 'Administrator'
  | 'Government Official'
  | 'Citizen'
  | 'Researcher'
  | 'Organization'
  | 'Guest User';

export interface User {
  id: number;
  fullName: string;
  email: string;
  role: UserRole;
  state?: string;
  phone?: string;
  avatarUrl?: string;
  createdAt: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: User;
  expiresIn: number;
}

export interface RegisterRequest {
  fullName: string;
  email: string;
  password: string;
  confirmPassword: string;
  role: UserRole;
}

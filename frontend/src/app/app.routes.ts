import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  {
    path: 'home',
    loadComponent: () => import('./pages/home/home.component').then((m) => m.HomeComponent),
    title: 'PolicyGPT | Home',
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.component').then((m) => m.LoginComponent),
    title: 'PolicyGPT | Login',
  },
  {
    path: 'register',
    loadComponent: () => import('./pages/register/register.component').then((m) => m.RegisterComponent),
    title: 'PolicyGPT | Register',
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./pages/dashboard/dashboard.component').then((m) => m.DashboardComponent),
    canActivate: [authGuard],
    title: 'PolicyGPT | Dashboard',
  },
  {
    path: 'policies',
    loadComponent: () => import('./pages/policy-list/policy-list.component').then((m) => m.PolicyListComponent),
    title: 'PolicyGPT | Policies',
  },
  {
    path: 'schemes',
    loadComponent: () => import('./pages/scheme-list/scheme-list.component').then((m) => m.SchemeListComponent),
    title: 'PolicyGPT | Schemes',
  },
  {
    path: 'about',
    loadComponent: () => import('./pages/about/about.component').then((m) => m.AboutComponent),
    title: 'PolicyGPT | About',
  },
  {
    path: 'contact',
    loadComponent: () => import('./pages/contact/contact.component').then((m) => m.ContactComponent),
    title: 'PolicyGPT | Contact',
  },
  {
    path: 'profile',
    loadComponent: () => import('./pages/profile/profile.component').then((m) => m.ProfileComponent),
    canActivate: [authGuard],
    title: 'PolicyGPT | Profile',
  },
  {
    path: 'not-found',
    loadComponent: () =>
      import('./shared/components/not-found/not-found.component').then((m) => m.NotFoundComponent),
    title: 'PolicyGPT | Not Found',
  },
  { path: '**', redirectTo: 'not-found' },
];

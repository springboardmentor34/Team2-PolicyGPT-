import { Routes } from '@angular/router';
import { Login } from './auth/login/login';
import { Registration } from './auth/registration/registration';
import { CitizenDashboard } from './dashboard/citizen-dashboard/citizen-dashboard';
import { PolicyList } from './pages/policy-list/policy-list';
import { SchemeList } from './pages/scheme-list/scheme-list';
import { Notifications } from './pages/notifications/notifications';
import { Feedback } from './pages/feedback/feedback';
import { Reports } from './pages/reports/reports';
import { LandingPage } from './pages/landing-page/landing-page';
import { PolicyApproval } from './pages/policy-approval/policy-approval';
import { ComparePolicies } from './pages/compare-policies/compare-policies';
import { EligibilityChecker } from './pages/eligibility-checker/eligibility-checker';

export const routes: Routes = [
  { path: 'landing', component: LandingPage },
  { path: 'login', component: Login },
  { path: 'register', component: Registration },
  { path: 'dashboard', component: CitizenDashboard },
  { path: 'policies', component: PolicyList },
  { path: 'approval', component: PolicyApproval },
  { path: 'policy-approval', component: PolicyApproval },
  { path: 'schemes', component: SchemeList },
  { path: 'compare', component: ComparePolicies },
  { path: 'eligibility', component: EligibilityChecker },
  { path: 'notifications', component: Notifications },
  { path: 'feedback', component: Feedback },
  { path: 'reports', component: Reports },
  { path: '', redirectTo: '/landing', pathMatch: 'full' }
];

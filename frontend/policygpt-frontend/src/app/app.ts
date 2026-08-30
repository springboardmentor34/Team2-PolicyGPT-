import { Component, signal, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive, Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { CommonModule } from '@angular/common';
import { AuthService, AuthUser } from './services/auth.service';
import { NotificationService } from './services/notification.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  title = signal('PolicyGPT');
  isDarkMode = false;
  languages = [
    { code: 'en', name: '🇬🇧 English' },
    { code: 'ta', name: '🇮🇳 Tamil' },
    { code: 'hi', name: '🇮🇳 Hindi' },
    { code: 'ml', name: '🇮🇳 Malayalam' },
    { code: 'kn', name: '🇮🇳 Kannada' },
    { code: 'te', name: '🇮🇳 Telugu' },
    { code: 'mr', name: '🇮🇳 Marathi' },
    { code: 'bn', name: '🇮🇳 Bengali' }
  ];
  selectedLang = this.languages[0];
  isLandingPage = false;
  currentUser: AuthUser | null = null;
  unreadNotificationCount = 0;

  constructor(
    private router: Router,
    private authService: AuthService,
    private notificationService: NotificationService
  ) {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      const url = event.urlAfterRedirects || '';
      const path = url.split('?')[0];
      this.isLandingPage = path === '/landing' || path === '/login' || path === '/register';
      this.syncUser();

      // If user is already logged in and tries to access /login, redirect to /dashboard
      if (this.authService.isLoggedIn() && (path === '/login' || path === '/register')) {
        this.router.navigate(['/dashboard']);
      }
    });
  }

  ngOnInit() {
    this.syncUser();
    // Check system preference on load
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      this.isDarkMode = true;
      this.applyTheme();
    }
  }

  syncUser() {
    this.currentUser = this.authService.getUser();
    if (this.currentUser) {
      this.notificationService.getUnreadCount().subscribe({
        next: (res) => this.unreadNotificationCount = res.unread_count,
        error: (err) => console.error('Failed to load notifications unread count', err)
      });
    } else {
      this.unreadNotificationCount = 0;
    }
  }

  get isGovernmentOfficial(): boolean {
    return this.currentUser?.role === 'government_official';
  }

  get isAdministrator(): boolean {
    return this.currentUser?.role === 'administrator';
  }

  get canApprovePolicies(): boolean {
    return this.isGovernmentOfficial || this.isAdministrator;
  }

  get canViewAnalytics(): boolean {
    return this.isGovernmentOfficial || this.isAdministrator;
  }

  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    this.applyTheme();
  }

  applyTheme() {
    if (this.isDarkMode) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  }

  changeLanguage(event: Event) {
    const select = event.target as HTMLSelectElement;
    const lang = this.languages.find(l => l.code === select.value);
    if (lang) {
      this.selectedLang = lang;
    }
  }

  logout() {
    this.authService.logout();
    this.syncUser();
    this.router.navigate(['/login']);
  }
}

import { Component, signal, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive, Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { CommonModule } from '@angular/common';

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

  constructor(private router: Router) {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: any) => {
      this.isLandingPage = event.urlAfterRedirects === '/' || event.urlAfterRedirects === '/landing';
    });
  }

  ngOnInit() {
    // Check system preference on load
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      this.isDarkMode = true;
      this.applyTheme();
    }
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
}

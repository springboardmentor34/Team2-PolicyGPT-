# PolicyGPT — Frontend (Angular)

Government Policy & Public Scheme Intelligence Platform — Angular + Angular Material frontend, built with mock data so it runs standalone with **no backend required**.

## What's included

| # | Item | Status |
|---|------|--------|
| 1 | Project structure (core / shared / pages) | ✅ |
| 2 | Routing (`/login`, `/register`, `/dashboard`, `/policies`, `/schemes`, `/about`, `/contact`, `/profile`) | ✅ |
| 3 | Angular Material UI (toolbar, menu, cards, buttons, icons, tabs, dialogs-ready, snackbar, form fields) | ✅ |
| 4 | Pages (Login, Register, Dashboard, Policy List, Scheme List, About, Contact, Profile, Home, 404) | ✅ |
| 5 | Reusable components (Navbar, Sidebar, Footer, Header, Search Bar, Policy Card, Scheme Card, Loader, Not Found) | ✅ |
| 6 | Responsive design (CSS Grid + Flexbox, mobile nav) | ✅ |
| 7 | Models/interfaces (User, Policy, Scheme, LoginRequest, LoginResponse, Notification) | ✅ |
| 8 | Services with mock data (`auth.service.ts`, `policy.service.ts`, `scheme.service.ts`) | ✅ |
| 9 | Reactive form validation (login, register, contact, eligibility checker, profile) | ✅ |
| 10 | Dashboard design (stat cards, recent policies, latest schemes, search + filters) | ✅ |

No real API calls are made anywhere — everything runs off in-memory mock data in the three services under `src/app/core/services/`. When your FastAPI backend is ready, you only need to replace the internals of those three files with `HttpClient` calls; every component already consumes them through `Observable`s, so nothing else needs to change.

---

## 1. Prerequisites

Install these once on your machine:

1. **Node.js** (v18 or v20 LTS) — [https://nodejs.org](https://nodejs.org)
   Check with: `node -v`
2. **Angular CLI** (v17)
   ```bash
   npm install -g @angular/cli@17
   ```
   Check with: `ng version`
3. **VS Code** — [https://code.visualstudio.com](https://code.visualstudio.com)
   Recommended extension: **Angular Language Service** (search in Extensions tab).

---

## 2. Get the project into VS Code

1. Unzip the file you downloaded (`policygpt-frontend.zip`) anywhere on your computer.
2. Open VS Code → **File → Open Folder…** → select the unzipped `policygpt-frontend` folder.
3. Open a terminal inside VS Code: **Terminal → New Terminal**.

---

## 3. Install dependencies

In the VS Code terminal, run:

```bash
npm install
```

This reads `package.json` and downloads Angular, Angular Material, and all other required packages into `node_modules`. It can take 1–3 minutes the first time.

---

## 4. Run the app

```bash
npm start
```

(this runs `ng serve --open`, which compiles the app and opens it automatically at `http://localhost:4200`)

If it doesn't open automatically, go to **http://localhost:4200** in your browser.

The app will auto-reload every time you save a file.

---

## 5. Try it out — demo logins

Go to the **Login** page and either type these in, or click the demo-account chips to auto-fill them:

| Role | Email | Password |
|------|-------|----------|
| Citizen | `citizen@example.com` | `Citizen@123` |
| Administrator | `admin@example.com` | `Admin@123` |
| Government Official | `official@example.com` | `Official@123` |

You can also click **Register** to create a brand-new mock account (it's stored only in memory for the current browser session).

Things to try:
- **Home** → search bar, hero, stats
- **Policies** → keyword search + category/state/status filters
- **Schemes → Browse Schemes** tab → search + category filter
- **Schemes → Eligibility Checker** tab → fill the form and click "Check My Eligibility" to see matching schemes
- **Dashboard** (after logging in) → stat cards, recent policies, latest schemes
- **Profile** (after logging in) → click "Edit Profile" to update your name/phone/state
- Resize your browser window / open dev tools device toolbar to see the responsive mobile navbar

---

## 6. Project structure

```
src/app/
├── core/
│   ├── models/        # TypeScript interfaces: User, Policy, Scheme, Notification
│   ├── services/       # auth.service.ts, policy.service.ts, scheme.service.ts (mock data)
│   └── guards/         # auth.guard.ts — protects /dashboard and /profile
├── shared/
│   └── components/     # navbar, sidebar, footer, header, search-bar,
│                        # policy-card, scheme-card, loader, not-found
├── pages/
│   ├── home/  login/  register/  dashboard/
│   ├── policy-list/  scheme-list/
│   └── about/  contact/  profile/
├── app.routes.ts
├── app.config.ts
└── app.component.ts
```

Every component is **standalone** (Angular 17 style) — no `NgModule` files to manage.

---

## 7. Build for production

```bash
ng build
```

Output goes to `dist/policygpt-frontend/` — you can deploy that folder to any static host (Netlify, Vercel, Nginx, S3, etc.) once you're ready.

---

## 8. Connecting the real FastAPI backend later

Each service file has a comment marking exactly where to swap mock logic for real HTTP calls, e.g. in `policy.service.ts`:

```ts
// Replace this:
getAll(): Observable<Policy[]> {
  return of(this.mockPolicies).pipe(delay(300));
}

// With this (once FastAPI is running):
getAll(): Observable<Policy[]> {
  return this.http.get<Policy[]>(`${environment.apiUrl}/policies`);
}
```

You'll need to add `HttpClientModule`/`provideHttpClient()` to `app.config.ts` and create an `environment.ts` file for the API base URL when you get there — happy to help with that step when you're ready.

---

## Troubleshooting

- **`ng: command not found`** → the Angular CLI isn't installed globally; run `npm install -g @angular/cli@17` again, then close and reopen the terminal.
- **Port 4200 already in use** → run `ng serve --port 4300` instead.
- **Blank page after `npm start`** → check the terminal for red error text; most often it's a typo introduced while editing. Save the file again to trigger a rebuild.
- **`npm install` fails** → delete `node_modules` and `package-lock.json` if present, then run `npm install` again.

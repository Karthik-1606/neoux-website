# Neoux Industrial Solutions — Website

A single-page premium website (Home, About, Services, Core Competencies,
Projects, Industries, Why Neoux, Contact) built with plain HTML, CSS and JS.
No build tools, no npm install, no framework — open and run directly.

## Folder structure

```
neoux-website/
├── index.html          → all page markup (nav + 8 sections/pages)
├── css/
│   └── style.css        → all styling (colors, type, layout, animations)
├── js/
│   └── main.js           → page navigation, scroll reveal, filters, form demo
├── assets/
│   └── neoux-logo.png    → your logo, background removed & trimmed
└── README.md
```

## Run locally (VS Code)

1. Open this folder in VS Code (`File → Open Folder`).
2. Install the **Live Server** extension (Extensions panel → search "Live Server" by Ritwick Dey → Install).
3. Right-click `index.html` → **Open with Live Server**.
4. The site opens in your browser and auto-refreshes whenever you save a file.

## Deploy for free

**Option A — Netlify (easiest)**
1. Go to [app.netlify.com](https://app.netlify.com) → sign up free.
2. Drag and drop this whole `neoux-website` folder onto the "Deploy manually" area.
3. You get a live URL immediately (e.g. `neoux.netlify.app`).

**Option B — GitHub Pages**
1. Push this folder to a new GitHub repository.
2. Repo → Settings → Pages → Source: `main` branch, root folder.
3. Your site goes live at `yourusername.github.io/repo-name`.

**Custom domain:** once deployed, both Netlify and GitHub Pages let you attach
a custom domain (e.g. `neoux.in`) under their domain settings — just point
your domain's DNS as instructed there.

## Before going live, update these placeholders

- `index.html` → search for `neouxindustrial@gmail.com`, `+91 00000 00000`, and the
  `href="#"` LinkedIn/Instagram links in the footer and Contact page.
- Projects page → the 4 placeholder project cards (marked with a note on the
  page) — replace with real client work once completed.
- Contact form → currently shows a demo message on submit. Connect it to a
  service like [Formspree](https://formspree.io) or your own backend to
  actually receive enquiries.

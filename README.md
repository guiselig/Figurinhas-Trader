# 🏆 Figurinha Trader

A mobile app to organize, manage, and trade World Cup 2026 Panini stickers with collectors in your area.

**Status:** 🚀 In development
**Platforms:** iOS 14+ | Android 8+
**Stack:** React Native + Expo | Supabase | Google ML Kit

---

## ✨ Features

### Collection Management
- 📸 AI sticker scanning (Google ML Kit)
- 📊 Track owned/missing/duplicates with quantity
- 📈 Progress statistics (% completed)
- 🎯 Wishlist of desired stickers

### Trades & Chat
- 💬 Real-time chat with other collectors
- 🔔 Push notifications for messages
- 🌍 Listing feed with advanced search
- 📍 Search by sticker ("who has #347?")

### Meetup Points
- 🗺️ Interactive map (OpenFreeMap + MapLibre)
- 📌 Create/manage local meetups
- ✅ RSVP confirmation
- 👥 View confirmed attendees list (Premium)

### Social & Ranking
- 👤 Public profile with statistics
- 🏅 Collector ranking by city
- ⭐ Rating system (1-5 stars)
- 🤖 Automatic compatible trade suggestions

### Premium
- 🎯 Real-time automatic matching
- 💎 Listings with featured badge
- 🔍 Advanced proximity filter
- 📱 Unlimited AI scans

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         React Native + Expo             │
│    (iOS/Android • TypeScript)           │
├─────────────────────────────────────────┤
│          Supabase Backend               │
│  • Auth (Email + OAuth)                 │
│  • PostgreSQL (Profiles, Albums, etc)   │
│  • Realtime (Chat)                      │
├─────────────────────────────────────────┤
│       External Integrations             │
│  • Google ML Kit (AI Scan)              │
│  • OpenCage API (Geocoding)             │
│  • RevenueCat (In-app Purchases)        │
│  • Google AdMob (Ads)                   │
│  • FCM + APNs (Push Notifications)      │
├─────────────────────────────────────────┤
│    Home Server Docker (i5-4460)         │
│  • N8N Automation (workflows)           │
│  • PostHog (self-hosted analytics)      │
│  • Cloudflare Tunnel (public URLs)      │
└─────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Expo CLI: `npm install -g expo-cli`
- Supabase account (free)
- Google Cloud account (for OAuth and ML Kit)

### Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/guiselig/figurinha-trader.git
cd figurinha-trader
```

**2. Install dependencies**
```bash
npm install
```

**3. Configure environment variables**
```bash
cp .env.example .env.local
```

Fill in with your credentials:
```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# RevenueCat
REVENUECAT_API_KEY=your-api-key

# PostHog (self-hosted)
POSTHOG_HOST=https://posthog.yourdomain.com
POSTHOG_API_KEY=phc_your-posthog-api-key

# N8N (home server via Cloudflare Tunnel)
N8N_HOST=https://n8n.yourdomain.com
N8N_API_KEY=your-api-key
```

**4. Start the development server**
```bash
npm start
```

Press:
- `i` to open in iOS Simulator
- `a` to open in Android Emulator
- `w` to open in web (preview)

### Production Build

**iOS:**
```bash
eas build --platform ios
```

**Android:**
```bash
eas build --platform android
```

Submit builds:
```bash
eas submit --platform ios      # App Store
eas submit --platform android  # Google Play
```

---

## 📁 Project Structure

```
figurinha-trader/
├── app/                          # React Native code
│   ├── (tabs)/                   # Bottom Tabs navigation
│   │   ├── collection.tsx        # Collection screen
│   │   ├── trades.tsx            # Trades screen
│   │   ├── map.tsx               # Map screen
│   │   ├── social.tsx            # Social screen
│   │   └── profile.tsx           # Profile screen
│   ├── screens/                  # Additional stack screens
│   │   ├── chat.tsx              # Detailed chat
│   │   ├── scan.tsx              # AI scan
│   │   ├── ad-detail.tsx         # Listing detail
│   │   └── ...
│   ├── components/               # Reusable components
│   ├── hooks/                    # Custom hooks
│   ├── services/                 # Supabase, APIs
│   └── utils/                    # Helpers
│
├── db/                           # Migrations and seed
│   ├── migrations/
│   └── schema.sql
│
├── n8n/                          # N8N Workflows
│   ├── auto-match.json
│   ├── meetup-reminders.json
│   └── ...
│
├── .env.example                  # Variables template
├── PLANO_COMPLETO.md             # Full project plan
├── app.json                      # Expo config
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🗄️ Database (Supabase)

### Main Tables

**profiles**
- user_id, username, bio, avatar_url, city, premium_status, created_at

**stickers**
- id, number, name, team_id, image_url

**user_stickers**
- user_id, sticker_id, quantity_owned, quantity_needed

**trades**
- id, user_id, offering_sticker_id, wanted_sticker_id, status, location

**trade_messages**
- trade_id, sender_id, content, created_at

**meetups**
- id, user_id, name, location, date, time

**meetup_attendees**
- meetup_id, user_id, confirmed_at

**establishments**
- id, name, location, is_verified, pin_type (free/verified)

**ratings**
- reviewer_id, reviewed_id, stars, comment

**push_tokens**
- user_id, token, platform (ios/android)

**subscriptions**
- user_id, revenuecat_id, plan, expires_at

See [PLANO_COMPLETO.md](PLANO_COMPLETO.md) for the complete schema with all 13 tables.

---

## 📱 Features by Tier

| Feature | Free | Premium |
|---------|------|---------|
| AI Scan | 30/day | Unlimited |
| Listings | ✓ | ✓ + featured |
| Chat | ✓ | ✓ + notifications |
| Map | View | View + Create Meetups |
| Auto match | — | ✓ |
| Push Notifications | Basic | Realtime |
| Ad-free | — | ✓ |

**Premium Price:** R$ 9.90/month or R$ 79.90/year (RevenueCat)

---

## ⚙️ Infrastructure

### Supabase
- **Database:** PostgreSQL 500MB (free)
- **Auth:** Email + Google + Apple OAuth
- **Realtime:** WebSocket for chat
- **Storage:** 1GB for avatars/photos

### Home Server (i5-4460, Ubuntu + Docker)

All automation and analytics run on a home desktop server at zero cloud cost:

**N8N (workflow automation):**
- Trade automatic matching
- Meetup reminders (1h before)
- Subscription sync (RevenueCat webhook)
- Anti-fraud monitoring
- Weekly admin reports via Telegram

**PostHog (self-hosted analytics):**
- User events & conversion funnels
- Retention analysis
- Session recording
- Feature flags & A/B testing
- Error tracking

**Cloudflare Tunnel:** Free public HTTPS URLs for all home server services — no static IP required.

### Push Notifications
- **Firebase Cloud Messaging (FCM):** Android push delivery
- **Apple Push Notification Service (APNs):** iOS push delivery
- **Expo Push Service:** Unified API over FCM + APNs

### Other APIs
- **Google ML Kit:** On-device sticker scanning (no cost)
- **OpenCage:** Geocoding (2.5k reqs/day free)
- **RevenueCat:** In-app purchases (free up to 10k MAU)
- **Google AdMob:** Monetization (free)

**Total monthly cost:** ~R$100 (electricity + MEI DAS only)

---

## 🧪 Testing

```bash
# TypeScript validation
npx tsc --noEmit

# Build test (Android local)
eas build --platform android --local
```

---

## 📚 Documentation

- **[PLANO_COMPLETO.md](PLANO_COMPLETO.md)** — Full project plan, AI automation system, costs, architecture
- **[.env.example](.env.example)** — Environment variables reference

---

## 🔑 API Keys Setup

### Google Cloud (ML Kit + OAuth)
1. Create a project at [Google Cloud Console](https://console.cloud.google.com)
2. Enable **ML Kit** and **Cloud Vision API**
3. Create OAuth 2.0 credentials (type: iOS/Android application)
4. Add the keys to `.env.local`

### Supabase
1. Create an account at [supabase.com](https://supabase.com)
2. Create a new project (free tier)
3. Go to **Settings → API** to copy keys
4. Configure allowed domains in **Auth → Providers**

### Apple
1. Register your app at [Apple Developer](https://developer.apple.com)
2. Create an **Apple Team ID**
3. Generate distribution certificates

### RevenueCat
1. Create an account at [revenuecat.com](https://www.revenuecat.com)
2. Connect Apple App Store and Google Play
3. Copy the API key to `.env.local`

### PostHog (self-hosted)
1. Install via Docker Compose on your home server
2. Configure Cloudflare Tunnel for public HTTPS access
3. Create a project and copy the API key to `.env.local`

---

## 🚀 Deploy

### App Store (iOS)
```bash
eas submit --platform ios --latest
```

### Google Play (Android)
```bash
eas submit --platform android --latest
```

---

## 🤝 Contributing

1. Create a branch: `git checkout -b feature/your-feature`
2. Commit your changes: `git commit -m 'Add feature'`
3. Push: `git push origin feature/your-feature`
4. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Guilherme Selig**
📧 guiselig10@gmail.com

---

## 🙏 Acknowledgements

- [Expo](https://expo.dev) — React Native framework
- [Supabase](https://supabase.com) — Open-source backend
- [Google ML Kit](https://developers.google.com/ml-kit) — On-device AI
- [MapLibre](https://maplibre.org) — Open-source maps
- [N8N](https://n8n.io) — Workflow automation
- [PostHog](https://posthog.com) — Open-source analytics

---

**Last updated:** 04/18/2026

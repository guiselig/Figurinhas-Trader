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
│  • Expo Push Notifications              │
├─────────────────────────────────────────┤
│      N8N Automation (AWS EC2)           │
│  • Automatic matching                   │
│  • Scheduled notifications              │
│  • Data cleanup                         │
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
git clone https://github.com/your-user/figurinha-trader.git
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
SUPABASE_SERVICE_KEY=your-service-key

# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com

# Apple
APPLE_TEAM_ID=your-team-id

# APIs
OPENCAGE_API_KEY=your-api-key
REVENUECAT_API_KEY=your-api-key

# N8N (production)
N8N_HOST=your-aws-ec2-public-ip.ec2.amazonaws.com
N8N_PORT=5678
N8N_API_KEY=your-api-key
N8N_ENCRYPTION_KEY=your-random-secret-key
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
│   ├── utils/                    # Helpers
│   └── app.json                  # Expo configuration
│
├── db/                           # Migrations and seed
│   ├── migrations/
│   └── schema.sql
│
├── n8n/                          # N8N Workflows
│   ├── auto-match.json
│   ├── scheduled-notifications.json
│   └── ...
│
├── docs/                         # Documentation
│   ├── FEATURES.md
│   ├── API.md
│   └── DEVELOPMENT.md
│
├── .env.example                  # Variables template
├── app.json                      # Expo config
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🗄️ Database (Supabase)

### Main Tables

**profiles**
- user_id, username, bio, avatar_url, city, created_at

**albums**
- user_id, figurinha_number, status (have/missing/repeated), quantity

**collections** (custom collections)
- user_id, name, stickers_array

**listings** (trading posts)
- user_id, sticker_offering, sticker_wanted, location, is_premium

**conversations** (chats)
- user_id_1, user_id_2, listing_id, last_message_at

**messages**
- conversation_id, sender_id, content, created_at

**meetups**
- user_id, name, location, date, time, confirmed_count

**confirmations**
- meetup_id, user_id, confirmed_at

**ratings**
- reviewer_id, reviewed_id, stars, comment

See `Figurinha_Trader_Planejamento.docx` for the complete schema.

---

## 📱 Features by Tier

| Feature | Free | Premium |
|---------|------|---------|
| AI Scan | 30/day | Unlimited |
| Listings | ✓ | ✓ + featured |
| Chat | ✓ | ✓ + notifications |
| Map | View | View + Create |
| Auto match | — | ✓ |
| Push Notifications | Basic | Realtime |
| Ad-free | — | ✓ |

**Premium Price:** R$ 14.90/month (RevenueCat)

---

## ⚙️ Infrastructure

### Supabase
- **Database:** PostgreSQL 500MB (free)
- **Auth:** Email + Google + Apple OAuth
- **Realtime:** WebSocket for chat
- **Storage:** 1GB for avatars/photos

### N8N (AWS EC2 Free Tier)
- **Server:** t2.micro EC2 instance (1 vCPU, 1GB RAM) — free tier eligible
- **Cost:** $0 for 12 months (then ~$6-10/month)
- **Workflows:**
  - Daily automatic matching
  - Scheduled notifications
  - Old data cleanup
  - Reports

### Other APIs
- **Google ML Kit:** On-device (no cost)
- **OpenCage:** Geocoding (2.5k reqs/day free)
- **RevenueCat:** In-app purchases (free up to 10k MAU)
- **Google AdMob:** Monetization (free)

**Total cost:** $0-10/month (initial phase)

---

## 🧪 Testing

```bash
# Unit tests
npm run test

# Integration tests
npm run test:integration

# Build test
eas build --platform ios --local
```

---

## 📚 Documentation

- **[FEATURES.md](docs/FEATURES.md)** — Full feature list
- **[API.md](docs/API.md)** — Supabase endpoints and functions
- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)** — Contributor guide
- **[Figurinha_Trader_Planejamento.docx](Figurinha_Trader_Planejamento.docx)** — Full product spec
- **[Figurinha_Trader_Cronograma.xlsx](Figurinha_Trader_Cronograma.xlsx)** — 66 development tasks

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

## 📊 Timeline

**Start:** 04/04/2026
**Duration:** 17 days
**Deadline:** 04/20/2026 (store submission)

See [Figurinha_Trader_Cronograma.xlsx](Figurinha_Trader_Cronograma.xlsx) for the detailed timeline with 66 tasks.

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
🐙 [@your-github](https://github.com)

---

## 🙏 Acknowledgements

- [Expo](https://expo.dev) — React Native framework
- [Supabase](https://supabase.com) — Open-source backend
- [Google ML Kit](https://developers.google.com/ml-kit) — On-device AI
- [MapLibre](https://maplibre.org) — Open-source maps
- [N8N](https://n8n.io) — Workflow automation

---

## 📖 Full Setup

See **[AWS_SETUP.md](AWS_SETUP.md)** for the step-by-step guide on setting up the AWS infrastructure (EC2, Security Groups, N8N, Docker).

---

**Last updated:** 04/04/2026

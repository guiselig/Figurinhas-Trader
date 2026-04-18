# PLANO COMPLETO — FIGURINHA TRADER

Documentação definitiva de automação, infraestrutura, arquitetura e desenvolvimento.

**Versão:** 1.0 | **Status:** Pronto para Execução | **Data:** Abril 2026

---

## 📋 SUMÁRIO EXECUTIVO

- **Objetivo:** Construir e lançar app Figurinha Trader antes de 25 de abril
- **Métodologia:** Automação IA (Gemini 3.1 Pro + Claude Opus 4.7)
- **Prazo:** 10 dias (5 dias de build + 5 dias de testes e submissão)
- **Custo:** ~R$1.200 para lançar; ~R$100/mês para manter
- **Infraestrutura:** Servidor caseiro (i5-4460) + Google Cloud + MacBook Pro

---

## 🏗️ INFRAESTRUTURA COMPLETA

### Três Ambientes Integrados

```
SERVIDOR CASEIRO (i5-4460, Ubuntu)
├── Orchestrator Python (IA automation)
├── n8n (automações de produção)
└── Cloudflare Tunnel (acesso externo)
       ↕
GOOGLE CLOUD (Vertex AI)
├── Gemini 3.1 Pro (cérebro)
├── Claude Opus 4.7 (desenvolvedor)
└── Secret Manager (credenciais)
       ↕
GITHUB (repositório)
├── Código do app
├── tasks.json (tarefas)
└── state.json (progresso)
       ↕
MACBOOK PRO
└── Testes iOS + certificados (manual)
```

---

## 🤖 SISTEMA DE AUTOMAÇÃO IA

### Gemini 3.1 Pro — O Cérebro

**Não escreve código. Pensa e delega.**

Para cada uma das 106 tarefas:

1. **Analisa** — Entende o contexto do projeto e o que precisa ser feito
2. **Planeja** — Constrói um prompt detalhado extremamente específico para o Opus
3. **Avalia** — Analisa o resultado e decide se passou, se precisa retry ou intervenção manual

### Claude Opus 4.7 — O Desenvolvedor

**Nunca pensa. Recebe instruções e executa.**

Ferramentas disponíveis:
- `read_file()` — entender contexto
- `write_file()` — implementar código
- `bash_exec()` — validar TypeScript, rodar comandos
- `list_directory()` — explorar estrutura

**Fluxo típico:**
```
Ler tipos + cliente Supabase + padrões existentes
    ↓
Escrever novo componente/tela
    ↓
Rodar `tsc --noEmit` para validar TypeScript
    ↓
Corrigir erros se houver
    ↓
Validar novamente
```

### Paralelismo & Caching

- **3 workers** rodam simultaneamente → reduz 5 dias para 2–3 dias
- **Prompt caching** → 60% dos tokens custam 10x menos → economia de ~40% no budget

---

## 📱 O QUE ESTÁ SENDO CONSTRUÍDO

### App Mobile (React Native + Expo)

Uma base de código, duas plataformas:
- **Android:** Google Play (APK Builder)
- **iOS:** App Store (EAS Build na nuvem, sem precisar de Mac local para builds)

### Todas as Telas

**Auth:** Login, Cadastro, Recuperação de Senha, Onboarding  
**Abas:** Home (Feed), Mapa, Scan IA, Meu Álbum (980 figurinhas), Perfil  
**Trocas:** Criar, Detalhar, Chat, Minhas Ofertas  
**Meetups:** Criar (premium), Detalhar, Confirmar Presença  
**Premium:** Paywall, Confirmação  
**Settings:** Notificações, Privacidade, Termos, Deletar Conta (LGPD)  

### Backend Completo

**Supabase (PostgreSQL + Auth + Storage + Realtime)**
- 13 tabelas: profiles, stickers, trades, meetups, estabelecimentos, ratings, etc.
- Row Level Security: cada usuário vê apenas seus dados + dados públicos
- Edge Functions: matching de trocas, sync de assinaturas, anti-fraude
- Realtime: mudanças de status, novas mensagens chegam instantaneamente

### Monetização Tripla

1. **Premium (RevenueCat)** → R$9,90/mês ou R$79,90/ano
   - Scan ilimitado, criar meetups, sem anúncios
   
2. **Anúncios (AdMob)** → R$0,50–1,50 CPM
   - Banner sutil + 1 interstitial por sessão (free tier apenas)
   
3. **Verified Pins (B2B)** → R$29,90–49,90/mês
   - Papelarias/bancas pagam para aparecer no mapa com pino dourado

### Automações em Produção (n8n)

Rodando 24/7 no servidor caseiro via Docker:

1. **Matching de Trocas** → quando nova troca criada, encontra matches e envia notificação
2. **Lembretes de Meetup** → 1 hora antes do encontro, notifica todos confirmados
3. **Sincronização de Assinaturas** → RevenueCat webhook atualiza banco
4. **Anti-Fraude** → conta avaliações negativas, suspende contas fraudulentas
5. **Relatório Admin** → métricas semanais via Telegram

---

## 🔄 O FLUXO COMPLETO: DIA A DIA

### Dia 0 — Setup Manual (~4 horas)

Você faz uma única vez:

- Criar projeto GCP, ativar US$300 créditos
- Criar contas: Supabase, Expo, RevenueCat, AdMob, Firebase, OpenCage, Cloudflare
- Pagar: Google Play (US$25), Apple Developer (US$99)
- Instalar Ubuntu no desktop, Docker, Python, Node
- Instalar Cloudflare Tunnel
- Clonar repositório e autenticar
- Salvar TODAS credenciais no Secret Manager
- Gerar certificados iOS (MacBook)
- Abrir MEI em gov.br

**Resultado:** Tudo está conectado, seguro e pronto.

### Dias 1–3 — Automação Roda Sozinha

```bash
# Um único comando, e o sistema roda 24h/dia
sudo systemctl start figurinha-orchestrator

# Monitorar em tempo real
tail -f /home/ubuntu/logs/orchestrator.log
```

**O que está acontecendo:**
- Gemini lê tasks.json
- Gemini constrói prompts detalhados para Opus
- Opus implementa cada tarefa
- Código é validado com TypeScript
- Git commit automático
- Próxima tarefa começa

**Progresso visível:**
- Commits chegando no GitHub em tempo real
- `state.json` atualizando com progresso
- Logs mostrando quais tarefas completaram

**Blocos de tarefas (paralelo quando possível):**
- Setup Expo + Supabase schema + Design system
- Autenticação + hooks + services
- Telas principais + mapa + scan IA
- Premium + monetização + notificações
- Automações + anti-fraude + polish

### Dia 4 — Testes Manuais

Você entra e testa no app real:

**Android:** Dispositivo físico ou emulador
- Cadastro e login
- Scan de uma figurinha
- Criar oferta de troca
- Buscar trocas disponíveis
- Ver mapa
- Confirmar presença em meetup
- Assinar premium
- Receber notificação push

**iOS:** Simulador no MacBook
- Mesmos testes acima
- Em device físico se disponível

Bugs encontrados são documentados. Opus pode ser acionado manualmente para corrigir via servidor caseiro.

### Dia 5 — Build de Produção + Submissão

```bash
# Compila Android (.aab) + iOS (.ipa) nos servidores Expo
npx eas build --platform all --profile production

# Submete para as lojas (automático)
npx eas submit --platform android --latest
npx eas submit --platform ios --latest
```

Google Play: revisão 1–3 dias  
App Store: revisão 2–7 dias

### Dias 6–10 — Período de Revisão

Enquanto as lojas revisam:
- Preparar launch strategy nas redes sociais
- Abordar primeiros estabelecimentos (Verified Pins)
- Criar conteúdo
- Testar webhooks de n8n

### Dia 10+ — APP LIVE! 🎉

Disponível para download em todo o Brasil nas lojas oficiais.

---

## 💰 CUSTOS DEFINITIVOS

### Créditos GCP (US$300)

| Item | Valor |
|---|---|
| Claude Opus 4.7 (primeira passagem com caching) | ~US$130 |
| Claude Opus 4.7 (retentativas) | ~US$35 |
| Gemini 3.1 Pro (orquestração) | ~US$13 |
| **Total usado** | **~US$178** |
| **Buffer restante** | **~US$122** |

### Seu Dinheiro (Fora do GCP)

| Item | Custo | Frequência |
|---|---|---|
| Google Play Developer | US$25 | Único |
| Apple Developer Program | US$99 | Anual |
| iubenda (política de privacidade) | ~R$100 | Anual |
| Advogado (revisão jurídica) | ~R$400 | Único |
| MEI (abertura) | R$0 | Único |
| **Total para lançar** | **~R$1.200** | |

### Mensal (Pós-Lançamento)

| Item | Custo |
|---|---|
| MEI DAS | ~R$70 |
| Tudo o mais (Supabase free, n8n self-hosted, etc.) | R$0 |
| Eletricidade servidor | ~R$30 |
| **Total mensal** | **~R$100** |

---

## 📊 TECNOLOGIAS: 40+ Serviços Integrados

### IA & Cloud
- Gemini 3.1 Pro (Vertex)
- Claude Opus 4.7 (Vertex)
- Google Secret Manager

### Mobile
- React Native + Expo SDK 52
- Expo Router (navegação)
- Zustand (estado)
- React Query (dados)

### Backend
- Supabase (PostgreSQL + Auth + Storage + Realtime)
- Edge Functions (serverless)

### Mapas
- OpenFreeMap (tiles)
- MapLibre React Native
- OpenCage (geocoding)

### Notificações
- Expo Push Service
- Firebase Cloud Messaging (Android)
- Apple Push Notifications (iOS)

### Monetização
- RevenueCat (premium)
- Google Play Billing
- StoreKit (Apple)
- AdMob (anúncios)
- Stripe (B2B)

### Distribuição
- Google Play Console
- Apple Developer Program
- App Store Connect
- EAS Build & Submit

### Automação
- n8n (self-hosted)

### Analytics
- Firebase Analytics
- Firebase Crashlytics

### Legal
- iubenda (LGPD)
- MEI (CNPJ)

---

## 📋 SCHEMA DO BANCO DE DADOS

13 tabelas principais:

- `profiles` — usuários, premium status, ratings
- `stickers` — 980 figurinhas do álbum
- `teams` — países/times
- `user_stickers` — coleção pessoal (tenho/preciso)
- `trades` — ofertas de troca
- `trade_messages` — chat dentro de troca
- `meetups` — pontos de encontro
- `meetup_attendees` — confirmações
- `establishments` — lojas verificadas (Verified Pins)
- `ratings` — avaliações
- `push_tokens` — para notificações
- `fraud_reports` — denúncias
- `subscriptions` — assinaturas (sync RevenueCat)

---

## 🎯 COMPLIANCE & LEGAL

### MEI
- Abrir em gov.br antes do lançamento
- CNAE: 6201-5/00 + 6202-3/00
- DAS: ~R$70/mês

### LGPD (Lei de Proteção de Dados)
- Política de Privacidade (iubenda)
- Termos de Uso (custom)
- Botão "Excluir minha conta" funcional
- Consentimento explícito de GPS
- URL pública de política de privacidade

### Requisitos Apple
- Privacy Policy URL no App Store Connect
- Sign in with Apple obrigatório (se houver OAuth)
- Privacy Nutrition Labels preenchidas
- Screenshots em 6.7" (iPhone 15 Pro Max)

---

## ✅ CHECKLIST FINAL

- [ ] Dia 0: Setup manual 100% completo
- [ ] Dia 0: Todas as credenciais no Secret Manager
- [ ] Dia 0: Orquestrador testado localmente
- [ ] Dia 1: `sudo systemctl start figurinha-orchestrator`
- [ ] Dias 1–3: Monitorar logs, acompanhar commits
- [ ] Dia 4: Testes manuais completos
- [ ] Dia 5: Build + submissão às lojas
- [ ] Dias 6–9: Revisão nas lojas
- [ ] Dia 10+: APP LIVE NAS LOJAS 🚀

---

**Documentação completa e pronta para execução.**

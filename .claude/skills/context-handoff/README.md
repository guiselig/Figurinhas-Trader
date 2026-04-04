# Context Handoff

Skill para transferir contexto entre conversas em Claude Code, Claude.ai Chat e Cowork.

## Uso rápido

### Claude Code
```bash
/context-handoff
```

Copia o bloco markdown que aparece e cola em um novo chat.

### Claude.ai Chat
Diga: "me dê um resumo para colar em outro chat" ou "context handoff"

A skill gera um bloco markdown pronto para copiar.

### Cowork
```bash
/context-handoff
```

Mesmo que Claude Code.

---

## Exportar para JSON (automação)

Se precisar passar o contexto para um workflow ou MCP:

```bash
python scripts/export_context.py --format pretty > context.json
```

Ou direto do output do `/context-handoff`:

```bash
# Copie o markdown do /context-handoff em um arquivo chamado context.md
python scripts/export_context.py -i context.md -o context.json
```

O JSON gerado tem esta estrutura:

```json
{
  "user_profile": "...",
  "completed_actions": ["...", "..."],
  "decisions": ["...", "..."],
  "current_state": "...",
  "next_steps": ["...", "..."],
  "technical_context": "...",
  "metadata": {
    "generated_at": "auto",
    "format_version": "1.0",
    "environments": ["claude-code", "claude-ai-chat", "cowork"]
  }
}
```

---

## Integração com N8N

Para passar contexto para um workflow N8N:

1. Gere o JSON: `python scripts/export_context.py > context.json`
2. Use o webhook do N8N para enviar o JSON
3. Use os campos do JSON para construir novos prompts, criar tarefas, etc.

Exemplo com curl:

```bash
curl -X POST https://seu-n8n.com/webhook/contexto \
  -H "Content-Type: application/json" \
  -d @context.json
```

---

## Estrutura da pasta

```
context-handoff/
├── SKILL.md           # Instruções da skill
├── README.md          # Este arquivo
└── scripts/
    └── export_context.py  # Conversor markdown → JSON
```

---

## Tips

- **Markdown puro é melhor para humanos** — copie e cole entre chats
- **JSON é melhor para automação** — use para N8N, webhooks, workflows
- **A skill não precisa de subagents** — funciona em qualquer ambiente Claude
- **O script é stateless** — pode rodar offline, não precisa de API

---

Criado para Guilherme | claude-haiku-4-5

#!/usr/bin/env python3
"""
Convert context-handoff markdown output to JSON.
Usage: python export_context.py < context.md > context.json
Or: python export_context.py --input context.md --output context.json
"""

import json
import sys
import argparse
from pathlib import Path
import re


def parse_markdown_context(markdown_text):
    """Parse the markdown context block into structured JSON."""

    context = {
        "user_profile": "",
        "completed_actions": [],
        "decisions": [],
        "current_state": "",
        "next_steps": [],
        "technical_context": ""
    }

    lines = markdown_text.split('\n')
    current_section = None
    current_content = []

    for line in lines:
        # Skip the header line
        if line.startswith("> Contexto de sessão"):
            continue

        # Detect section headers
        if line.startswith("## Perfil do usuário"):
            if current_section and current_content:
                context[current_section] = '\n'.join(current_content).strip()
            current_section = "user_profile"
            current_content = []
        elif line.startswith("## O que foi feito"):
            if current_section and current_content:
                context[current_section] = parse_list('\n'.join(current_content))
            current_section = "completed_actions"
            current_content = []
        elif line.startswith("## Decisões"):
            if current_section and current_content:
                context[current_section] = parse_list('\n'.join(current_content))
            current_section = "decisions"
            current_content = []
        elif line.startswith("## Estado atual"):
            if current_section and current_content:
                context[current_section] = parse_list('\n'.join(current_content)) if isinstance(context[current_section], list) else '\n'.join(current_content).strip()
            current_section = "current_state"
            current_content = []
        elif line.startswith("## Próximos passos"):
            if current_section and current_content:
                context[current_section] = '\n'.join(current_content).strip()
            current_section = "next_steps"
            current_content = []
        elif line.startswith("## Contexto técnico"):
            if current_section and current_content:
                context[current_section] = parse_list('\n'.join(current_content)) if isinstance(context[current_section], list) else '\n'.join(current_content).strip()
            current_section = "technical_context"
            current_content = []
        elif line.strip() and not line.startswith("#"):
            if current_section:
                current_content.append(line)

    # Handle last section
    if current_section and current_content:
        if isinstance(context[current_section], list):
            context[current_section] = parse_list('\n'.join(current_content))
        else:
            context[current_section] = '\n'.join(current_content).strip()

    # Add metadata
    context["metadata"] = {
        "generated_at": "auto",
        "format_version": "1.0",
        "environments": ["claude-code", "claude-ai-chat", "cowork"]
    }

    return context


def parse_list(text):
    """Extract bullet points from text."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    items = [line.lstrip('- ').lstrip('* ') for line in lines if line.startswith('-') or line.startswith('*')]
    return items if items else text


def main():
    parser = argparse.ArgumentParser(description='Convert context-handoff markdown to JSON')
    parser.add_argument('--input', '-i', type=str, help='Input markdown file (default: stdin)')
    parser.add_argument('--output', '-o', type=str, help='Output JSON file (default: stdout)')
    parser.add_argument('--format', '-f', type=str, default='json', choices=['json', 'pretty'],
                       help='Output format')

    args = parser.parse_args()

    # Read input
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
    else:
        markdown_text = sys.stdin.read()

    # Parse and convert
    context_json = parse_markdown_context(markdown_text)

    # Format output
    if args.format == 'pretty':
        output = json.dumps(context_json, indent=2, ensure_ascii=False)
    else:
        output = json.dumps(context_json, ensure_ascii=False)

    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✓ Contexto exportado para: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()

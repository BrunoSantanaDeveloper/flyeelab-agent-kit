#!/usr/bin/env python3
"""flyee-bridge — Connects the .agent runtime to the Flyee Platform via structured events.

Usage:
    # Test connectivity
    python bridge.py --test

    # Emit an event
    python bridge.py emit "dev.task_completed" '{"task": "T1.1", "files": ["sdk.ts"]}'

    # Configure interactively
    python bridge.py --setup
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Resolve config path relative to this script
BRIDGE_DIR = Path(__file__).parent
CONFIG_PATH = BRIDGE_DIR / "config.json"
FALLBACK_PATH = BRIDGE_DIR / "events.jsonl"

DEFAULT_CONFIG = {
    "api_url": "http://localhost:8001",
    "project_id": "",
    "api_key": "",
    "enabled": False,
    "opted_out": False,
    "fallback_file": str(FALLBACK_PATH),
}


def load_config() -> dict:
    """Load bridge config, creating default if absent."""
    if not CONFIG_PATH.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_PATH) as f:
        return json.load(f)


def save_config(config: dict) -> None:
    """Persist config to disk."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def is_configured(config: dict) -> bool:
    """Check if bridge is properly configured for event emission."""
    if config.get("opted_out"):
        return False
    return bool(
        config.get("enabled")
        and config.get("api_key")
        and config.get("project_id")
    )


def setup_interactive() -> dict:
    """Interactive first-run setup. Returns updated config."""
    config = load_config()

    print("\n🔗 Flyee Bridge — Setup")
    print("=" * 40)
    print()
    print("The flyee-bridge sends development events")
    print("(task completions, test runs, deploys, etc.)")
    print("from your local .agent runtime to the Flyee Platform.")
    print()

    choice = input("Deseja integrar com a plataforma Flyee? (s/n): ").strip().lower()

    if choice in ("n", "nao", "não", "no"):
        config["opted_out"] = True
        config["enabled"] = False
        save_config(config)
        print("\n✅ Integração desabilitada. Eventos NÃO serão enviados.")
        print("   Para reconfigurar: python .agent/flyee-bridge/bridge.py --setup")
        return config

    # Get API URL
    default_url = config.get("api_url", "http://localhost:8001")
    url = input(f"API URL [{default_url}]: ").strip()
    config["api_url"] = url or default_url

    # Get Project ID
    project_id = input("Project ID (UUID do projeto no Flyee): ").strip()
    if not project_id:
        print("❌ Project ID é obrigatório.")
        return config

    config["project_id"] = project_id

    # Get API Key
    print()
    print("📋 Obtenha sua API Key na plataforma Flyee:")
    print("   Settings → API Keys → Generate Key")
    print()
    api_key = input("API Key: ").strip()
    if not api_key:
        print("❌ API Key é obrigatória.")
        return config

    config["api_key"] = api_key
    config["enabled"] = True
    config["opted_out"] = False

    save_config(config)
    print("\n✅ Flyee Bridge configurado com sucesso!")
    print(f"   API: {config['api_url']}")
    print(f"   Project: {config['project_id']}")
    print("   Eventos serão enviados automaticamente pelos workflows.")
    return config


def emit_event(
    event_type: str,
    payload: Optional[dict] = None,
    config: Optional[dict] = None,
) -> bool:
    """Emit a structured event to the Flyee Platform.

    Returns True if event was sent or queued, False if bridge is disabled.
    """
    if config is None:
        config = load_config()

    # Skip silently if opted out or not configured
    if config.get("opted_out") or not is_configured(config):
        return False

    event_data = {
        "project_id": config["project_id"],
        "entity_type": event_type.split(".")[0],
        "event_type": event_type,
        "payload": {
            **(payload or {}),
            "_timestamp": datetime.now(timezone.utc).isoformat(),
            "_agent_runtime": ".agent",
        },
        "source": "flyee-bridge",
    }

    # Try sending via HTTP
    url = f"{config['api_url'].rstrip('/')}/flyee/events/ingest"
    headers = {
        "Content-Type": "application/json",
        "X-Bridge-API-Key": config["api_key"],
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            import urllib.request

            req = urllib.request.Request(
                url,
                data=json.dumps(event_data).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status in (200, 201):
                    return True
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                time.sleep(wait)
            else:
                # Fallback: write to local file
                _fallback_write(event_data, config)
                return True

    return False


def _fallback_write(event_data: dict, config: dict) -> None:
    """Write event to local JSONL file as fallback."""
    fallback = config.get("fallback_file", str(FALLBACK_PATH))
    with open(fallback, "a") as f:
        f.write(json.dumps(event_data) + "\n")


def test_connection(config: dict) -> None:
    """Send a test event to verify connectivity."""
    print(f"\n🔗 Testing connection to {config['api_url']}...")

    if not is_configured(config):
        print("❌ Bridge not configured. Run: python bridge.py --setup")
        return

    success = emit_event(
        "dev.test_run",
        {"test": True, "message": "flyee-bridge connectivity test"},
        config,
    )

    if success:
        print("✅ Test event sent successfully!")
    else:
        print("❌ Failed to send test event. Check API URL and API key.")


def main():
    args = sys.argv[1:]

    if not args or "--help" in args:
        print(__doc__)
        return

    if "--setup" in args:
        setup_interactive()
        return

    config = load_config()

    # First-run detection: if not configured and not opted out, prompt
    if not config.get("opted_out") and not is_configured(config):
        if sys.stdin.isatty():
            print("\n⚠️  Flyee Bridge não está configurado.")
            config = setup_interactive()
            if not is_configured(config):
                return
        else:
            # Non-interactive: skip silently
            return

    if "--test" in args:
        test_connection(config)
        return

    if args[0] == "emit" and len(args) >= 2:
        event_type = args[1]
        payload = json.loads(args[2]) if len(args) > 2 else {}
        success = emit_event(event_type, payload, config)
        if success:
            print(f"✅ Event '{event_type}' emitted")
        else:
            print(f"⚠️  Event '{event_type}' skipped (bridge disabled)")
        return

    print(f"Unknown command: {args}")
    print("Use --help for usage info")


if __name__ == "__main__":
    main()

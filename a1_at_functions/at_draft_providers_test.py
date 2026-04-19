# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/commands/providers.py:175
# Component id: at.source.ass_ade.providers_test
__version__ = "0.1.0"

def providers_test(
    name: Annotated[str, typer.Argument(help="Provider to ping (e.g., groq). Use 'all' to test every available one.")] = "all",
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Send a minimal request to verify the provider responds."""
    _, settings = _resolve_config(config)
    config_providers = {
        n: override.model_dump() for n, override in settings.providers.items()
    }

    names = [name] if name != "all" else [p.name for p in detect_available_providers(config_providers)]
    if not names:
        console.print("[yellow]No providers available to test.[/yellow]")
        raise typer.Exit(code=0)

    results = []
    for pname in names:
        profile = get_provider(pname)
        if profile is None:
            console.print(f"[red]Unknown provider:[/red] {pname}")
            continue
        user_override = settings.providers.get(pname)
        user_key = user_override.api_key if user_override else None
        api_key = profile.resolve_api_key(user_key) or ""
        base_url = (user_override.base_url if user_override and user_override.base_url else profile.base_url)
        if not base_url:
            results.append((pname, "skipped (no base_url)"))
            continue
        model = profile.model_for_tier(
            "fast",
            override=user_override.models_by_tier if user_override else None,
        ) or "default"
        try:
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            with httpx.Client(base_url=base_url.rstrip("/"), headers=headers, timeout=15.0) as client:
                resp = client.post(
                    "/chat/completions",
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": "Say 'ok' in one word."}],
                        "max_tokens": 8,
                        "temperature": 0.0,
                    },
                )
            if resp.status_code == 200:
                text = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "") or ""
                results.append((pname, f"[green]✓ {resp.status_code}[/green] — {text.strip()[:32]}"))
            else:
                err = resp.text[:120].replace("\n", " ")
                results.append((pname, f"[yellow]{resp.status_code}[/yellow] {err}"))
        except httpx.HTTPError as exc:
            results.append((pname, f"[red]error[/red] — {type(exc).__name__}: {str(exc)[:80]}"))
        except Exception as exc:  # noqa: BLE001
            results.append((pname, f"[red]crash[/red] — {exc}"))

    table = Table(title="Provider connectivity test")
    table.add_column("Provider")
    table.add_column("Result")
    for pname, result in results:
        table.add_row(pname, result)
    console.print(table)

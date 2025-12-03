#!/usr/bin/env python3
"""Test script to verify all configurations."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.shared.config import settings


def test_configuration() -> None:
    """Test all configuration settings."""
    print("\n" + "=" * 80)
    print("CONFIGURATION TEST REPORT")
    print("=" * 80 + "\n")

    # Test 1: Environment
    print("1. Environment Configuration")
    print(f"   Environment: {settings.environment}")
    print(f"   Host: {settings.host}")
    print(f"   Port: {settings.port}")
    print("   ✅ Environment settings loaded\n")

    # Test 2: API Keys
    print("2. API Keys Configuration")
    openai_configured = bool(settings.openai_api_key)
    anthropic_configured = bool(settings.anthropic_api_key)
    brave_configured = bool(settings.brave_api_key_free)

    print(f"   OpenAI API Key: {'✅ Configured' if openai_configured else '❌ Missing'}")
    if openai_configured:
        print(f"      Key preview: {settings.openai_api_key[:20]}...")

    print(f"   Anthropic API Key: {'✅ Configured' if anthropic_configured else '❌ Missing'}")
    if anthropic_configured:
        print(f"      Key preview: {settings.anthropic_api_key[:20]}...")

    print(f"   Brave API Key: {'✅ Configured' if brave_configured else '❌ Missing'}")
    if brave_configured:
        print(f"      Key preview: {settings.brave_api_key_free[:20]}...")

    print(f"   Model Name: {settings.model_name}\n")

    # Test 3: Obsidian Vault
    print("3. Obsidian Vault Configuration")
    vault_path = Path(settings.obsidian_vault_path) if settings.obsidian_vault_path else None

    if vault_path:
        vault_exists = vault_path.exists()
        vault_is_dir = vault_path.is_dir() if vault_exists else False

        print(f"   Vault Path: {vault_path}")
        print(f"   Vault Exists: {'✅ Yes' if vault_exists else '❌ No'}")
        print(f"   Is Directory: {'✅ Yes' if vault_is_dir else '❌ No'}")

        if vault_exists and vault_is_dir:
            # Count files
            md_files = list(vault_path.rglob("*.md"))
            print(f"   Markdown Files: {len(md_files)} files found")
            print("   ✅ Vault is accessible\n")
        else:
            print("   ❌ Vault path not accessible\n")
    else:
        print("   ❌ Vault path not configured\n")

    # Test 4: Research Output Paths
    print("4. Research Output Paths")

    linkedin_path = Path(settings.linkedin_post_path) if settings.linkedin_post_path else None
    blog_path = Path(settings.blog_post_path) if settings.blog_post_path else None

    if linkedin_path:
        linkedin_exists = linkedin_path.exists()
        linkedin_is_dir = linkedin_path.is_dir() if linkedin_exists else False
        print(f"   LinkedIn Post Path: {linkedin_path}")
        print(f"   Directory Exists: {'✅ Yes' if linkedin_exists else '❌ No'}")
        print(f"   Is Directory: {'✅ Yes' if linkedin_is_dir else '❌ No'}")
        if linkedin_exists and linkedin_is_dir:
            files = list(linkedin_path.glob("*.md"))
            print(f"   Markdown Files: {len(files)} files")
            print("   ✅ LinkedIn path is accessible\n")
        else:
            print("   ❌ LinkedIn path not accessible\n")
    else:
        print("   ⚠️  LinkedIn path not configured\n")

    if blog_path:
        blog_exists = blog_path.exists()
        blog_is_dir = blog_path.is_dir() if blog_exists else False
        print(f"   Blog Post Path: {blog_path}")
        print(f"   Directory Exists: {'✅ Yes' if blog_exists else '❌ No'}")
        print(f"   Is Directory: {'✅ Yes' if blog_is_dir else '❌ No'}")
        if blog_exists and blog_is_dir:
            files = list(blog_path.glob("*.md"))
            print(f"   Markdown Files: {len(files)} files")
            print("   ✅ Blog path is accessible\n")
        else:
            print("   ❌ Blog path not accessible\n")
    else:
        print("   ⚠️  Blog path not configured\n")

    # Test 5: Tool Configuration
    print("5. Tool Configuration")
    print(f"   Obsidian Note Manager: {'✅ Enabled' if settings.enable_obsidian_note_manager else '❌ Disabled'}")
    print(f"   Obsidian Vault Query: {'✅ Enabled' if settings.enable_obsidian_vault_query else '❌ Disabled'}")
    print(f"   Obsidian Graph Analyzer: {'✅ Enabled' if settings.enable_obsidian_graph_analyzer else '❌ Disabled'}")
    print(f"   Obsidian Vault Organizer: {'✅ Enabled' if settings.enable_obsidian_vault_organizer else '❌ Disabled'}")
    print(f"   Obsidian Folder Manager: {'✅ Enabled' if settings.enable_obsidian_folder_manager else '❌ Disabled'}")
    print(f"   Web Search: {'✅ Enabled' if settings.enable_web_search else '❌ Disabled'}\n")

    # Test 6: Safety Limits
    print("6. Safety Limits")
    print(f"   Max File Size: {settings.max_file_size_mb} MB")
    print(f"   Max Search Results: {settings.max_search_results}")
    print(f"   Max Graph Depth: {settings.max_graph_depth}")
    print(f"   Max Batch Organize: {settings.max_batch_organize}")
    print(f"   Max Folder Depth: {settings.max_folder_depth}")
    print("   ✅ Safety limits configured\n")

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    all_checks = [
        ("Environment", True),
        ("OpenAI API", openai_configured),
        ("Anthropic API", anthropic_configured),
        ("Brave API", brave_configured),
        ("Obsidian Vault", vault_path and vault_path.exists() if vault_path else False),
        ("LinkedIn Path", linkedin_path and linkedin_path.exists() if linkedin_path else False),
        ("Blog Path", blog_path and blog_path.exists() if blog_path else False),
    ]

    passed = sum(1 for _, status in all_checks if status)
    total = len(all_checks)

    print(f"\nTests Passed: {passed}/{total}\n")

    for name, status in all_checks:
        print(f"   {name}: {'✅ PASS' if status else '❌ FAIL'}")

    print("\n" + "=" * 80 + "\n")

    if passed == total:
        print("🎉 All configuration tests passed! Your system is ready to use.\n")
        return

    print("⚠️  Some configuration items need attention. Review the failures above.\n")


if __name__ == "__main__":
    try:
        test_configuration()
    except Exception as e:
        print(f"\n❌ Configuration test failed with error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

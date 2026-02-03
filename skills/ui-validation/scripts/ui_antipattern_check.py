#!/usr/bin/env python3
"""
UI Anti-Pattern Validation Script
Detects common UI issues that make interfaces look unprofessional.

Usage:
    python ui_antipattern_check.py <project_path>
    python ui_antipattern_check.py .

Exit codes:
    0 - No violations found
    1 - Violations found (blocks completion)
"""

import os
import re
import sys
import io
from pathlib import Path
from typing import List, Tuple

# Fix encoding for Windows terminals
# encoding fix removed

# Common emojis used incorrectly as icons
EMOJI_PATTERN = r'[🔍⚡📊🎨🚀⚙️✨💡🔧📈📌🎯🏆💎🔥⭐🌟✅❌➡️⬅️🔴🟢🟡📁📂💻🖥️📱🎉💪🙌👋👍👎🤔💭📧📞🏠🔒🔓🛒💳📦🎁🔔🔕⚠️❗❓✏️🗑️📝📄🔗🌐🎵🎶📸🖼️🎬📹🎤🎧💾📀💿🖨️⌨️🖱️🔋🔌💰💵💸🏦📊📉📈🗓️📅⏰⏱️⌛⏳🔄🔃↩️↪️⬆️⬇️↔️↕️🔀🔁🔂▶️⏸️⏹️⏺️⏭️⏮️🔇🔈🔉🔊]'

# Hex color pattern (potential hardcoded colors)
HEX_COLOR_PATTERN = r'(?:bg-|text-|border-|fill-|stroke-)\[#[0-9A-Fa-f]{3,8}\]'

# File extensions to check
EXTENSIONS = ['.tsx', '.jsx', '.vue', '.svelte']


class Violation:
    def __init__(self, file: str, line: int, content: str, violation_type: str, severity: str):
        self.file = file
        self.line = line
        self.content = content.strip()[:100]  # Truncate for readability
        self.violation_type = violation_type
        self.severity = severity

    def __str__(self):
        clean_content = self.content.encode('ascii', 'ignore').decode('ascii')
        return f"VIOLATION|{self.file}|{self.line}|{self.violation_type}|{clean_content}"


def find_files(project_path: str) -> List[Path]:
    """Find all relevant UI files in the project."""
    files = []
    for ext in EXTENSIONS:
        files.extend(Path(project_path).rglob(f"*{ext}"))
    
    # Exclude common directories
    excluded = ['node_modules', '.next', 'dist', 'build', '.git', 'coverage']
    return [f for f in files if not any(ex in str(f) for ex in excluded)]


def check_emojis(file_path: Path) -> List[Violation]:
    """Check for emojis used as icons."""
    violations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Skip comments and strings that might be content (not icons)
                if '// ' in line and re.search(EMOJI_PATTERN, line.split('// ')[1] if len(line.split('// ')) > 1 else ''):
                    continue
                    
                # Check if emoji is used in JSX (likely as icon)
                matches = re.findall(EMOJI_PATTERN, line)
                if matches:
                    # Check if it's in a className or text content context
                    # Emojis in feature cards, icons, etc. are violations
                    if '<' in line or 'className' in line or 'Icon' not in line:
                        violations.append(Violation(
                            str(file_path),
                            line_num,
                            line,
                            "EMOJI_AS_ICON",
                            "ERROR"
                        ))
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    return violations


def check_cursor_pointer(file_path: Path) -> List[Violation]:
    """Check for missing cursor-pointer on interactive elements."""
    violations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # Check Link elements without cursor-pointer
                if '<Link' in line and 'className' in line:
                    if 'cursor-pointer' not in line and 'cursor:' not in line:
                        # Check if it's a simple navigation link (might be ok)
                        # but card-like Links should have cursor
                        if 'hover:' in line:  # Has hover but no cursor
                            violations.append(Violation(
                                str(file_path),
                                line_num,
                                line,
                                "LINK_NO_CURSOR",
                                "WARNING"
                            ))
                
                # Check button elements
                if '<button' in line.lower() and 'className' in line:
                    if 'cursor-pointer' not in line and 'cursor:' not in line:
                        # Buttons should always be obvious as clickable
                        violations.append(Violation(
                            str(file_path),
                            line_num,
                            line,
                            "BUTTON_NO_CURSOR",
                            "WARNING"
                        ))
                        
                # Check div/article with onClick
                if 'onClick=' in line and 'cursor-pointer' not in line:
                    violations.append(Violation(
                        str(file_path),
                        line_num,
                        line,
                        "CLICKABLE_NO_CURSOR",
                        "ERROR"
                    ))
                    
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    return violations


def check_hardcoded_colors(file_path: Path) -> List[Violation]:
    """Check for hardcoded hex colors instead of CSS variables."""
    violations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                matches = re.findall(HEX_COLOR_PATTERN, line)
                if matches:
                    # Allow certain exceptions (shadows, specific overrides)
                    if 'shadow' not in line.lower():
                        violations.append(Violation(
                            str(file_path),
                            line_num,
                            line,
                            "HARDCODED_COLOR",
                            "WARNING"
                        ))
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    return violations


def check_transitions(file_path: Path) -> List[Violation]:
    """Check for hover states without transitions."""
    violations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # If element has hover state but no transition
                if 'hover:' in line and 'className' in line:
                    if 'transition' not in line and 'duration-' not in line:
                        violations.append(Violation(
                            str(file_path),
                            line_num,
                            line,
                            "HOVER_NO_TRANSITION",
                            "INFO"
                        ))
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    return violations


def check_tailwind_theme(project_path: str) -> List[Violation]:
    """Check for incorrect Tailwind v4 @theme syntax in globals.css."""
    violations = []
    globals_paths = [
        Path(project_path) / "src" / "app" / "globals.css",
        Path(project_path) / "src" / "styles" / "globals.css",
        Path(project_path) / "app" / "globals.css",
    ]
    
    for globals_path in globals_paths:
        if globals_path.exists():
            try:
                with open(globals_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for line_num, line in enumerate(lines, 1):
                        # Check for problematic @theme inline pattern
                        if '@theme inline' in line:
                            violations.append(Violation(
                                str(globals_path),
                                line_num,
                                line,
                                "THEME_INLINE_WRONG",
                                "ERROR"
                            ))
                        
                        # Check for var() inside @theme block (doesn't work in v4)
                        if 'var(--' in line and '@theme' in content[:content.find(line)]:
                            # Check if we're inside @theme block
                            theme_start = content.rfind('@theme', 0, content.find(line))
                            if theme_start != -1:
                                between = content[theme_start:content.find(line)]
                                if '{' in between and '}' not in between:  # Inside @theme
                                    violations.append(Violation(
                                        str(globals_path),
                                        line_num,
                                        line,
                                        "VAR_INSIDE_THEME",
                                        "ERROR"
                                    ))
            except Exception as e:
                print(f"Warning: Could not read {globals_path}: {e}")
    
    return violations


def main():
    if len(sys.argv) < 2:
        print("Usage: python ui_antipattern_check.py <project_path>")
        print("Example: python ui_antipattern_check.py .")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    if not os.path.exists(project_path):
        print(f"Error: Path '{project_path}' does not exist")
        sys.exit(1)
    
    print("=" * 60)
    print("UI ANTI-PATTERN VALIDATION")
    print("=" * 60)
    print(f"Scanning: {os.path.abspath(project_path)}")
    print()
    
    files = find_files(project_path)
    print(f"Found {len(files)} UI files to check")
    print()
    
    all_violations: List[Violation] = []
    
    # Run all checks
    for file_path in files:
        print(f"DEBUG: Checking {file_path}")
        all_violations.extend(check_emojis(file_path))
        all_violations.extend(check_cursor_pointer(file_path))
        all_violations.extend(check_hardcoded_colors(file_path))
        all_violations.extend(check_transitions(file_path))
    
    # Check Tailwind theme config
    all_violations.extend(check_tailwind_theme(project_path))
    
    # Categorize violations
    errors = [v for v in all_violations if v.severity == "ERROR"]
    warnings = [v for v in all_violations if v.severity == "WARNING"]
    infos = [v for v in all_violations if v.severity == "INFO"]
    
    # Print results
    if errors:
        print("ERRORS (MUST FIX):")
        print("-" * 40)
        for v in errors:
            print(f"  {v}")
        print()
    
    if warnings:
        print("WARNINGS (SHOULD FIX):")
        print("-" * 40)
        for v in warnings:
            print(f"  {v}")
        print()
    
    if infos:
        print("INFO (CONSIDER):")
        print("-" * 40)
        for v in infos:
            print(f"  {v}")
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Errors:   {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    print(f"  Info:     {len(infos)}")
    print()
    
    if errors:
        print("VALIDATION FAILED - Fix errors before proceeding")
        print()
        print("Quick Fixes:")
        print("  - EMOJI_AS_ICON: Replace with Heroicons or Lucide icons")
        print("  - CLICKABLE_NO_CURSOR: Add cursor-pointer to className")
        print("  - THEME_INLINE_WRONG: Use @theme {} not @theme inline")
        print("  - VAR_INSIDE_THEME: Put values directly in @theme, not var()")
        sys.exit(1)
    elif warnings:
        print("VALIDATION PASSED WITH WARNINGS")
        print("  Consider fixing warnings for better UX")
        sys.exit(0)
    else:
        print("VALIDATION PASSED - No issues found!")
        sys.exit(0)


if __name__ == "__main__":
    main()

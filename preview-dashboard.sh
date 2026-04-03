#!/bin/bash
# Quick preview of all key documents

cd ~/github/Bot-MVP

echo "📊 BOT-MVP ENTERPRISE DASHBOARD"
echo "================================"
echo ""

echo "📁 Key Documents:"
echo "----------------"
echo "1. Chief of Staff Accountability: accountability/README.md"
echo "2. Performance Dashboard: performance-dashboard/README.md"
echo "3. Work Tracking: processes/work-submission/README.md"
echo "4. Catch-up Plan: docs/README.md"
echo "5. Audit Report: team-outputs/README.md"
echo ""

echo "🦞 Quick Preview Commands:"
echo "  glow accountability/README.md"
echo "  glow performance-dashboard/README.md"
echo "  glow processes/work-submission/README.md"
echo ""

# Check if glow is installed
if command -v glow &> /dev/null; then
    echo "📖 Previewing Accountability Framework:"
    echo "----------------------------------------"
    glow accountability/README.md 2>/dev/null || cat accountability/README.md
else
    echo "💡 Tip: Install 'glow' for beautiful markdown preview"
    echo "   curl -s https://api.github.com/repos/charmbracelet/glow/releases/latest | ..."
fi

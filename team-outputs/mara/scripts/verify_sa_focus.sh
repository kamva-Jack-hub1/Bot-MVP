#!/bin/bash

# ============================================
# VERIFY SOUTH AFRICA FOCUS SCRIPT
# Checks all data files for South Africa geographic focus
# Usage: ./verify_sa_focus.sh [directory]
# ============================================

set -e

# Default directory to current if not specified
DIR="${1:-.}"

echo "============================================"
echo "SOUTH AFRICA GEOGRAPHIC FOCUS VERIFICATION"
echo "Date: $(date)"
echo "Directory: $DIR"
echo "============================================"
echo ""

# Check for data files
echo "📁 Scanning for data files..."
DATA_FILES=$(find "$DIR" -name "*.csv" -o -name "*.json" -o -name "*.xlsx" -o -name "*.xls" 2>/dev/null | head -20)

if [ -z "$DATA_FILES" ]; then
    echo "❌ No data files found in $DIR"
    exit 1
fi

echo "Found $(echo "$DATA_FILES" | wc -l) data files"
echo ""

# Initialize counters
TOTAL_FILES=0
CLEAN_FILES=0
ISSUE_FILES=0

# Check each file
for FILE in $DATA_FILES; do
    echo "🔍 Checking: $(basename "$FILE")"
    TOTAL_FILES=$((TOTAL_FILES + 1))
    
    # Skip if file is empty
    if [ ! -s "$FILE" ]; then
        echo "   ⚠️  File is empty"
        ISSUE_FILES=$((ISSUE_FILES + 1))
        continue
    fi
    
    # Check for non-SA country codes in phone numbers
    NON_SA_PHONES=$(grep -c -E "\+234|\+254|\+20|\+233|\+971|\+212|\+34|\+81|\+44|\+1|\+33|\+49|\+86" "$FILE" 2>/dev/null || echo "0")
    
    # Check for non-SA email domains
    NON_SA_EMAILS=$(grep -c -E "\.ng$|\.ke$|\.eg$|\.gh$|\.ae$|\.ma$|\.co$|\.jp$|\.uk$|\.com$|\.org$|\.net$" "$FILE" 2>/dev/null || echo "0")
    
    # Check for non-SA locations
    NON_SA_LOCATIONS=$(grep -c -i "lagos\|nairobi\|cairo\|accra\|dubai\|casablanca\|madrid\|tokyo\|london\|new york\|paris\|berlin\|beijing" "$FILE" 2>/dev/null || echo "0")
    
    # Check for USD currency
    USD_CURRENCY=$(grep -c "\$" "$FILE" 2>/dev/null || echo "0")
    
    # Check for missing SA province
    MISSING_PROVINCE=$(grep -c -v -i "gauteng\|western cape\|kwa.*natal\|eastern cape\|limpopo\|mpumalanga\|north west\|free state\|northern cape" "$FILE" 2>/dev/null || echo "0")
    
    # Calculate issues
    TOTAL_ISSUES=$((NON_SA_PHONES + NON_SA_EMAILS + NON_SA_LOCATIONS + USD_CURRENCY + MISSING_PROVINCE))
    
    if [ "$TOTAL_ISSUES" -eq 0 ]; then
        echo "   ✅ Clean - South Africa focus maintained"
        CLEAN_FILES=$((CLEAN_FILES + 1))
    else
        echo "   ❌ Issues found:"
        [ "$NON_SA_PHONES" -gt 0 ] && echo "      - $NON_SA_PHONES non-SA phone numbers"
        [ "$NON_SA_EMAILS" -gt 0 ] && echo "      - $NON_SA_EMAILS non-SA email domains"
        [ "$NON_SA_LOCATIONS" -gt 0 ] && echo "      - $NON_SA_LOCATIONS non-SA locations"
        [ "$USD_CURRENCY" -gt 0 ] && echo "      - $USD_CURRENCY USD currency references"
        [ "$MISSING_PROVINCE" -gt 0 ] && echo "      - $MISSING_PROVINCE missing SA province"
        ISSUE_FILES=$((ISSUE_FILES + 1))
    fi
    
    echo ""
done

# Summary
echo "============================================"
echo "VERIFICATION SUMMARY"
echo "============================================"
echo "Total files checked: $TOTAL_FILES"
echo "Clean files: $CLEAN_FILES"
echo "Files with issues: $ISSUE_FILES"
echo ""

if [ "$ISSUE_FILES" -eq 0 ]; then
    echo "🎉 SUCCESS: All files maintain South Africa focus!"
    echo "✅ Geographic purity: 100%"
    exit 0
else
    echo "⚠️  WARNING: $ISSUE_FILES files need cleanup"
    echo "❌ Geographic purity: $((CLEAN_FILES * 100 / TOTAL_FILES))%"
    echo ""
    echo "RECOMMENDED ACTIONS:"
    echo "1. Run ./clean_sa_data.sh to automatically fix issues"
    echo "2. Review ./data_quality_report.md for detailed analysis"
    echo "3. Update data collection templates to prevent future issues"
    exit 1
fi
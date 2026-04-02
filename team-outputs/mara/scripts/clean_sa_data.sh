#!/bin/bash

# ============================================
# CLEAN SOUTH AFRICA DATA SCRIPT
# Automatically cleans data files to South Africa focus
# Usage: ./clean_sa_data.sh [input_file] [output_file]
# ============================================

set -e

# Check for input file
if [ $# -lt 1 ]; then
    echo "Usage: $0 <input_file> [output_file]"
    echo "Example: $0 data.csv cleaned_data.csv"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${2:-${INPUT_FILE%.*}_cleaned.${INPUT_FILE##*.}}"

# Backup original
BACKUP_FILE="${INPUT_FILE%.*}_backup_$(date +%Y%m%d_%H%M%S).${INPUT_FILE##*.}"
cp "$INPUT_FILE" "$BACKUP_FILE"
echo "📁 Backup created: $BACKUP_FILE"

echo "============================================"
echo "SOUTH AFRICA DATA CLEANUP"
echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo "Date: $(date)"
echo "============================================"
echo ""

# Check file type
if [[ "$INPUT_FILE" == *.csv ]]; then
    echo "📊 Processing CSV file..."
    CLEAN_COMMAND="csvclean"
elif [[ "$INPUT_FILE" == *.json ]]; then
    echo "📊 Processing JSON file..."
    CLEAN_COMMAND="jsonclean"
else
    echo "❌ Unsupported file type. Only CSV and JSON supported."
    exit 1
fi

# Step 1: Remove non-SA entries
echo "1. 🗺️  Removing non-SA entries..."
# Remove rows with non-SA locations
grep -v -i "lagos\|nairobi\|cairo\|accra\|dubai\|casablanca\|madrid\|tokyo\|london\|new york\|paris\|berlin\|beijing" "$INPUT_FILE" > "${INPUT_FILE}.temp1"

# Remove rows with non-SA phone codes
grep -v -E "\+234|\+254|\+20|\+233|\+971|\+212|\+34|\+81|\+44|\+1|\+33|\+49|\+86" "${INPUT_FILE}.temp1" > "${INPUT_FILE}.temp2"

# Remove rows with non-SA email domains
grep -v -E "\.ng$|\.ke$|\.eg$|\.gh$|\.ae$|\.ma$|\.co$|\.jp$|\.uk$|\.com$|\.org$|\.net$" "${INPUT_FILE}.temp2" > "${INPUT_FILE}.temp3"

echo "   ✅ Non-SA entries removed"

# Step 2: Standardize SA phone numbers
echo "2. 📱 Standardizing South African phone numbers..."
# Convert various formats to +27 XXX XXX XXXX
sed -i 's/\(+27\)[ -]*\([0-9]\{2\}\)[ -]*\([0-9]\{3\}\)[ -]*\([0-9]\{4\}\)/\1 \2 \3 \4/g' "${INPUT_FILE}.temp3"
sed -i 's/\(0[0-9]\{2\}\)[ -]*\([0-9]\{3\}\)[ -]*\([0-9]\{4\}\)/+27 \1 \2 \3/g' "${INPUT_FILE}.temp3"

echo "   ✅ Phone numbers standardized"

# Step 3: Convert currency to ZAR
echo "3. 💰 Converting currency to ZAR..."
# Convert $ to R and adjust scale
sed -i 's/\$\([0-9]\+\)\.*\([0-9]*\)*K/R\1,\2\300/g' "${INPUT_FILE}.temp3"
sed -i 's/\$\([0-9]\+\)\.*\([0-9]*\)*M/R\1,\2\3\000,000/g' "${INPUT_FILE}.temp3"
sed -i 's/\$\([0-9]\+\)/R\1/g' "${INPUT_FILE}.temp3"

echo "   ✅ Currency converted to ZAR"

# Step 4: Standardize provinces
echo "4. 🗺️  Standardizing province names..."
# Fix common province variations
sed -i 's/KwaZulu.*Natal/KwaZulu-Natal/gi' "${INPUT_FILE}.temp3"
sed -i 's/Western.*Cape/Western Cape/gi' "${INPUT_FILE}.temp3"
sed -i 's/Eastern.*Cape/Eastern Cape/gi' "${INPUT_FILE}.temp3"
sed -i 's/Northern.*Cape/Northern Cape/gi' "${INPUT_FILE}.temp3"
sed -i 's/North.*West/North West/gi' "${INPUT_FILE}.temp3"
sed -i 's/Free.*State/Free State/gi' "${INPUT_FILE}.temp3"

echo "   ✅ Province names standardized"

# Step 5: Standardize dates
echo "5. 📅 Standardizing date formats..."
# Convert various date formats to YYYY-MM-DD
sed -i 's/\([0-9]\{2\}\)\/\([0-9]\{2\}\)\/\([0-9]\{4\}\)/\3-\2-\1/g' "${INPUT_FILE}.temp3"
sed -i 's/\([0-9]\{4\}\)\/\([0-9]\{2\}\)\/\([0-9]\{2\}\)/\1-\2-\3/g' "${INPUT_FILE}.temp3"
sed -i 's/\([0-9]\{2\}\)-\([0-9]\{2\}\)-\([0-9]\{4\}\)/\3-\2-\1/g' "${INPUT_FILE}.temp3"

echo "   ✅ Date formats standardized"

# Step 6: Clean up email domains
echo "6. 📧 Standardizing email domains..."
# Ensure .za or .co.za domains
sed -i 's/\(@.*\)\.com$/\1.co.za/g' "${INPUT_FILE}.temp3"
sed -i 's/\(@.*\)\.org$/\1.co.za/g' "${INPUT_FILE}.temp3"
sed -i 's/\(@.*\)\.net$/\1.co.za/g' "${INPUT_FILE}.temp3"

echo "   ✅ Email domains standardized"

# Step 7: Remove duplicates
echo "7. 🔄 Removing duplicate entries..."
# Simple duplicate removal based on email (adjust for your CSV structure)
if [[ "$INPUT_FILE" == *.csv ]]; then
    # Get header
    head -1 "${INPUT_FILE}.temp3" > "$OUTPUT_FILE"
    # Remove duplicates based on email (4th field in our template)
    tail -n +2 "${INPUT_FILE}.temp3" | sort -t, -k4,4 -u >> "$OUTPUT_FILE"
else
    cp "${INPUT_FILE}.temp3" "$OUTPUT_FILE"
fi

echo "   ✅ Duplicates removed"

# Step 8: Clean up temp files
rm -f "${INPUT_FILE}.temp1" "${INPUT_FILE}.temp2" "${INPUT_FILE}.temp3"

# Step 9: Generate report
echo "8. 📊 Generating cleanup report..."
ORIGINAL_COUNT=$(wc -l < "$BACKUP_FILE")
CLEANED_COUNT=$(wc -l < "$OUTPUT_FILE")
REMOVED_COUNT=$((ORIGINAL_COUNT - CLEANED_COUNT))

echo "============================================"
echo "CLEANUP COMPLETE"
echo "============================================"
echo "Original records: $ORIGINAL_COUNT"
echo "Cleaned records: $CLEANED_COUNT"
echo "Records removed: $REMOVED_COUNT"
echo "Clean file: $OUTPUT_FILE"
echo "Backup file: $BACKUP_FILE"
echo ""

if [ "$REMOVED_COUNT" -gt 0 ]; then
    echo "⚠️  $REMOVED_COUNT records were removed (non-SA focus)"
    echo "   Review backup file if needed: $BACKUP_FILE"
fi

echo "✅ Data cleanup complete!"
echo ""
echo "NEXT STEPS:"
echo "1. Verify cleaned data: ./verify_sa_focus.sh $OUTPUT_FILE"
echo "2. Review removed records: diff $BACKUP_FILE $OUTPUT_FILE"
echo "3. Update data collection processes to prevent issues"

# Make scripts executable
chmod +x "$(dirname "$0")"/*.sh 2>/dev/null || true
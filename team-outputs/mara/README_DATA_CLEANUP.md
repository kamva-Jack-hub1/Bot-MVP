# 📊 MARA'S DATA WORKSPACE
## **South Africa Focus - Quality First**

### **Sponsor Directive (April 2, 2026):**
> "Can you help Mara focus and clean up the data - Focus on SA for now"

### **Chief of Staff Response:**
Complete data cleanup toolkit and guidance provided for immediate use.

---

## 🎯 **IMMEDIATE PRIORITY: SOUTH AFRICA FOCUS**

### **Current Status:**
- ✅ **South Africa-only database created**: `SME_CONTACTS_DATABASE_TEMPLATE_SOUTH_AFRICA_ONLY.csv`
- ✅ **Research scope guidance**: `MARA_RESEARCH_SCOPE_GUIDANCE.md`
- ✅ **Data cleanup plan**: `MARA_DATA_CLEANUP_PLAN.md`
- ✅ **Cleanup tools**: Scripts in `scripts/` directory
- ✅ **Collection template**: `templates/SME_DATA_COLLECTION_TEMPLATE_SOUTH_AFRICA.csv`

### **Non-Negotiable Rule:**
> **ONLY South Africa data. No exceptions.**

---

## 🛠️ **DATA CLEANUP TOOLS**

### **1. Verification Script:**
```bash
# Check data for South Africa focus
./scripts/verify_sa_focus.sh [directory_or_file]

# Example:
./scripts/verify_sa_focus.sh .          # Check current directory
./scripts/verify_sa_focus.sh data.csv   # Check specific file
```

### **2. Cleanup Script:**
```bash
# Automatically clean data to South Africa standards
./scripts/clean_sa_data.sh input.csv [output.csv]

# Example:
./scripts/clean_sa_data.sh old_data.csv cleaned_data.csv
```

### **3. Python Quality Tool:**
```bash
# Advanced data quality checking and cleaning
python3 scripts/sa_data_quality.py data.csv [cleaned_data.csv]

# Example:
python3 scripts/sa_data_quality.py messy_data.csv clean_data.csv
```

### **4. Quick Check:**
```bash
# One-liner to check current data
find . -name "*.csv" -exec ./scripts/verify_sa_focus.sh {} \;
```

---

## 📋 **DATA COLLECTION PROCESS**

### **Step 1: Use Correct Template**
Always start with: `templates/SME_DATA_COLLECTION_TEMPLATE_SOUTH_AFRICA.csv`

### **Step 2: Follow Data Rules:**
1. **Location**: South Africa cities only
2. **Phone**: +27 format only
3. **Email**: .za or .co.za domains
4. **Currency**: ZAR only (R)
5. **Province**: Valid SA province
6. **BEE**: Level 1-8 or N/A
7. **Registration**: Valid SA company number

### **Step 3: Verify Before Submission**
```bash
# Always run verification before submitting
./scripts/verify_sa_focus.sh your_data.csv
```

### **Step 4: Submit for Review**
1. Commit to GitHub with clear description
2. Tag Chief of Staff for review
3. Wait for verification approval
4. Fix any issues identified

---

## 🚨 **COMMON ISSUES & SOLUTIONS**

### **Issue: Non-SA entries found**
**Solution:**
```bash
# Remove non-SA entries
./scripts/clean_sa_data.sh problematic_data.csv cleaned_data.csv
```

### **Issue: Mixed currency formats**
**Solution:**
```bash
# Convert all to ZAR
sed -i 's/\$/R/g' your_data.csv
```

### **Issue: Invalid phone formats**
**Solution:**
```bash
# Standardize phone numbers
sed -i 's/\(0[0-9]\{2\}\)[ -]*\([0-9]\{3\}\)[ -]*\([0-9]\{4\}\)/+27 \1 \2 \3/g' your_data.csv
```

### **Issue: Missing required fields**
**Solution:**
1. Check template for required fields
2. Fill missing data before submission
3. Use "N/A" if genuinely not applicable

---

## 📊 **QUALITY METRICS**

### **Target Standards:**
- **Geographic purity**: 100% South Africa
- **Data completeness**: 95%+ for critical fields
- **Format consistency**: 100% standardized
- **Accuracy rate**: 90%+ verified

### **Monitoring:**
- **Daily**: Self-check with verification script
- **Weekly**: Chief of Staff quality audit
- **Monthly**: Comprehensive data review
- **Continuous**: Automated quality checks

---

## 👥 **SUPPORT CHANNELS**

### **Immediate Help:**
- **Chief of Staff**: Direct assistance available
- **Cleanup Scripts**: Automated tools provided
- **Templates**: Pre-configured for success
- **Documentation**: Comprehensive guidance

### **Escalation Path:**
1. **Self-fix**: Use provided tools
2. **Peer help**: Check with other agents
3. **Chief of Staff**: Direct intervention
4. **Sponsor**: Final validation

### **Training Resources:**
1. `MARA_RESEARCH_SCOPE_GUIDANCE.md` - Geographic focus
2. `MARA_DATA_CLEANUP_PLAN.md` - Cleanup procedures
3. Script documentation - Tool usage
4. Template examples - Data standards

---

## 🎯 **SUCCESS CRITERIA**

### **Clean Data Definition:**
- ✅ **100% South Africa entries**
- ✅ **Complete required fields**
- ✅ **Consistent formats**
- ✅ **Accurate information**
- ✅ **Ready for Campaign 1**

### **Sponsor Validation:**
- Can open any file and see pure South Africa data
- Can trust all contact information is accurate
- Can use data immediately for business decisions
- Can see quality improvement over time

### **Quality Certification:**
> **"South Africa Focus Certified - Data Quality Assured"**
> This data meets all South Africa focus and quality standards.

---

## 🔄 **CONTINUOUS IMPROVEMENT**

### **Feedback Loop:**
1. **Collect data** using templates
2. **Verify quality** with scripts
3. **Submit for review** to Chief of Staff
4. **Receive feedback** and improve
5. **Update processes** based on learnings

### **Quality Culture:**
- **Proactive**: Check quality before issues arise
- **Transparent**: All data visible on GitHub
- **Collaborative**: Share best practices
- **Accountable**: Own data quality completely

### **Progress Tracking:**
- **Git commits**: Show quality improvements
- **Quality reports**: Document verification results
- **Sponsor feedback**: Direct input on data quality
- **Team metrics**: Compare and improve together

---

## 📞 **QUICK REFERENCE**

### **Essential Commands:**
```bash
# Check data quality
./scripts/verify_sa_focus.sh .

# Clean problematic data
./scripts/clean_sa_data.sh input.csv output.csv

# Advanced quality analysis
python3 scripts/sa_data_quality.py data.csv
```

### **Key Files:**
- `SME_CONTACTS_DATABASE_TEMPLATE_SOUTH_AFRICA_ONLY.csv` - Clean database
- `MARA_RESEARCH_SCOPE_GUIDANCE.md` - Geographic rules
- `MARA_DATA_CLEANUP_PLAN.md` - Cleanup procedures
- `scripts/` - Quality tools
- `templates/` - Collection templates

### **Quality Mantra:**
> "South Africa only. Quality first. Verify always."

---

**Status**: **Data cleanup toolkit deployed - Ready for immediate use**  
**Support**: **Chief of Staff available for direct assistance**  
**Goal**: **Clean, focused, actionable South Africa data**  
**Success**: **Sponsor can trust all data is South Africa focused and high quality**

**No more data quality issues. No more geographic drift. Just clean South Africa data ready for action.** 🦞

---
*Workspace setup: April 2, 2026, 09:25 SAST*  
*Authority: Chief of Staff (Single Point Accountability)*  
*Support: Immediate and ongoing*  

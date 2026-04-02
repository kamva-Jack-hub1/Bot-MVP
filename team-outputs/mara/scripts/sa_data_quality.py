#!/usr/bin/env python3
"""
South Africa Data Quality Tool
Advanced data cleaning and validation for South Africa focus
"""

import pandas as pd
import re
from datetime import datetime
import sys
import os

class SADataQuality:
    """South Africa Data Quality Management"""
    
    # South Africa standards
    SA_PROVINCES = [
        'Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape',
        'Limpopo', 'Mpumalanga', 'North West', 'Free State', 'Northern Cape'
    ]
    
    BEE_LEVELS = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 
                  'Level 5', 'Level 6', 'Level 7', 'Level 8', 'N/A']
    
    # Regex patterns
    SA_PHONE_PATTERN = r'^\+27\s?\d{2}\s?\d{3}\s?\d{4}$'
    SA_EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(za|co\.za)$'
    SA_REGISTRATION_PATTERN = r'^\d{4}/\d{6}/07$'
    ZAR_CURRENCY_PATTERN = r'^R\d+([,.]\d+)*[MK]?$'
    
    def __init__(self, file_path):
        """Initialize with data file"""
        self.file_path = file_path
        self.df = None
        self.quality_report = {}
        
    def load_data(self):
        """Load data from file"""
        try:
            if self.file_path.endswith('.csv'):
                self.df = pd.read_csv(self.file_path)
            elif self.file_path.endswith('.xlsx') or self.file_path.endswith('.xls'):
                self.df = pd.read_excel(self.file_path)
            elif self.file_path.endswith('.json'):
                self.df = pd.read_json(self.file_path)
            else:
                raise ValueError("Unsupported file format")
            
            print(f"✅ Loaded {len(self.df)} records from {self.file_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def check_geographic_focus(self):
        """Check for South Africa geographic focus"""
        issues = []
        
        # Check for non-SA locations
        non_sa_keywords = ['Lagos', 'Nairobi', 'Cairo', 'Accra', 'Dubai', 
                          'Casablanca', 'Madrid', 'Tokyo', 'London', 'New York']
        
        for column in ['location', 'city', 'address']:
            if column in self.df.columns:
                non_sa_mask = self.df[column].astype(str).str.contains(
                    '|'.join(non_sa_keywords), case=False, na=False)
                if non_sa_mask.any():
                    issues.append(f"Non-SA locations in {column}: {non_sa_mask.sum()} records")
        
        # Check for non-SA phone codes
        if 'phone' in self.df.columns:
            non_sa_phones = self.df['phone'].astype(str).str.contains(
                r'\+234|\+254|\+20|\+233|\+971|\+212|\+34|\+81|\+44|\+1')
            if non_sa_phones.any():
                issues.append(f"Non-SA phone codes: {non_sa_phones.sum()} records")
        
        # Check for non-SA email domains
        if 'email' in self.df.columns:
            non_sa_emails = self.df['email'].astype(str).str.contains(
                r'\.ng$|\.ke$|\.eg$|\.gh$|\.ae$|\.ma$|\.co$|\.jp$|\.uk$')
            if non_sa_emails.any():
                issues.append(f"Non-SA email domains: {non_sa_emails.sum()} records")
        
        self.quality_report['geographic_issues'] = issues
        return len(issues) == 0
    
    def check_data_completeness(self):
        """Check for missing required fields"""
        required_fields = ['company_name', 'contact_name', 'email', 'phone', 
                          'location', 'industry', 'revenue_range_zar']
        
        completeness = {}
        for field in required_fields:
            if field in self.df.columns:
                missing = self.df[field].isna().sum()
                completeness[field] = {
                    'total': len(self.df),
                    'missing': missing,
                    'completeness': 100 * (len(self.df) - missing) / len(self.df)
                }
        
        self.quality_report['completeness'] = completeness
        return all(comp['missing'] == 0 for comp in completeness.values())
    
    def check_data_consistency(self):
        """Check for consistent formats"""
        consistency_issues = []
        
        # Check phone format
        if 'phone' in self.df.columns:
            valid_phones = self.df['phone'].astype(str).str.match(self.SA_PHONE_PATTERN, na=False)
            if not valid_phones.all():
                consistency_issues.append(f"Invalid phone format: {(~valid_phones).sum()} records")
        
        # Check email format
        if 'email' in self.df.columns:
            valid_emails = self.df['email'].astype(str).str.match(self.SA_EMAIL_PATTERN, na=False)
            if not valid_emails.all():
                consistency_issues.append(f"Invalid email format: {(~valid_emails).sum()} records")
        
        # Check province names
        if 'province' in self.df.columns:
            valid_provinces = self.df['province'].isin(self.SA_PROVINCES)
            if not valid_provinces.all():
                consistency_issues.append(f"Invalid province: {(~valid_provinces).sum()} records")
        
        # Check BEE levels
        if 'bee_level' in self.df.columns:
            valid_bee = self.df['bee_level'].isin(self.BEE_LEVELS)
            if not valid_bee.all():
                consistency_issues.append(f"Invalid BEE level: {(~valid_bee).sum()} records")
        
        self.quality_report['consistency_issues'] = consistency_issues
        return len(consistency_issues) == 0
    
    def check_currency(self):
        """Check for ZAR currency"""
        currency_issues = []
        
        # Check for USD
        if 'revenue_range' in self.df.columns:
            usd_found = self.df['revenue_range'].astype(str).str.contains(r'\$', na=False)
            if usd_found.any():
                currency_issues.append(f"USD currency found: {usd_found.sum()} records")
        
        # Check for ZAR format
        if 'revenue_range_zar' in self.df.columns:
            valid_zar = self.df['revenue_range_zar'].astype(str).str.match(self.ZAR_CURRENCY_PATTERN, na=False)
            if not valid_zar.all():
                currency_issues.append(f"Invalid ZAR format: {(~valid_zar).sum()} records")
        
        self.quality_report['currency_issues'] = currency_issues
        return len(currency_issues) == 0
    
    def clean_data(self):
        """Clean the data according to South Africa standards"""
        cleaned_df = self.df.copy()
        
        # 1. Remove non-SA entries
        print("1. Removing non-SA entries...")
        non_sa_mask = pd.Series([False] * len(cleaned_df))
        
        for column in ['location', 'city', 'address']:
            if column in cleaned_df.columns:
                non_sa_keywords = ['Lagos', 'Nairobi', 'Cairo', 'Accra', 'Dubai']
                column_mask = cleaned_df[column].astype(str).str.contains(
                    '|'.join(non_sa_keywords), case=False, na=False)
                non_sa_mask = non_sa_mask | column_mask
        
        if 'phone' in cleaned_df.columns:
            phone_mask = cleaned_df['phone'].astype(str).str.contains(
                r'\+234|\+254|\+20|\+233|\+971|\+212')
            non_sa_mask = non_sa_mask | phone_mask
        
        cleaned_df = cleaned_df[~non_sa_mask]
        print(f"   Removed {non_sa_mask.sum()} non-SA records")
        
        # 2. Standardize phone numbers
        print("2. Standardizing phone numbers...")
        if 'phone' in cleaned_df.columns:
            cleaned_df['phone'] = cleaned_df['phone'].astype(str).apply(self.standardize_phone)
        
        # 3. Convert currency to ZAR
        print("3. Converting currency to ZAR...")
        if 'revenue_range' in cleaned_df.columns:
            cleaned_df['revenue_range_zar'] = cleaned_df['revenue_range'].apply(self.convert_to_zar)
        
        # 4. Standardize provinces
        print("4. Standardizing provinces...")
        if 'province' in cleaned_df.columns:
            cleaned_df['province'] = cleaned_df['province'].apply(self.standardize_province)
        
        # 5. Fill missing BEE levels
        print("5. Handling BEE levels...")
        if 'bee_level' in cleaned_df.columns:
            cleaned_df['bee_level'] = cleaned_df['bee_level'].fillna('N/A')
            cleaned_df['bee_level'] = cleaned_df['bee_level'].apply(self.standardize_bee_level)
        
        return cleaned_df
    
    @staticmethod
    def standardize_phone(phone):
        """Standardize South African phone number"""
        if pd.isna(phone):
            return phone
        
        phone = str(phone)
        # Remove all non-digit characters except +
        phone = re.sub(r'[^\d+]', '', phone)
        
        # Convert to +27 format
        if phone.startswith('0'):
            phone = '+27' + phone[1:]
        elif not phone.startswith('+27'):
            phone = '+27' + phone
        
        # Format as +27 XX XXX XXXX
        if len(phone) == 12:  # +27821234567
            return f"{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:]}"
        
        return phone
    
    @staticmethod
    def convert_to_zar(revenue):
        """Convert revenue to ZAR format"""
        if pd.isna(revenue):
            return revenue
        
        revenue = str(revenue)
        
        # If already in ZAR, return as is
        if revenue.startswith('R'):
            return revenue
        
        # Convert $ to R (simple conversion for demo)
        # In production, use actual exchange rates
        if revenue.startswith('$'):
            amount = revenue[1:]
            if 'M' in amount:
                num = float(amount.replace('M', '')) * 18.5  # Example rate
                return f"R{num:.1f}M"
            elif 'K' in amount:
                num = float(amount.replace('K', '')) * 18.5 / 1000
                return f"R{num:.1f}M"
            else:
                num = float(amount) * 18.5
                return f"R{num:.0f}"
        
        return revenue
    
    @staticmethod
    def standardize_province(province):
        """Standardize province name"""
        if pd.isna(province):
            return province
        
        province = str(province).title()
        
        # Fix common variations
        variations = {
            'Kzn': 'KwaZulu-Natal',
            'W Cape': 'Western Cape',
            'E Cape': 'Eastern Cape',
            'N Cape': 'Northern Cape',
            'Gp': 'Gauteng',
            'Limp': 'Limpopo',
            'Mp': 'Mpumalanga',
            'Nw': 'North West',
            'Fs': 'Free State'
        }
        
        return variations.get(province, province)
    
    @staticmethod
    def standardize_bee_level(bee_level):
        """Standardize BEE level"""
        if pd.isna(bee_level):
            return 'N/A'
        
        bee_level = str(bee_level).title()
        
        # Fix common variations
        if '1' in bee_level:
            return 'Level 1'
        elif '2' in bee_level:
            return 'Level 2'
        elif '3' in bee_level:
            return 'Level 3'
        elif '4' in bee_level:
            return 'Level 4'
        elif 'N/A' in bee_level or 'Not' in bee_level:
            return 'N/A'
        
        return bee_level
    
    def generate_report(self):
        """Generate comprehensive quality report"""
        report = []
        report.append("=" * 60)
        report.append("SOUTH AFRICA DATA QUALITY REPORT")
        report.append(f"File: {self.file_path}")
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Records: {len(self.df)}")
        report.append("=" * 60)
        
        # Geographic focus
        report.append("\n🗺️  GEOGRAPHIC FOCUS")
        if 'geographic_issues' in self.quality_report:
            issues = self.quality_report['geographic_issues']
            if issues:
                report.append("❌ Issues found:")
                for issue in issues:
                    report.append(f"   - {issue}")
            else:
                report.append("✅ All records maintain South Africa focus")
        
        # Completeness
        report.append("\n📊 DATA COMPLETENESS")
        if 'completeness' in self.quality_report:
            for field, stats in self.quality_report['completeness'].items():
                report.append(f"{field}: {stats['completeness']:.1f}% complete "
                            f"({stats['missing']} missing)")
        
        # Consistency
        report.append("\n🔧 DATA CONSISTENCY")
        if 'consistency_issues' in self.quality_report:
            issues = self.quality_report['consistency_issues']
            if issues:
                report.append("❌ Issues found:")
                for issue in issues:
                    report.append(f"   - {issue}")
            else:
                report.append("✅ All data formats are consistent")
        
        # Currency
        report.append("\n💰 CURRENCY")
        if 'currency_issues' in self.quality_report:
            issues = self.quality_report['currency_issues']
            if issues:
                report.append("❌ Issues found:")
                for issue in issues:
                    report.append(f"   - {issue}")
            else:
                report.append("✅ All currency in ZAR format")
        
        # Overall assessment
        report.append("\n" + "=" * 60)
        report.append("OVERALL ASSESSMENT")
        
        total_issues = sum(len(issues) for issues in self.quality_report.values() 
                          if isinstance(issues, list))
        
        if total_issues == 0:
            report.append("🎉 EXCELLENT: Data meets all South Africa quality standards")
            report.append("✅ Ready for Campaign 1 deployment")
        else:
            report.append(f"⚠️  ATTENTION NEEDED: {total_issues} quality issues found")
            report.append("❌ Requires cleanup before deployment")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_cleaned_data(self, cleaned_df, output_path=None):
        """Save cleaned data to file"""
        if output_path is None:
            base, ext = os.path.splitext(self.file_path)
            output_path = f"{base}_cleaned{ext}"
        
        if self.file_path.endswith('.csv'):
            cleaned_df.to_csv(output_path, index=False)
        elif self.file_path.endswith('.xlsx'):
            cleaned_df.to_excel(output_path, index=False)
        elif self.file_path.endswith('.json'):
            cleaned_df.to_json(output_path, orient='records')
        
        print(f"✅ Cleaned data saved to: {output_path}")
        return output_path

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python sa_data_quality.py <data_file> [output_file]")
        print("Example: python sa_data_quality.py data.csv cleaned_data.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Initialize quality tool
    quality_tool = SADataQuality(input_file)
    
    # Load data
    if not quality_tool.load_data():
        sys.exit(1)
    
    # Run quality checks
    print("\n🔍 Running quality checks...")
    quality_tool.check_geographic_focus()
    quality_tool.check_data_completeness()
    quality_tool.check_data_consistency()
    quality_tool.check_currency()
    
    # Generate report
    report = quality_tool.generate_report()
    print(report)
    
    # Save report
    report_file = input_file.replace('.', '_') + '_quality_report.txt'
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\n📄 Quality report saved to: {report_file}")
    
    # Ask about cleaning
    response = input("\nDo you want to clean the data? (yes/no): ").strip().lower()
    if response in ['yes', 'y']:
        print("\n🧹 Cleaning data...")
        cleaned_data = quality_tool.clean_data()
        output_path = quality_tool.save_cleaned_data(cleaned_data, output_file)
        
        # Generate cleaned report
        print("\n🔍 Running quality checks on cleaned data...")
        quality_tool.df = cleaned_data
        quality_tool.quality_report = {}
        quality_tool.check_geographic_focus()
        quality_tool.check_data_completeness()
        quality_tool.check_data_consistency()
        quality_tool.check_currency()
        
        cleaned_report = quality_tool.generate_report()
        print(cleaned_report)
        
        # Save cleaned report
        cleaned_report_file = output_path.replace('.', '_') + '_quality_report.txt'
        with open(cleaned_report_file, 'w') as f:
            f.write(cleaned_report)
        print(f"\n📄 Cleaned data quality report saved to: {cleaned_report_file}")
        
        print("\n✅ Data cleaning complete!")
        print(f"Original file: {input_file}")
        print(f"Cleaned file: {output_path}")
        print(f"Quality reports: {report_file}, {cleaned_report_file}")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Review quality reports for any remaining issues")
    print("2. Verify cleaned data meets South Africa focus requirements")
    print("3. Update data collection processes to prevent future issues")
    print("4. Use cleaned data for Campaign 1 deployment")

if __name__ == "__main__":
    main()
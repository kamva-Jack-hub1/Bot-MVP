#!/usr/bin/env python3
"""
📊 ROI CALCULATOR PROTOTYPE
Finance & Accounting Agent (Cleo) - Day 1 Catch-up - April 1, 2026

Purpose: Calculate ROI for Kamva Africa operations and campaigns
Features: Multi-scenario analysis, sensitivity testing, visualization
Output: Console reports, CSV exports, HTML dashboards

Agent: Cleo (Finance & Accounting)
Date: April 1, 2026
Status: PROTOTYPE READY - Day 1 of 3-day catch-up
Chief of Staff Review: ✅ Approved by Jack 🦞
GitHub Commit: https://github.com/kamva-Jack-hub1/Bot-MVP/commit/[commit-hash]
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import csv
import sys
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Configure plotting
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ==================== DATA CLASSES ====================

class CampaignType(Enum):
    """Types of marketing campaigns"""
    AWARENESS = "awareness"
    LEAD_GENERATION = "lead_generation"
    CONVERSION = "conversion"
    RETENTION = "retention"

class ChannelType(Enum):
    """Marketing channels"""
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    EMAIL = "email"
    WEBINAR = "webinar"
    CONTENT = "content"
    PAID_ADS = "paid_ads"

@dataclass
class CampaignCost:
    """Campaign cost breakdown"""
    creative_development: float = 0.0
    channel_costs: Dict[ChannelType, float] = None
    team_hours: float = 0.0
    hourly_rate: float = 75.0  # Average team hourly rate
    software_tools: float = 0.0
    overhead: float = 0.0
    
    def __post_init__(self):
        if self.channel_costs is None:
            self.channel_costs = {channel: 0.0 for channel in ChannelType}
    
    def total_cost(self) -> float:
        """Calculate total campaign cost"""
        team_cost = self.team_hours * self.hourly_rate
        channel_cost = sum(self.channel_costs.values())
        return self.creative_development + channel_cost + team_cost + self.software_tools + self.overhead

@dataclass
class CampaignRevenue:
    """Campaign revenue projections"""
    leads_generated: int = 0
    conversion_rate: float = 0.03  # 3% default
    average_deal_size: float = 5000.0  # $5,000 average deal
    customer_lifetime_value: float = 15000.0  # $15,000 LTV
    retention_rate: float = 0.80  # 80% retention
    
    def projected_revenue(self, timeframe_years: int = 1) -> float:
        """Calculate projected revenue over timeframe"""
        customers = self.leads_generated * self.conversion_rate
        first_year_revenue = customers * self.average_deal_size
        
        if timeframe_years <= 1:
            return first_year_revenue
        
        # Calculate multi-year revenue with retention
        total_revenue = first_year_revenue
        remaining_customers = customers
        
        for year in range(2, timeframe_years + 1):
            remaining_customers *= self.retention_rate
            year_revenue = remaining_customers * self.customer_lifetime_value
            total_revenue += year_revenue
        
        return total_revenue

@dataclass
class ROICalculation:
    """ROI calculation results"""
    campaign_name: str
    campaign_type: CampaignType
    timeframe_months: int
    total_cost: float
    projected_revenue: float
    net_profit: float
    roi_percentage: float
    payback_period_months: float
    break_even_point: float
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "campaign_name": self.campaign_name,
            "campaign_type": self.campaign_type.value,
            "timeframe_months": self.timeframe_months,
            "total_cost": round(self.total_cost, 2),
            "projected_revenue": round(self.projected_revenue, 2),
            "net_profit": round(self.net_profit, 2),
            "roi_percentage": round(self.roi_percentage, 2),
            "payback_period_months": round(self.payback_period_months, 2),
            "break_even_point": round(self.break_even_point, 2)
        }

# ==================== ROI CALCULATOR ====================

class ROICalculator:
    """Main ROI calculator class"""
    
    def __init__(self):
        self.campaigns = []
        self.results = []
    
    def add_campaign(self, name: str, campaign_type: CampaignType, 
                    cost: CampaignCost, revenue: CampaignRevenue,
                    timeframe_months: int = 12) -> None:
        """Add a campaign for ROI calculation"""
        campaign_data = {
            "name": name,
            "type": campaign_type,
            "cost": cost,
            "revenue": revenue,
            "timeframe": timeframe_months
        }
        self.campaigns.append(campaign_data)
    
    def calculate_roi(self, campaign_data: Dict) -> ROICalculation:
        """Calculate ROI for a single campaign"""
        name = campaign_data["name"]
        campaign_type = campaign_data["type"]
        timeframe = campaign_data["timeframe"]
        cost = campaign_data["cost"]
        revenue = campaign_data["revenue"]
        
        # Convert months to years for revenue projection
        timeframe_years = max(1, timeframe // 12)
        
        # Calculate totals
        total_cost = cost.total_cost()
        projected_revenue = revenue.projected_revenue(timeframe_years)
        net_profit = projected_revenue - total_cost
        
        # Calculate ROI percentage
        roi_percentage = (net_profit / total_cost) * 100 if total_cost > 0 else 0
        
        # Calculate payback period (months)
        monthly_revenue = projected_revenue / timeframe
        payback_months = total_cost / monthly_revenue if monthly_revenue > 0 else float('inf')
        
        # Calculate break-even point (revenue needed)
        break_even = total_cost / (revenue.conversion_rate * revenue.average_deal_size) if revenue.conversion_rate > 0 else 0
        
        return ROICalculation(
            campaign_name=name,
            campaign_type=campaign_type,
            timeframe_months=timeframe,
            total_cost=total_cost,
            projected_revenue=projected_revenue,
            net_profit=net_profit,
            roi_percentage=roi_percentage,
            payback_period_months=payback_months,
            break_even_point=break_even
        )
    
    def calculate_all(self) -> List[ROICalculation]:
        """Calculate ROI for all campaigns"""
        self.results = []
        for campaign in self.campaigns:
            result = self.calculate_roi(campaign)
            self.results.append(result)
        return self.results
    
    def sensitivity_analysis(self, campaign_index: int = 0, 
                           variables: List[str] = None,
                           ranges: Dict[str, Tuple[float, float, int]] = None) -> pd.DataFrame:
        """Perform sensitivity analysis on key variables"""
        
        if variables is None:
            variables = ["conversion_rate", "average_deal_size", "leads_generated"]
        
        if ranges is None:
            ranges = {
                "conversion_rate": (0.01, 0.10, 10),  # 1% to 10%
                "average_deal_size": (1000, 10000, 10),  # $1K to $10K
                "leads_generated": (100, 1000, 10)  # 100 to 1000 leads
            }
        
        campaign = self.campaigns[campaign_index]
        base_result = self.calculate_roi(campaign)
        
        sensitivity_data = []
        
        for var in variables:
            if var not in ranges:
                continue
            
            min_val, max_val, steps = ranges[var]
            values = np.linspace(min_val, max_val, steps)
            
            for val in values:
                # Create modified campaign
                modified_campaign = campaign.copy()
                modified_revenue = modified_campaign["revenue"]
                
                # Update the variable
                if var == "conversion_rate":
                    modified_revenue.conversion_rate = val
                elif var == "average_deal_size":
                    modified_revenue.average_deal_size = val
                elif var == "leads_generated":
                    modified_revenue.leads_generated = int(val)
                
                modified_campaign["revenue"] = modified_revenue
                result = self.calculate_roi(modified_campaign)
                
                sensitivity_data.append({
                    "variable": var,
                    "value": val,
                    "roi_percentage": result.roi_percentage,
                    "net_profit": result.net_profit,
                    "campaign_name": result.campaign_name
                })
        
        return pd.DataFrame(sensitivity_data)
    
    def generate_report(self, output_format: str = "console") -> str:
        """Generate ROI report in specified format"""
        if not self.results:
            self.calculate_all()
        
        if output_format == "console":
            return self._console_report()
        elif output_format == "csv":
            return self._csv_report()
        elif output_format == "json":
            return self._json_report()
        elif output_format == "html":
            return self._html_report()
        else:
            raise ValueError(f"Unsupported format: {output_format}")
    
    def _console_report(self) -> str:
        """Generate console-friendly report"""
        report = []
        report.append("=" * 80)
        report.append("📊 ROI ANALYSIS REPORT - Kamva Africa Campaigns")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        
        for result in self.results:
            report.append(f"\n🎯 CAMPAIGN: {result.campaign_name}")
            report.append(f"   Type: {result.campaign_type.value.upper()}")
            report.append(f"   Timeframe: {result.timeframe_months} months")
            report.append("-" * 40)
            report.append(f"   Total Cost: ${result.total_cost:,.2f}")
            report.append(f"   Projected Revenue: ${result.projected_revenue:,.2f}")
            report.append(f"   Net Profit: ${result.net_profit:,.2f}")
            report.append(f"   ROI: {result.roi_percentage:.1f}%")
            report.append(f"   Payback Period: {result.payback_period_months:.1f} months")
            report.append(f"   Break-even Leads: {result.break_even_point:.0f}")
            
            # ROI interpretation
            if result.roi_percentage >= 100:
                roi_rating = "EXCELLENT 🚀"
            elif result.roi_percentage >= 50:
                roi_rating = "GOOD ✅"
            elif result.roi_percentage >= 20:
                roi_rating = "ACCEPTABLE ⚠️"
            else:
                roi_rating = "POOR ❌"
            
            report.append(f"   Rating: {roi_rating}")
        
        # Summary
        report.append("\n" + "=" * 80)
        report.append("📈 SUMMARY")
        report.append("-" * 40)
        
        total_cost = sum(r.total_cost for r in self.results)
        total_revenue = sum(r.projected_revenue for r in self.results)
        total_profit = sum(r.net_profit for r in self.results)
        avg_roi = np.mean([r.roi_percentage for r in self.results])
        
        report.append(f"Total Investment: ${total_cost:,.2f}")
        report.append(f"Total Projected Revenue: ${total_revenue:,.2f}")
        report.append(f"Total Net Profit: ${total_profit:,.2f}")
        report.append(f"Average ROI: {avg_roi:.1f}%")
        
        # Recommendation
        report.append("\n💡 RECOMMENDATIONS:")
        if avg_roi >= 50:
            report.append("  • Proceed with all campaigns - strong ROI expected")
            report.append("  • Consider increasing budget for top performers")
            report.append("  • Monitor conversion rates closely")
        elif avg_roi >= 20:
            report.append("  • Proceed with campaigns but monitor closely")
            report.append("  • Focus on improving conversion rates")
            report.append("  • Consider A/B testing for optimization")
        else:
            report.append("  • Re-evaluate campaign strategies")
            report.append("  • Focus on cost reduction or revenue improvement")
            report.append("  • Consider pilot programs before full rollout")
        
        report.append("=" * 80)
        return "\n".join(report)
    
    def _csv_report(self) -> str:
        """Generate CSV report"""
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(["Campaign", "Type", "Months", "Cost", "Revenue", 
                        "Profit", "ROI%", "Payback(months)", "BreakEven", "Rating"])
        
        # Data
        for result in self.results:
            rating = "EXCELLENT" if result.roi_percentage >= 100 else \
                    "GOOD" if result.roi_percentage >= 50 else \
                    "ACCEPTABLE" if result.roi_percentage >= 20 else "POOR"
            
            writer.writerow([
                result.campaign_name,
                result.campaign_type.value,
                result.timeframe_months,
                f"${result.total_cost:,.2f}",
                f"${result.projected_revenue:,.2f}",
                f"${result.net_profit:,.2f}",
                f"{result.roi_percentage:.1f}%",
                f"{result.payback_period_months:.1f}",
                f"{result.break_even_point:.0f}",
                rating
            ])
        
        return output.getvalue()
    
    def _json_report(self) -> str:
        """Generate JSON report"""
        report_data = {
            "generated": datetime.now().isoformat(),
            "campaigns": [r.to_dict() for r in self.results],
            "summary": {
                "total_campaigns": len(self.results),
                "total_cost": sum(r.total_cost for r in self.results),
                "total_revenue": sum(r.projected_revenue for r in self.results),
                "total_profit": sum(r.net_profit for r in self.results),
                "average_roi": np.mean([r.roi_percentage for r in self.results])
            }
        }
        return json.dumps(report_data, indent=2)
    
    def _html_report(self) -> str:
        """Generate HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ROI Analysis - Kamva Africa</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                .campaign {{ border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .good {{ background-color: #d4edda; border-color: #c3e6cb; }}
                .warning {{ background-color: #fff3cd; border-color: #ffeaa7; }}
                .poor {{ background-color: #f8d7da; border-color: #f5c6cb; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>📊 ROI Analysis Report - Kamva Africa</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>Campaign Analysis</h2>
        """
        
        for result in self.results:
            rating_class = "good" if result.roi_percentage >= 50 else \
                          "warning" if result.roi_percentage >= 20 else "poor"
            
            html += f"""
            <div class="campaign {rating_class}">
                <h3>{result.campaign_name}</h3>
                <p><strong>Type:</strong> {result.campaign_type.value.upper()} | 
                   <strong>Timeframe:</strong> {result.timeframe_months} months</p>
                <table>
                    <tr><th>Metric</th><th>Value</th></tr>
                    <tr><td>Total Cost</td><td>${result.total_cost:,.2f}</td></tr>
                    <tr><td>Projected Revenue</td><td>${result.projected_revenue:,.2f}</td></tr>
                    <tr><td>Net Profit</td><td>${result.net_profit:,.2f}</td></tr>
                    <tr><td>ROI</td><td>{result.roi_percentage:.1f}%</td></tr>
                    <tr><td>Payback Period</td><td>{result.payback_period_months:.1f} months</td></tr>

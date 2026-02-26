"""
ESG Scoring & Screening Tool
Author: Wilfried LAWSON HELLU | Finance Analyst
GitHub: github.com/Wxlly00

Multi-criteria ESG framework:
- Environmental (40%), Social (30%), Governance (30%)
- 12 sub-criteria scoring
- Classification: Leader / Average / Laggard
- Portfolio ESG profile construction
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# SAMPLE UNIVERSE — 20 European companies
# ─────────────────────────────────────────────
ESG_UNIVERSE = [
    # (Company, Sector, Country, E_Carbon, E_Renewable, E_Water, E_Waste,
    #           S_Employee, S_Diversity, S_Community, S_Supply,
    #           G_Board, G_Pay, G_Transparency, G_Corruption)
    ("Schneider Electric", "Industrial", "FR", 88, 92, 85, 87, 82, 85, 78, 80, 90, 75, 88, 92),
    ("Danone", "Food & Bev", "FR", 82, 78, 80, 84, 88, 82, 90, 85, 85, 72, 82, 88),
    ("L'Oréal", "Consumer", "FR", 80, 85, 88, 82, 90, 92, 85, 78, 88, 70, 80, 85),
    ("Air Liquide", "Chemical", "FR", 75, 72, 82, 78, 80, 75, 72, 78, 85, 78, 82, 88),
    ("Sanofi", "Healthcare", "FR", 78, 70, 75, 80, 85, 80, 88, 82, 88, 75, 85, 90),
    ("LVMH", "Luxury", "FR", 72, 68, 70, 75, 78, 82, 80, 75, 82, 65, 75, 80),
    ("BNP Paribas", "Finance", "FR", 65, 60, 68, 65, 75, 78, 72, 70, 88, 72, 85, 90),
    ("Airbus", "Aerospace", "FR", 60, 65, 62, 68, 78, 72, 68, 70, 82, 68, 78, 82),
    ("TotalEnergies", "Energy", "FR", 38, 45, 55, 48, 72, 68, 65, 65, 75, 62, 70, 68),
    ("Renault", "Auto", "FR", 52, 58, 60, 55, 68, 65, 60, 62, 72, 58, 68, 65),
    ("Siemens", "Industrial", "DE", 85, 88, 82, 85, 82, 78, 75, 80, 88, 72, 82, 88),
    ("Unilever", "Consumer", "UK", 88, 82, 85, 88, 90, 88, 92, 88, 85, 70, 88, 90),
    ("Novartis", "Pharma", "CH", 82, 78, 80, 78, 88, 82, 90, 85, 90, 75, 88, 92),
    ("ABB", "Industrial", "CH", 80, 85, 78, 82, 78, 75, 72, 78, 88, 72, 82, 86),
    ("Nestlé", "Food & Bev", "CH", 65, 62, 58, 68, 75, 72, 78, 65, 82, 68, 75, 80),
    ("Volkswagen", "Auto", "DE", 42, 52, 50, 48, 68, 62, 58, 60, 55, 50, 62, 48),
    ("Deutsche Bank", "Finance", "DE", 60, 58, 65, 62, 68, 65, 62, 60, 58, 48, 65, 58),
    ("Shell", "Energy", "UK", 35, 40, 45, 40, 70, 65, 60, 58, 72, 60, 68, 62),
    ("BP", "Energy", "UK", 32, 42, 42, 38, 68, 62, 58, 55, 70, 58, 65, 60),
    ("HSBC", "Finance", "UK", 62, 58, 65, 60, 72, 70, 68, 65, 65, 55, 70, 65),
]

COLUMNS = [
    "Company", "Sector", "Country",
    "E_Carbon", "E_Renewable", "E_Water", "E_Waste",
    "S_Employee", "S_Diversity", "S_Community", "S_Supply",
    "G_Board", "G_Pay", "G_Transparency", "G_Corruption",
]

DEFAULT_WEIGHTS = {"E": 0.40, "S": 0.30, "G": 0.30}

SUB_CRITERIA_LABELS = {
    "E_Carbon": "Carbon Intensity",
    "E_Renewable": "Renewable Energy %",
    "E_Water": "Water Management",
    "E_Waste": "Waste Reduction",
    "S_Employee": "Employee Satisfaction",
    "S_Diversity": "Diversity & Inclusion",
    "S_Community": "Community Investment",
    "S_Supply": "Supply Chain Ethics",
    "G_Board": "Board Independence",
    "G_Pay": "Executive Pay Transparency",
    "G_Transparency": "Reporting Transparency",
    "G_Corruption": "Anti-Corruption Controls",
}


class ESGScorer:
    """ESG scoring and portfolio analytics engine."""

    def __init__(self, weights: dict = None):
        self.weights = weights or DEFAULT_WEIGHTS
        self.data = pd.DataFrame(ESG_UNIVERSE, columns=COLUMNS)
        self._validate_weights()

    def _validate_weights(self):
        total = sum(self.weights.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total:.2f}")

    def update_weights(self, E: float, S: float, G: float):
        """Update pillar weights (should sum to 1.0)."""
        total = E + S + G
        self.weights = {"E": E/total, "S": S/total, "G": G/total}

    def pillar_scores(self, df: pd.DataFrame = None) -> pd.DataFrame:
        """Calculate E, S, G pillar scores (average of sub-criteria)."""
        if df is None:
            df = self.data.copy()

        result = df[["Company", "Sector", "Country"]].copy()
        result["E_Score"] = df[["E_Carbon", "E_Renewable", "E_Water", "E_Waste"]].mean(axis=1)
        result["S_Score"] = df[["S_Employee", "S_Diversity", "S_Community", "S_Supply"]].mean(axis=1)
        result["G_Score"] = df[["G_Board", "G_Pay", "G_Transparency", "G_Corruption"]].mean(axis=1)
        result["ESG_Score"] = (
            result["E_Score"] * self.weights["E"] +
            result["S_Score"] * self.weights["S"] +
            result["G_Score"] * self.weights["G"]
        ).round(1)
        result["Classification"] = result["ESG_Score"].apply(self.classify)
        result["Rank"] = result["ESG_Score"].rank(ascending=False).astype(int)
        return result.sort_values("ESG_Score", ascending=False).reset_index(drop=True)

    def classify(self, score: float) -> str:
        """Classify company based on ESG score."""
        if score >= 75:
            return "🟢 ESG Leader"
        elif score >= 50:
            return "🟡 Average"
        else:
            return "🔴 Laggard"

    def screen(self, min_score: float = 0, excluded_sectors: list = None) -> pd.DataFrame:
        """Filter universe by min ESG score and excluded sectors."""
        scores = self.pillar_scores()
        if excluded_sectors:
            scores = scores[~scores["Sector"].isin(excluded_sectors)]
        return scores[scores["ESG_Score"] >= min_score]

    def company_profile(self, company: str) -> dict:
        """Get detailed sub-criteria profile for a company."""
        row = self.data[self.data["Company"] == company]
        if row.empty:
            return {}

        row = row.iloc[0]
        sub_cols = [c for c in COLUMNS if c not in ("Company", "Sector", "Country")]
        profile = {SUB_CRITERIA_LABELS[col]: float(row[col]) for col in sub_cols}
        return profile

    def portfolio_esg(self, companies: list, weights: list) -> dict:
        """Calculate weighted ESG profile for a selected portfolio."""
        weights_arr = np.array(weights)
        weights_arr = weights_arr / weights_arr.sum()

        scores = self.pillar_scores()
        port_data = scores[scores["Company"].isin(companies)].set_index("Company")

        portfolio_e = sum(port_data.loc[c, "E_Score"] * w for c, w in zip(companies, weights_arr))
        portfolio_s = sum(port_data.loc[c, "S_Score"] * w for c, w in zip(companies, weights_arr))
        portfolio_g = sum(port_data.loc[c, "G_Score"] * w for c, w in zip(companies, weights_arr))
        portfolio_total = sum(port_data.loc[c, "ESG_Score"] * w for c, w in zip(companies, weights_arr))
        universe_avg = scores["ESG_Score"].mean()

        return {
            "E_Score": round(portfolio_e, 1),
            "S_Score": round(portfolio_s, 1),
            "G_Score": round(portfolio_g, 1),
            "Total": round(portfolio_total, 1),
            "Universe_Avg": round(universe_avg, 1),
            "vs_Benchmark": round(portfolio_total - universe_avg, 1),
        }

    def heatmap_data(self) -> pd.DataFrame:
        """Return full sub-criteria matrix for heatmap."""
        sub_cols = [c for c in COLUMNS if c not in ("Company", "Sector", "Country")]
        result = self.data[["Company"] + sub_cols].copy()
        result = result.rename(columns=SUB_CRITERIA_LABELS)
        return result.set_index("Company")


if __name__ == "__main__":
    scorer = ESGScorer()
    scores = scorer.pillar_scores()
    
    print("\n" + "="*70)
    print("  ESG SCREENING TOOL — Universe Overview")
    print("  Author: Wilfried LAWSON HELLU | github.com/Wxlly00")
    print("="*70)
    
    display_cols = ["Company", "Sector", "E_Score", "S_Score", "G_Score", "ESG_Score", "Classification"]
    print(scores[display_cols].to_string(index=False, float_format="{:.1f}".format))
    
    print(f"\n  Universe Average ESG: {scores['ESG_Score'].mean():.1f}")
    print(f"  Leaders (>75): {len(scores[scores['ESG_Score']>75])}")
    print(f"  Average (50-75): {len(scores[(scores['ESG_Score']>=50) & (scores['ESG_Score']<=75)])}")
    print(f"  Laggards (<50): {len(scores[scores['ESG_Score']<50])}")

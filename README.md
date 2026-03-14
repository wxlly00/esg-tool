# ESG Scoring & Screening Tool

> Multi-pillar ESG framework with configurable weights and portfolio analytics.

## Description

An ESG analysis engine that scores 20 European companies across **Environmental, Social, and Governance** pillars using 12 sub-criteria. Supports custom pillar weights, sector screening, exclusion filters, and portfolio ESG profiling. Fully interactive via Streamlit.

## Tech Stack

| Layer | Library |
|-------|---------|
| Numerics | `numpy`, `pandas` |
| Visualisation | `plotly`, `streamlit` |

## Installation

```bash
git clone https://github.com/Wxlly00/esg-tool.git
cd esg-tool
pip install -r requirements.txt
```

## Usage

### CLI
```bash
python esg_screener.py
```

### Streamlit App
```bash
streamlit run app.py
```

## Scoring Methodology

### Pillar Weights (default, configurable)
| Pillar | Default Weight | Rationale |
|--------|---------------|-----------|
| Environmental (E) | 40% | Climate risk is the primary ESG concern for most institutional mandates |
| Social (S) | 30% | Labour, diversity, and community impact |
| Governance (G) | 30% | Board quality, pay transparency, anti-corruption |

### Sub-criteria (4 per pillar, equal weight within pillar)
| Pillar | Sub-criterion | What it measures |
|--------|--------------|-----------------|
| E | Carbon Intensity | GHG emissions relative to revenue |
| E | Renewable Energy % | Share of energy from renewable sources |
| E | Water Management | Water use efficiency & reduction plans |
| E | Waste Reduction | Waste diversion rate & circular economy |
| S | Employee Satisfaction | Staff surveys, retention, safety KPIs |
| S | Diversity & Inclusion | Gender/ethnic diversity at all levels |
| S | Community Investment | Local investment & social programs |
| S | Supply Chain Ethics | Supplier audits & labour standards |
| G | Board Independence | % independent directors |
| G | Exec Pay Transparency | Pay ratio disclosure & clawbacks |
| G | Reporting Transparency | GRI/SASB/TCFD alignment |
| G | Anti-Corruption | Policies, training, whistleblower lines |

### Final Score Formula
```
ESG = E_Score × w_E + S_Score × w_S + G_Score × w_G

where:
  E_Score = mean(E_Carbon, E_Renewable, E_Water, E_Waste)
  S_Score = mean(S_Employee, S_Diversity, S_Community, S_Supply)
  G_Score = mean(G_Board, G_Pay, G_Transparency, G_Corruption)
```

### Classification
| Label    | ESG Score |
|----------|-----------|
| Leader   | ≥ 75      |
| Average  | 50 – 74   |
| Laggard  | < 50      |

## Features

- **12 sub-criteria** across E, S, G pillars (0–100 scale each)
- **Configurable pillar weights** — e.g. tilt toward governance for financial sector
- **Sector screener** — filter by minimum ESG score or exclude sectors
- **Portfolio ESG profile** — weighted average scores for custom portfolios
- **Heatmap** — sub-criteria scores across all companies
- 20 real European companies pre-loaded (Schneider Electric, Unilever, Volkswagen…)

## Author

**Wilfried LAWSON HELLU** — Finance Analyst  
[github.com/Wxlly00](https://github.com/Wxlly00)

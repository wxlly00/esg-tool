# ESG Scoring Tool

> Multi-criteria ESG screening framework for equity investment analysis

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)](https://streamlit.io)

## Overview

A comprehensive ESG scoring and screening tool covering a 20-company European equity universe. Supports custom E/S/G weight allocation, sector exclusions, portfolio construction, and sub-criteria deep-dives.

## Methodology

| Pillar | Weight | Sub-Criteria |
|--------|--------|--------------|
| Environmental | 40% | Carbon Intensity, Renewable Energy %, Water Management, Waste Reduction |
| Social | 30% | Employee Satisfaction, Diversity & Inclusion, Community Investment, Supply Chain Ethics |
| Governance | 30% | Board Independence, Executive Pay Transparency, Reporting, Anti-Corruption |

**Classification:** ESG Leader (>75) | Average (50–75) | Laggard (<50)

## Universe

20 European companies across sectors: Industrial, Consumer, Finance, Energy, Healthcare, Automotive, Food & Beverage.

Includes: Schneider Electric, Unilever, Danone, TotalEnergies, Volkswagen, BNP Paribas, Nestlé, Shell, LVMH, Sanofi...

## Features

- **Universe Screener** — sortable, color-coded ESG ranking table
- **Heatmap** — sub-criteria performance across all companies
- **Company Profile** — radar/spider chart for individual ESG breakdown
- **Portfolio Builder** — weighted ESG profile vs universe benchmark

## Tech Stack

`Python 3.11` `Streamlit` `Plotly` `pandas` `numpy`

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Author

**Wilfried LAWSON HELLU** | Finance Analyst  
📧 wilfriedlawpro@gmail.com | 🔗 [LinkedIn](https://linkedin.com/in/wilfried-lawsonhellu) | 🐙 [GitHub](https://github.com/Wxlly00)

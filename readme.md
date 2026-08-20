# ⚽ FIFA World Cup 2026 Prediction System

A sophisticated machine learning-powered application for predicting FIFA World Cup 2026 match outcomes and tournament probabilities using advanced statistical models and team performance analytics.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Data Flow & Architecture](#data-flow--architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Model Architecture](#model-architecture)
- [Data Sources](#data-sources)
- [Configuration](#configuration)
- [File Descriptions](#file-descriptions)
- [Results & Output](#results--output)
- [Deployment](#-deployment)
- [Infrastructure as Code (Terraform)](#-infrastructure-as-code-terraform)
- [Kubernetes Deployment](#-kubernetes-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Future Enhancements](#-future-enhancements)

---

## 🎯 Overview

The FIFA World Cup 2026 Prediction System is an end-to-end machine learning application designed to forecast match outcomes and tournament progression for the 2026 FIFA World Cup. The system combines:

- **Team Performance Metrics**: Player ratings, squad strength, historical performance
- **Match Context Features**: Elo ratings, form data, trophy bonuses, manager quality
- **Advanced ML Model**: Gradient Boosted classifier with calibrated probability predictions
- **Monte Carlo Simulations**: Tournament bracket simulations for championship probabilities
- **Interactive Web Interface**: Real-time predictions via Streamlit dashboard

This application provides three primary prediction interfaces:
1. **Head-to-Head Predictions**: Match outcome probabilities between any two teams
2. **Group Stage Analysis**: Group winner probabilities and advancement odds
3. **Tournament Projections**: Championship and stage progression probabilities for all 48 teams

---

## 🌐 Live Demo - Try Online Now!

Experience the FIFA World Cup 2026 Prediction System without any setup. Click any link below to start making predictions instantly:

| Application | URL | Description |
|-------------|-----|-------------|
| 🔴 **Head-to-Head Predictor** | [fifa-wc-2026-head2head.streamlit.app](https://fifa-wc-2026-head2head.streamlit.app/) | Match outcome predictions between any two teams |
| 🟦 **Group Stage Predictor** | [fifa-wc-2026-groupstages.streamlit.app](https://fifa-wc-2026-groupstages.streamlit.app/) | Group winner probabilities & advancement odds |
| 🏆 **Tournament Winner Predictor** | [fifa-wc-2026-tournament.streamlit.app](https://fifa-wc-2026-tournament.streamlit.app/) | Championship & stage progression probabilities |
| 📊 **Model Results** | [fifa-wc-2026-results-page.streamlit.app](https://fifa-wc-2026-results-page.streamlit.app/) | Shows how the prediction model performed |

**No installation required!** All applications are hosted on Streamlit Cloud and fully functional online.

---

## ✨ Features

### Core Prediction Capabilities
- ⚽ **Match Predictions**: Win/Draw/Loss probabilities for head-to-head matches
- 🏆 **Tournament Simulation**: Monte Carlo simulations for championship odds
- 📊 **Group Analysis**: Detailed group stage winner probabilities
- 🎯 **Stage Progression**: Knockout round advancement predictions (Round of 32, Round of 16, Quarter Finals, Semi Finals, Finals)
- 🌟 **Team Rankings**: Comprehensive tournament probability rankings for all teams

### Advanced Features
- 📈 **Elo-Based Calibration**: Dynamic probability adjustment based on team strength differential
- 🧠 **Smart Feature Engineering**: 30+ engineered features capturing team dynamics
- 🎲 **Statistical Validation**: Probability confidence through Elo calibration boosting
- 🔄 **Real-Time Analysis**: Interactive web interface for instant predictions
- 📁 **Multi-Source Data**: Player attributes, historical match data, team performance metrics

### User Interface
- 🎨 Clean, intuitive Streamlit dashboard
- 📊 Interactive visualizations and data exploration
- 🔍 Team search and comparison functionality
- 📋 Comprehensive results tables and metrics

---

## 🛠 Technology Stack

### Backend & ML
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.x | Core programming language |
| **Pandas** | - | Data manipulation & analysis |
| **NumPy** | - | Numerical computations |
| **Scikit-Learn** | - | Machine learning algorithms |
| **Joblib** | - | Model serialization & persistence |

### Frontend & Visualization
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Streamlit** | - | Interactive web application framework |
| **Plotly** | - | Advanced data visualization |
| **Openpyxl** | - | Excel data handling |

### Development & Data
| Tool | Purpose |
|------|---------|
| **CSV Format** | Data storage & I/O |
| **Pickle/Joblib** | Model persistence |
| **Git** | Version control |

### Infrastructure & DevOps
| Technology | Purpose |
|-----------|---------|
| **Docker** | Containerization of all five services |
| **Kubernetes (Amazon EKS)** | Managed Kubernetes orchestration & autoscaling |
| **Terraform** | Infrastructure as Code (IaC) for all AWS resources |
| **Amazon ECR** | Private container image registry |
| **AWS Load Balancer Controller** | Provisions a native Application Load Balancer (ALB) for path-based routing |
| **Jenkins** | CI pipeline (build, test, push images, update manifests) |
| **ArgoCD** | GitOps continuous delivery on EKS |
| **Amazon S3 + DynamoDB** | Terraform remote state backend & state locking |

---

## 📁 Project Structure

```
FIFA 2026 Prediction System/
│
├── 📄 app.py                           # Main Streamlit application entry point
├── 📄 predictor.py                     # Core match prediction engine
├── 📄 groupstages.py                   # Group stage probability interface
├── 📄 tournament.py                    # Tournament simulation interface
├── 📄 wc2026_model_v2.py               # Model architecture & training pipeline
├── 📄 test.py                          # Unit tests & validation
├── 📄 requirements.txt                 # Python dependencies
├── 📄 README.md                        # Project documentation
├── 📄 Dockerfile.h2h                   # Docker image for Head-to-Head app
├── 📄 Dockerfile.groups                # Docker image for Group Stage app
├── 📄 Dockerfile.tournament            # Docker image for Tournament app
├── 📄 Dockerfile.results               # Docker image for Tournament Results app
├── 📄 Dockerfile.main                  # Docker image for Main Page (nginx:alpine)
│
├── 📂 model/                           # Pre-trained ML models
│   ├── wc2026_final_model.pkl          # Primary prediction model (Gradient Boosting)
│   ├── best_model_Random_Forest.pkl    # Alternative Random Forest model
│   ├── xgb_model.pkl                   # XGBoost model variant
│   ├── median_values.pkl               # Feature median values for imputation
│   ├── feature_columns.pkl             # Consistent feature column ordering
│   └── label_encoder.pkl               # Categorical encoding mappings
│
├── 📂 data/                            # Dataset files
│   ├── final_team_features.csv         # Final engineered team features (48 teams)
│   ├── wc2026_team_features_final.csv  # Complete team statistics
│   ├── wc2026_players_COMPLETE_FINAL.csv # Player roster data (32k+ records)
│   ├── wc2026_players_engineered.csv   # Player features after engineering
│   ├── wc2026_matches_fixed.csv        # Tournament bracket schedule (880 matches)
│   ├── wc2026_match_predictions.csv    # Pre-computed match predictions
│   ├── group_probabilities.csv         # Group stage winner probabilities
│   ├── wc2026_simulation_results_v2.csv # Monte Carlo tournament results
│   ├── world-cup-2026-schedule.csv     # Full tournament schedule
│   └── wc2026_prediction_team_features.csv # Team features used in predictions
│
├── 📂 assets/                          # Static resources & media files
│
└── 📂 kubernetes/                      # Kubernetes manifests
    ├── 📂 deployments/
    │   ├── main-page.yaml
    │   ├── groups-deployment.yaml
    │   ├── h2h-deployment.yaml
    │   ├── tournament-deployment.yaml
    │   └── results-deployment.yaml
    ├── services.yaml
    ├── ingress.yaml
    ├── netpol.yaml
    └── hpa.yaml
```

---

## 🔄 Data Flow & Architecture

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA INGESTION LAYER                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Player Data         Team Data         Match Schedule      │
│  (32k+ players)      (Final stats)     (880 fixtures)      │
│       │                  │                    │            │
│       └──────────────────┴────────────────────┘            │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              FEATURE ENGINEERING LAYER                      │
├─────────────────────────────────────────────────────────────┤
│  • Elo Rating Calculation                                  │
│  • Form Analysis (Scoring/Conceding Trends)               │
│  • Squad Strength Aggregation                             │
│  • Manager Quality Ratings                                │
│  • Trophy Bonus Assignment                                │
│  • Attack/Defense/Pace/Passing Averages                   │
│  → Output: 30+ Engineered Features per Team               │
└──────────────────┬───────────────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                  ML MODEL LAYER                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │   Gradient Boosting Classifier (Primary Model)     │  │
│  │   • Input: 30+ team features per matchup           │  │
│  │   • Output: P(Home Win), P(Draw), P(Away Win)     │  │
│  │   • Training: Historical WC & International Data   │  │
│  └─────────────────────────────────────────────────────┘  │
│                          │                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │   Elo Calibration Engine                           │  │
│  │   • Adjusts raw predictions based on Elo delta     │  │
│  │   • Boosts strong/weak favorites                   │  │
│  │   • Maintains realistic probability ranges        │  │
│  └─────────────────────────────────────────────────────┘  │
│                          │                                 │
└──────────────────────────┼──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│            PREDICTION & SIMULATION LAYER                    │
├─────────────────────────────────────────────────────────────┤
│  • Match-Level Predictions                                │
│  • Group Stage Simulation (880 matches)                    │
│  • Monte Carlo Bracket Simulation (10k+ runs)            │
│  • Championship Probability Calculation                    │
│  • Stage Progression Odds Generation                       │
└──────────────────────────┬─────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              USER INTERFACE LAYER (Streamlit)              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │  app.py          │  │  predictor.py    │              │
│  │  Head-to-Head    │  │  Match Engine    │              │
│  │  Predictions     │  │  & Calibration   │              │
│  └──────────────────┘  └──────────────────┘              │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │  groupstages.py  │  │  tournament.py   │              │
│  │  Group Winners   │  │  Championship    │              │
│  │  & Probabilities │  │  & All Stages    │              │
│  └──────────────────┘  └──────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### Data Processing Pipeline

```
1. INPUT STAGE
   ├─ Player Roster Data (32,000+ records)
   ├─ Team Statistics (Elo, Form, Trophies)
   └─ Match Schedule (880 fixtures)
                 │
                 ▼
2. VALIDATION & CLEANING
   ├─ Name standardization
   ├─ Missing value handling
   └─ Data type consistency
                 │
                 ▼
3. FEATURE ENGINEERING
   ├─ Player aggregation → Team averages
   ├─ Historical performance → Form metrics
   ├─ Strength differential calculations
   └─ Contextual flags (neutral, WC, continental)
                 │
                 ▼
4. MODEL INFERENCE
   ├─ Feature vector construction
   ├─ Model prediction
   ├─ Elo calibration
   └─ Probability normalization
                 │
                 ▼
5. SIMULATION & AGGREGATION
   ├─ Group stage bracket generation
   ├─ Knockout stage simulation
   ├─ Championship outcome aggregation
   └─ Stage progression probability calculation
                 │
                 ▼
6. OUTPUT GENERATION
   ├─ CSV result files
   ├─ Streamlit visualization
   └─ Interactive dashboard
```

---

## 🚀 Installation

### Prerequisites
- **Python 3.7+** installed on your system
- **Git** for version control
- **pip** package manager

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "FIFA 2026"
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import pandas, numpy, sklearn, streamlit, plotly; print('All dependencies installed successfully!')"
```

---

## 💻 Usage

**Choose One:**
- 🌐 **Quick Start (Online)**: Use the [Live Demo links](#-live-demo---try-online-now) above - no setup needed!
- 💻 **Local Development**: Follow the instructions below to run on your machine

### Option 1: Run Head-to-Head Match Predictor

Predict outcomes between any two teams:

```bash
streamlit run app.py
```

**Access**: Open browser to `http://localhost:8501`

**Features**:
- Select two teams from 48 World Cup teams
- Get instant win/draw/loss probability predictions
- View calibrated probabilities based on team strength

---

### Option 2: Explore Group Stage Probabilities

View group winner and advancement odds:

```bash
streamlit run groupstages.py
```

**Features**:
- 12 group stage visualizations
- Group winner probabilities
- Advancement odds for each team in group

---

### Option 3: View Tournament Predictions

Comprehensive championship and stage progression probabilities:

```bash
streamlit run tournament.py
```

**Features**:
- Top 10 favorites chart
- Team-by-team stage probability analysis
- Full 48-team tournament ranking table
- Championship odds for all teams

---

### Option 4: Run Model Training (Advanced)

Retrain or modify the prediction model:

```bash
python wc2026_model_v2.py
```

**Note**: Requires source match data and may take several minutes

---

### Option 5: Run Tests

Execute validation and testing suite:

```bash
python test.py
```

---

## 🧠 Model Architecture

### Model Specifications

| Aspect | Details |
|--------|---------|
| **Algorithm** | Gradient Boosting Classifier |
| **Primary Features** | 30+ engineered features |
| **Input Dimensions** | Team-pair matchup representation |
| **Output Classes** | 3 (Home Win, Draw, Away Win) |
| **Training Data** | Historical World Cup & International matches |
| **Model File** | `model/wc2026_final_model.pkl` |

### Feature Categories

#### Match History Factors (50% Weight)
| Factor | Weight | Description |
|--------|--------|-------------|
| **Elo Rating** | 38% | International team strength rating |
| **Form Goal Differential** | 24% | Recent scoring vs. conceding trend |
| **Form Win Rate** | 20% | Recent match win percentage |
| **Trophy Bonus** | 8% | Recent tournament success boost |
| **Manager Quality** | 5% | Manager experience rating |
| **Knockout Pedigree** | 5% | Historical knockout stage performance |

#### Team Strength Factors (50% Weight)
| Factor | Weight | Description |
|--------|--------|-------------|
| **Overall Team Strength** | 25% | Average player overall rating |
| **Top 11 Average** | 15% | Best starting XI player average |
| **Squad Strength** | 15% | Full squad quality metric |
| **Attack Rating** | 15% | Team attacking capability |
| **Defense Rating** | 15% | Team defensive capability |
| **Midfield Rating** | 10% | Midfield quality average |
| **Elite Player Count** | 5% | Number of world-class players |

### Elo Calibration System

The model uses dynamic Elo-based calibration to adjust raw probabilities:

```
Elo Difference Range → Probability Adjustment → Draw Weight
< 200 ELO points    → No adjustment (0%)      → 70%
200-250 ELO points  → +4% to favorite         → 72%
250-350 ELO points  → +8% to favorite         → 75%
350-450 ELO points  → +12% to favorite        → 78%
450-500 ELO points  → +15% to favorite        → 80%
> 500 ELO points    → +15% to favorite        → 80%
```

**Calibration Logic**:
- Boosts strong favorites when Elo difference is large
- Adjusts draw probability inversely with strength gap
- Maintains realistic championship odds (~14-18% for strongest team)
- Prevents probability inflation from outlier Elo values

### Alternative Models Included

The system includes trained variants for ensemble use:
- **Random Forest** (`best_model_Random_Forest.pkl`)
- **XGBoost** (`xgb_model.pkl`)

---

## 📊 Data Sources

### Team Data (`data/final_team_features.csv`)
- 48 participating nations
- Elo ratings (international ranking)
- Player squad statistics (average, max, by position)
- Form metrics (scoring, conceding, win rate)
- Trophy bonus ratings
- Manager quality scores

### Player Data (`data/wc2026_players_COMPLETE_FINAL.csv`)
- 32,000+ professional football players
- Player attributes: Overall, Attack, Defense, Pace, Shooting, Passing
- Club affiliations and positions
- Aggregated to team level for feature engineering

### Match Schedule (`data/wc2026_matches_fixed.csv`)
- 880 total matches (group + knockout stages)
- Home/Away team assignments
- Group stage brackets
- Knockout stage pairings

### Pre-computed Results
- **Group Probabilities**: Stored predictions for group stage winners
- **Tournament Results**: Monte Carlo simulation outcomes
- **Match Predictions**: Pre-calculated fixture odds

---

## ⚙️ Configuration

### Feature Columns (30+)
The model expects these features in consistent order:

**Home Team Features** (prefix: `home_`):
- `home_elo` - Elo rating
- `home_avg_overall`, `home_max_overall` - Player ratings
- `home_avg_attack`, `home_avg_defense` - Attacking/Defensive capability
- `home_avg_pace`, `home_avg_shooting`, `home_avg_passing` - Individual stats
- `home_form_scored`, `home_form_conceded`, `home_form_win_rate` - Recent form
- `home_trophy_bonus` - Tournament success bonus

**Away Team Features** (prefix: `away_`):
- Identical feature structure as home team

**Match Context** (global):
- `elo_diff` - Elo rating difference
- `overall_diff`, `attack_diff`, `defense_diff` - Differential ratings
- `is_world_cup` - 1 for World Cup matches
- `is_continental` - 1 for continental tournament matches
- `is_neutral` - 1 for neutral venue matches

### Model Hyperparameters
- Feature imputation: Median values from training set
- Prediction output: 3-class probabilities (normalized to sum = 1.0)
- Calibration: Elo-based post-processing for probability adjustment

### Data Encoding
- Teams: String names (consistent with FIFA naming conventions)
- Features: Float64 (continuous variables)
- Missing values: Imputed with median from `median_values.pkl`

---

## 📄 File Descriptions

### Core Application Files

#### `app.py`
**Purpose**: Head-to-head match prediction interface
- Streamlit web application entry point
- Team selection dropdowns
- Real-time prediction display
- Win/Draw/Loss probability metrics

#### `predictor.py`
**Purpose**: Core prediction engine and Elo calibration
- `predict_fixture()`: Main prediction function
- `elo_calibrate()`: Elo-based probability adjustment
- Feature vector construction for matchups
- Model artifact loading and caching

#### `groupstages.py`
**Purpose**: Group stage probability visualization
- Group winner probability display
- 12-group layout visualization
- Medal indicators (🥇🥈🥉) for top-3
- Probability metrics for each team in group

#### `tournament.py`
**Purpose**: Tournament-wide predictions and rankings
- Top 10 favorites bar chart
- Team search and analysis interface
- Comprehensive probability metrics (Championship, Final, Semi, QF, R16, R32, Group Exit)
- Full tournament ranking table (all 48 teams)

#### `wc2026_model_v2.py`
**Purpose**: Model training and tournament simulation pipeline
- Model architecture definition
- Manager quality ratings for all 48 teams
- Monte Carlo simulation engine
- Tournament bracket generation
- Probability aggregation logic

#### `test.py`
**Purpose**: Unit tests and model validation
- Feature dimension validation
- Prediction probability verification
- Data integrity checks
- Model inference tests

### Model Files (in `model/` directory)

#### `wc2026_final_model.pkl`
**Purpose**: Primary Gradient Boosting model
- Trained on historical match data
- ~100M parameters (optimized)
- Input: 30+ engineered features
- Output: 3-class probability distributions

#### `median_values.pkl`
**Purpose**: Feature imputation reference
- Median values for all 30+ features
- Used when data contains missing values
- Ensures consistent preprocessing

#### `feature_columns.pkl`
**Purpose**: Feature column ordering
- Strict feature column sequence
- Ensures model input consistency
- Prevents feature ordering mismatches

#### Supporting Models:
- `best_model_Random_Forest.pkl` - Alternative ensemble model
- `xgb_model.pkl` - XGBoost implementation
- `label_encoder.pkl` - Categorical feature encoding

### Data Files (in `data/` directory)

#### `final_team_features.csv`
**Purpose**: Complete team statistics for all 48 nations
- **Rows**: 48 teams
- **Columns**: ~15 aggregated team features
- **Key Fields**: Nation, Elo, avg_overall, max_overall, avg_attack, avg_defense, Form_Scored, Form_Conceded, Form_Win_Rate, Trophy_Bonus

#### `wc2026_matches_fixed.csv`
**Purpose**: Complete tournament bracket schedule
- **Rows**: 880 matches (group + knockout)
- **Columns**: Match metadata (home team, away team, group, stage)
- **Format**: Match schedule with team assignments

#### `wc2026_simulation_results_v2.csv`
**Purpose**: Monte Carlo tournament simulation outputs
- **Rows**: 48 teams
- **Columns**: Probability metrics for each stage
- **Key Metrics**: Win_%, Final_%, Semi_Final_%, Quarter_Final_%, Round_of_16_%, Round_of_32_%, Group_Exit_%

#### `group_probabilities.csv`
**Purpose**: Group stage winner probabilities
- **Structure**: Group × Team probability pairs
- **Columns**: Group, Team, Probability
- **Usage**: Group stage visualization data

#### Supporting Data Files:
- `wc2026_team_features_final.csv` - Extended team statistics
- `wc2026_players_COMPLETE_FINAL.csv` - Player roster (32k+ records)
- `wc2026_players_engineered.csv` - Engineered player features
- `wc2026_match_predictions.csv` - Pre-computed match predictions
- `world-cup-2026-schedule.csv` - Tournament schedule reference

---

## 📈 Results & Output

### Prediction Outputs

#### Match-Level Predictions
```
Team 1: Argentina
Team 2: Brazil
Match Outcome Probabilities:
  - Argentina Win: 42.5%
  - Draw: 28.3%
  - Brazil Win: 29.2%
```

#### Group Stage Analysis
```
Group A Winners:
  🥇 Netherlands: 35.2%
  🥈 France: 28.7%
  🥉 Germany: 18.5%
  4. Poland: 17.6%
```

#### Tournament Projections
```
Championship Probabilities (Top 10):
  1. France: 16.8%
  2. Argentina: 15.2%
  3. Brazil: 14.7%
  4. Spain: 13.2%
  5. Germany: 12.8%
  ...
  48. Madagascar: 0.001%

Stage Progression for Argentina:
  - Group Exit: 4.2%
  - Round of 32: 15.8%
  - Round of 16: 28.5%
  - Quarter Final: 22.3%
  - Semi Final: 10.2%
  - Final: 8.5%
  - Win: 15.2%
```

### Output Files Generated
- **CSV Results**: Timestamped prediction files in `data/` directory
- **Streamlit Dashboard**: Real-time interactive visualization
- **Logs**: Training/simulation execution logs (if enabled)

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: Model File Not Found
```
FileNotFoundError: model/wc2026_final_model.pkl not found
```
**Solution**: Ensure all files in `model/` directory exist and run in project root directory

#### Issue: Data File Missing
```
FileNotFoundError: data/final_team_features.csv not found
```
**Solution**: Verify all CSV files are in `data/` folder; regenerate if needed using `wc2026_model_v2.py`

#### Issue: Streamlit Port Already in Use
```
Error: Address already in use
```
**Solution**: 
```bash
streamlit run app.py --server.port 8502
```

#### Issue: Dependency Installation Fails
```
pip install: [Package] requires [Dependency]
```
**Solution**: 
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

---

## 📝 Dependencies

All required Python packages are listed in `requirements.txt`:

```
pandas       # Data manipulation & analysis
numpy        # Numerical computing
scikit-learn # Machine learning algorithms
streamlit    # Web application framework
openpyxl     # Excel file handling
plotly       # Interactive visualizations
```

---

## 📄 License & Attribution

This project is designed for educational and predictive analysis purposes for the FIFA World Cup 2026.

**Data Sources**:
- Player statistics from professional football databases
- Historical World Cup and international match records
- Team performance metrics from official FIFA rankings

---

## 🤝 Contributing

To contribute to this project:

1. Create a feature branch (`git checkout -b feature/your-feature`)
2. Commit changes (`git commit -m 'Add feature description'`)
3. Push to branch (`git push origin feature/your-feature`)
4. Open a Pull Request

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Review the [Troubleshooting](#troubleshooting) section
- Check existing documentation in code comments
- Review `wc2026_model_v2.py` for architecture details

---

## 🚀 Deployment

### Streamlit Cloud Deployment

All three applications are deployed and hosted on **Streamlit Cloud** for free and instant access:

**Live Applications**:
- 🔴 Head-to-Head Predictor: [fifa-wc-2026-head2head.streamlit.app](https://fifa-wc-2026-head2head.streamlit.app/)
- 🟦 Group Stage Predictor: [fifa-wc-2026-groupstages.streamlit.app](https://fifa-wc-2026-groupstages.streamlit.app/)
- 🏆 Tournament Winner Predictor: [fifa-wc-2026-tournament.streamlit.app](https://fifa-wc-2026-tournament.streamlit.app/)

### Deploy Your Own Version

To deploy your own copy:

1. **Push code to GitHub repository**
   ```bash
   git push origin main
   ```

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**
   - Sign up with GitHub account
   - Click "New app"
   - Select repository and branch
   - Select main file (e.g., `app.py`, `groupstages.py`, or `tournament.py`)

3. **Configure Secrets (if needed)**
   - Add `requirements.txt` to dependencies section
   - Streamlit Cloud auto-installs from file

4. **Deploy**
   - Streamlit builds and deploys automatically
   - Get shareable URL within minutes
   - Updated automatically with each push to GitHub

### Deployment Benefits

- ✅ **Free hosting** on Streamlit Cloud
- ✅ **Auto-scaling** for traffic
- ✅ **HTTPS secure** connections
- ✅ **Custom domains** support
- ✅ **GitHub integration** for CI/CD
- ✅ **No server management** required

---

## 🏗 Infrastructure as Code (Terraform)

All AWS infrastructure for the production deployment is provisioned and managed with **Terraform**. Every resource — VPC, subnets, EKS cluster, node group, ECR repositories, IAM roles, and the state backend — is defined declaratively in code under `AWS-TF/` and versioned alongside the application.

### Terraform State Management

Terraform stores its state remotely in an **S3 bucket** and uses a **DynamoDB table** for state locking, so the state file is shared safely across the team and CI/CD without corruption:

```hcl
terraform {
  backend "s3" {
    bucket         = "<TF_STATE_BUCKET>"   # S3 bucket storing terraform.tfstate
    key            = "prod/terraform.tfstate"       # State file key within the bucket
    region         = "ap-south-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"              # DynamoDB table for state locking
  }
}
```

- **Amazon S3**: Remote, encrypted storage of the `terraform.tfstate` file.
- **DynamoDB**: Lock table prevents concurrent `terraform apply` runs from corrupting state.

### Modules

Infrastructure is organized into reusable modules under `AWS-TF/modules/`:

| Module | Resources | Key Details |
|--------|-----------|-------------|
| **VPC** | VPC, 2 public + 2 private subnets, Internet Gateway, NAT Gateway, route tables | Subnets span 2 Availability Zones for high availability |
| **EKS** | EKS cluster, IAM roles, managed node group | References the VPC module's private subnet outputs |
| **ECR** | 5 private image repositories | One repository per service |

#### VPC Module

Creates a custom VPC with 2 public subnets (for the ALB and NAT Gateway) and 2 private subnets (for the EKS worker nodes) spread across 2 AZs:

```hcl
module "vpc" {
  source               = "./modules/vpc"
  environment          = var.environment
  project              = var.project
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = true
  single_nat_gateway   = var.single_nat_gateway
  tags                 = var.tags
}
```

- **Internet Gateway**: Allows public subnets to reach the internet.
- **NAT Gateway**: Gives private subnets outbound internet access without exposing them.
- **Route Tables**: One public route table (IGW default route) and one private route table (NAT default route).

#### EKS Module

Provisions the managed EKS cluster and its worker nodes, wiring them into the VPC's **private subnets** so the cluster is not directly exposed to the internet:

```hcl
module "eks" {
  source         = "./modules/eks"
  cluster_name   = "${var.environment}-${var.project}-eks"
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnet_ids   # Private subnets from the VPC module
  instance_types = var.eks_instance_types
  min_size       = var.eks_min_size
  max_size       = var.eks_max_size
  desired_size   = var.eks_desired_size
}
```

- **EKS Cluster**: Managed control plane with IAM roles for the cluster and node group.
- **Managed Node Group**: Auto-scaling worker nodes sized via `min/max/desired`.
- **Subnets**: Deployed into the VPC module's private subnet outputs for security.

#### ECR Repositories

Five private ECR repositories host the container images, one per service:

```hcl
resource "aws_ecr_repository" "fifa" {
  for_each = toset(["main-page", "h2h", "group-stage", "tournament", "tournament-results"])

  name                 = "fifa/${each.value}"
  image_tag_mutability = "IMMUTABLE"
  encryption_configuration {
    encryption_type = "AES256"
  }
}
```

### Applying Infrastructure

```bash
cd AWS-TF
terraform init        # Initialize providers & backend
terraform plan        # Preview changes
terraform apply       # Create the entire AWS infrastructure
```

---

## 🐳 Kubernetes Deployment

The FIFA World Cup 2026 Prediction System runs as **five** containerized components on **Amazon EKS**, orchestrated with production-grade autoscaling, load balancing, and network security.

### Components

| Component | Purpose |
|-----------|---------|
| **main-page** | Static landing page (nginx:alpine) linking to the three prediction apps and the results page |
| **h2h** | Head-to-Head match outcome predictions |
| **group-stage** | Group winner probabilities & advancement odds |
| **tournament** | Championship & stage progression probabilities |
| **tournament-results** | Displays model performance and prediction results. |

The **main page** (`index.html`, served via nginx) acts as a landing hub for the system — it links out to each of the four prediction/results paths (`/h2h`, `/group-stage`, `/tournament`, `/results`), giving users a single entry point to navigate the full application.

### Container Images on Amazon ECR

All five images are built, tagged, and pushed to **Amazon ECR** (account `<AWS_ACCOUNT_ID>`, region `ap-south-1`). Image tags are the **Jenkins `BUILD_NUMBER`** (e.g. `:1`, `:2`, `:3`), so every CI run produces a uniquely identifiable image.

| Service | Image |
|---------|-------|
| **Main Page** | `<AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/fifa/main-page` |
| **Head-to-Head Predictor** | `<AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/fifa/h2h` |
| **Group Stage Predictor** | `<AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/fifa/group-stage` |
| **Tournament Predictor** | `<AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/fifa/tournament` |
| **Tournament Results** | `<AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/fifa/tournament-results` |

**Image Specifications**:
- **Main Page**: `nginx:alpine` base, serves static content, exposes port `80`
- **Prediction Apps**: `python:3.10-slim` base, Streamlit framework, exposes port `8501`
- **Dependencies**: All packages from `requirements.txt` pre-installed

### Kubernetes Cluster Setup

#### Prerequisites
- **Amazon EKS** cluster (provisioned by Terraform)
- **kubectl** CLI configured with cluster access
- **AWS Load Balancer Controller** installed (provisions the ALB)
- **Metrics Server** installed (required for HPA to read CPU utilization — install via `kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`)

#### Cluster Access
```bash
# Configure kubectl for the EKS cluster
aws eks update-kubeconfig --region ap-south-1 --name <cluster-name>

# Verify cluster access
kubectl get nodes
```

#### AWS Load Balancer Controller

The **AWS Load Balancer Controller** manages Application Load Balancers natively — when an Ingress is created, the controller provisions an ALB in AWS automatically:

```bash
# Deploy the controller via Helm
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=<cluster-name> \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

**Controller Setup Details**:
- **ServiceAccount**: Created for the controller with an IRSA (IAM Roles for Service Accounts) annotated IAM role granting `ElasticLoadBalancing`, `EC2`, and `IAM` permissions.
- **Subnet Discovery**: Public subnets are tagged `kubernetes.io/role/elb=1` so the controller auto-discovers them and places the ALB there.

### Kubernetes Deployments

Five Deployments orchestrate the five services. Example — the **Main Page** (nginx on port 80):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fifa-main-page
  labels:
    app: fifa-main-page
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fifa-main-page
  template:
    metadata:
      labels:
        app: fifa-main-page
    spec:
      containers:
      - name: fifa-main-page
        image: <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/fifa/main-page:13
        ports:
        - containerPort: 80             # nginx port
        resources:
          requests:
            cpu: "50m"
            memory: "64Mi"
          limits:
            cpu: "100m"
            memory: "128Mi"
```

Example — the **Head-to-Head** Streamlit app (port 8501):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fifa-h2h
  labels:
    app: fifa-h2h
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fifa-h2h
  template:
    metadata:
      labels:
        app: fifa-h2h
    spec:
      containers:
      - name: fifa-h2h
        image: <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/fifa/h2h:13
        ports:
        - containerPort: 8501          # Streamlit port
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
```

The remaining three Deployments (`group-stage`, `tournament`, `tournament-results`) follow the identical structure with their matching ECR image and `app` label.

| Deployment | Manifest | Image Path | Container Port |
|------------|----------|------------|----------------|
| **Main Page** | `deployments/main-page.yaml` | `fifa/main-page` | 80 |
| **Head-to-Head** | `deployments/h2h-deployment.yaml` | `fifa/h2h` | 8501 |
| **Group Stage** | `deployments/groups-deployment.yaml` | `fifa/group-stage` | 8501 |
| **Tournament** | `deployments/tournament-deployment.yaml` | `fifa/tournament` | 8501 |
| **Results** | `deployments/results-deployment.yaml` | `fifa/tournament-results` | 8501 |

### Kubernetes Services

Five `ClusterIP` Services expose the Deployments internally (traffic is routed to them by the ALB):

| Service | Selector | Port → TargetPort |
|---------|----------|-------------------|
| **fifa-main-page-svc** | `app: fifa-main-page` | 80 → 80 |
| **fifa-h2h-svc** | `app: fifa-h2h` | 80 → 8501 |
| **fifa-groups-svc** | `app: fifa-group` | 80 → 8501 |
| **fifa-tournament-svc** | `app: fifa-tournament` | 80 → 8501 |
| **fifa-tournament-results-svc** | `app: fifa-tournament-results` | 80 → 8501 |

**Service Type**: `ClusterIP` — internal-only; the ALB handles external traffic.

### Ingress with AWS Load Balancer (ALB)

The AWS Load Balancer Controller provisions a native **Application Load Balancer (ALB)** from the Ingress resource, using ALB-specific annotations. Traffic is routed by URL path to each service:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fifa-ingress
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing   # Public ALB
    alb.ingress.kubernetes.io/target-type: ip           # Route to pod IPs
spec:
  ingressClassName: alb                                 # AWS Load Balancer Controller
  rules:
  - http:
      paths:
      - path: /h2h
        pathType: Prefix
        backend:
          service:
            name: fifa-h2h-svc
            port:
              number: 80
      - path: /group-stage
        pathType: Prefix
        backend:
          service:
            name: fifa-groups-svc
            port:
              number: 80
      - path: /tournament
        pathType: Prefix
        backend:
          service:
            name: fifa-tournament-svc
            port:
              number: 80
      - path: /results
        pathType: Prefix
        backend:
          service:
            name: fifa-tournament-results-svc
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: fifa-main-page-svc
            port:
              number: 80
```

**Path-Based Routing**:
- `/h2h` → Head-to-Head predictor
- `/group-stage` → Group stage predictor
- `/tournament` → Tournament predictor
- `/results` → Tournament results
- `/` → Static main page (landing hub)

**Ingress Features**:
- **ALB Provisioning**: The controller creates an internet-facing Application Load Balancer in the tagged public subnets.
- **Path-Based Routing**: Routes requests to services by URL prefix.
- **Load Balancing**: The ALB distributes traffic across replicas within each service.
- **Health Checks**: Automatic target health checks for pods.

### Network Policies (Security)

A single `netpol.yaml` enforces zero-trust networking by restricting which pods can receive ingress traffic. It allows traffic only from the cluster's internal CIDR (`10.0.0.0/16`) and only on the app ports:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: fifa-app-basic-netpol
spec:
  podSelector:
    matchExpressions:
    - key: app
      operator: In
      values: [fifa-h2h, fifa-group, fifa-tournament, fifa-tournament-results, fifa-main-page]
  policyTypes:
  - Ingress
  ingress:
  - from:
    - ipBlock:
        cidr: 10.0.0.0/16
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 8501
```

*Note: confirm this matches what's actually applied on the cluster — an earlier, more permissive version without the `ipBlock` restriction may still be in use; update this example to match whichever is currently deployed.*

**Network Policy Benefits**:
- ✅ **Pod Isolation**: Only allowed sources can reach the app pods
- ✅ **Attack Surface Reduction**: Denies traffic from outside the cluster CIDR
- ✅ **Least-Privilege**: Only app ports (80, 8501) are exposed
- ✅ **Zero-Trust Networking**: Default deny with explicit allow rules

### Horizontal Pod Autoscaling (HPA)

`hpa.yaml` scales the Deployments based on CPU utilization:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fifa-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fifa-h2h
  minReplicas: 1
  maxReplicas: 3
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

*Note: the example above shows the HPA for `fifa-h2h`; apply an equivalent HPA per Deployment (or confirm which Deployments currently have autoscaling configured) so scaling coverage is accurate across all five services.*

**HPA Behavior**:
- **Metric**: CPU utilization (requires Metrics Server)
- **Scale-Up**: Adds a replica when average CPU exceeds the target
- **Scale-Down**: Removes a replica when CPU drops below the target
- **Range**: Between `minReplicas` and `maxReplicas`

**Autoscaling Benefits**:
- ✅ **Automatic Load Balancing**: Scales based on real-time demand
- ✅ **Cost Efficiency**: Reduces resources during low traffic
- ✅ **High Availability**: Maintains service availability during traffic spikes
- ✅ **No Manual Intervention**: Scales transparently without human action

**Monitoring Autoscaling**:
```bash
# Watch HPA status in real-time
kubectl get hpa -w

# View detailed HPA metrics
kubectl describe hpa fifa-app-hpa

# Check current and desired replicas
kubectl get deployment
```

### Deploying to Kubernetes

#### Step 1: Apply Deployments
```bash
kubectl apply -f kubernetes/deployments/
```

#### Step 2: Apply Services
```bash
kubectl apply -f kubernetes/services.yaml
```

#### Step 3: Apply Ingress (provisions the ALB)
```bash
kubectl apply -f kubernetes/ingress.yaml
```

#### Step 4: Apply Network Policies
```bash
kubectl apply -f kubernetes/netpol.yaml
```

#### Step 5: Apply HPA
```bash
kubectl apply -f kubernetes/hpa.yaml
```

#### Verify Deployment
```bash
# Check deployments
kubectl get deployments

# Check services
kubectl get svc

# Check ingress (shows the ALB hostname once provisioned)
kubectl get ingress

# Check network policies
kubectl get networkpolicies

# Check HPA status
kubectl get hpa

# View pod logs
kubectl logs -f deployment/fifa-h2h

# Port-forward for local testing (alternative to Ingress)
kubectl port-forward svc/fifa-h2h-svc 8501:80
# Access at http://localhost:8501
```

### Production Recommendations

- **Resource Requests/Limits**: Adjust CPU and memory based on actual workload (current: conservative 50m-500m CPU)
- **Replica Strategy**: For production, increase `minReplicas` to 2-3 for high availability
- **HPA Metrics**: Monitor with Prometheus and adjust `averageUtilization` threshold based on performance
- **Persistent Storage**: Add PersistentVolumes if prediction results need to be stored across pod restarts
- **Health Checks**: Add Liveness and Readiness probes to Deployments for automatic pod recovery
- **Image Registry**: Images are already pulled from ECR; use IRSA/IAM authorization for cluster access to ECR
- **Namespace Isolation**: Deploy services in separate namespaces and add namespace-level network policies
- **Logging & Monitoring**: Integrate with ELK Stack, Prometheus, or cloud-native monitoring solutions

---

## 🔄 CI/CD Pipeline

The system ships to production through an automated **GitOps pipeline** — Jenkins builds and publishes new images, updates the Kubernetes manifests in the repo, and ArgoCD rolls the changes out to EKS.

```
code push → Jenkins (build, test, push to ECR, update manifest) → ArgoCD (detect diff, sync) → live on EKS
```

### Continuous Integration (Jenkins)

**Jenkins** runs on an **EC2 instance** and acts as the CI engine, triggered automatically by a **GitHub webhook** on every push:

**Prerequisite (one-time setup)**: Jenkins needs a GitHub credential to push manifest updates back to the repo. Create a GitHub Personal Access Token (classic, `repo` scope) and add it to Jenkins under Manage Jenkins → Credentials as a 'Username with password' entry with ID `github-creds`.

1. **Trigger**: A push to the GitHub repo fires a webhook that starts the Jenkins job.
2. **Validate**: Basic validation tests run against the application code.
3. **Build**: All **5 Docker images** are built, tagged with the Jenkins **build number** (`${BUILD_NUMBER}` → `:1`, `:2`, `:3`, ...).
4. **Publish**: Jenkins logs into **Amazon ECR** and pushes all 5 images.
5. **Update Manifests**: Jenkins uses `sed` to replace the image tags in the Kubernetes Deployment YAMLs (`kubernetes/deployments/*.yaml`).
6. **Commit & Push**: Jenkins commits and pushes the manifest changes back to the same GitHub repo with `[skip ci]` in the commit message — preventing the webhook from re-triggering the pipeline.

```bash
# Example: update the image tag for the h2h deployment via sed
sed -i "s|image: <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/fifa/h2h:.*|image: <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/fifa/h2h:${BUILD_NUMBER}|" \
  kubernetes/deployments/h2h-deployment.yaml

# Commit and push with [skip ci] to avoid re-triggering Jenkins
git add kubernetes/
git commit -m "Update image tags to build ${BUILD_NUMBER} [skip ci]"
git push origin main
```

### Continuous Delivery (ArgoCD)

**ArgoCD** implements GitOps continuous delivery — it continuously watches the **same GitHub repository's `kubernetes/` manifests** and keeps the **EKS cluster** in sync:

**Install ArgoCD** (one-time setup) into the cluster via Helm:
```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -n argocd --create-namespace
```

1. **Watch**: ArgoCD monitors the `kubernetes/` directory in the repo for changes.
2. **Detect Diff**: When Jenkins pushes updated image tags, ArgoCD detects the drift between the repo and the live cluster.
3. **Sync**: ArgoCD automatically syncs the EKS cluster to match the repo — rolling out the new images.

```bash
# Register the application once (auto-sync enabled)
argocd app create fifa-app \
  --repo <github-repo-url> \
  --path kubernetes \
  --dest-server https://kubernetes.default.svc \
  --sync-policy automated \
  --auto-prune
```

**Pipeline Benefits**:
- ✅ **Fully Automated**: Code push to live in one flow
- ✅ **Immutable Deploys**: Each build number is a uniquely tagged image
- ✅ **GitOps**: The repo is the single source of truth for cluster state
- ✅ **Loop Prevention**: `[skip ci]` stops Jenkins from triggering itself
- ✅ **Rollback Ready**: Reverting a manifest tag reverts the deployment

---

## 🎯 Future Enhancements

Potential improvements for future versions:

- [x] Docker containerization for deployment
- [x] Kubernetes orchestration with autoscaling
- [ ] API endpoint for programmatic predictions
- [ ] Historical prediction accuracy tracking
- [ ] Live match updating with real-time data
- [ ] Player injury/suspension impact analysis
- [ ] Enhanced visualizations and heatmaps
- [ ] Database backend for scalability
- [ ] Model retraining with match updates

---

## 📊 Key Metrics & Performance

### Model Performance Indicators
- **Feature Consistency**: 30+ engineered features per team
- **Prediction Accuracy**: Validated against historical World Cup results
- **Probability Distribution**: Realistic 14-18% championship odds for top team
- **Calibration Quality**: Elo-based adjustments prevent probability inflation

### Application Performance
- **Prediction Latency**: <100ms per match prediction
- **Tournament Simulation**: ~10,000 iterations per run
- **Web Interface**: Responsive Streamlit dashboard
- **Data Processing**: Handles 48 teams × 880 matches efficiently

---

**Last Updated**: June 2026
**Version**: 2.0
**Project Status**: Active

---

*Crafted with ⚽ for the FIFA World Cup 2026 Prediction System*


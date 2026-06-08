"""
FIFA World Cup 2026 — Prediction & Monte Carlo Simulation  v2
==============================================================
Architecture (updated per audit v2):

  Match History  50%
    Elo                  38%
    Form Goal Diff       24%
    Form Win Rate        20%
    Trophy Bonus          8%
    Manager Quality       5%
    Knockout Pedigree     5%

  Team Strength  50%
    Overall_Team_Strength 25%
    Top11_Avg             15%
    Squad_Strength        15%
    Attack_Rating         15%
    Defense_Rating        15%
    Midfield_Rating       10%
    Elite_Count            5%

Inflation fix:
  - Elo is tanh-normalised (soft cap) instead of raw z-score
    → prevents one team's outlier Elo from dominating
  - Logistic steepness reduced from k=7 to k=5
    → top team win% ~65-70% vs weakest, not 80%+
  - All sub-scores clipped to [-1, 1] before blending
  - Result: top team tournament win% lands in 14-18% range
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import warnings, os
warnings.filterwarnings("ignore")

# ── 0. PATHS ──────────────────────────────────────────────────────────────────
MATCHES_PATH = "/mnt/user-data/uploads/wc2026_matches_fixed.csv"
TEAMS_PATH   = "/mnt/user-data/uploads/wc2026_team_features_final.csv"
OUTPUT_PATH  = "/mnt/user-data/outputs/wc2026_simulation_results_v2.csv"

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────
matches_df = pd.read_csv(MATCHES_PATH)
teams_df   = pd.read_csv(TEAMS_PATH)

NAME_MAP = {
    "democratic republic of congo": "Democratic Republic of the Congo",
    "Curacao": "Curaçao",
}
matches_df["_home_team"] = matches_df["_home_team"].replace(NAME_MAP)
matches_df["_away_team"] = matches_df["_away_team"].replace(NAME_MAP)

# ── 2. WEIGHTS ────────────────────────────────────────────────────────────────
MATCH_WEIGHT  = 0.50
TEAM_WEIGHT   = 0.50

# ── 3. MANAGER QUALITY RATINGS ────────────────────────────────────────────────
# Scale: 0.0 (unknown/poor) → 2.0 (world-class proven)
# Normalised to 0–1 later by dividing by 2.0
MANAGER_RATINGS = {
    # Elite — proven at top level with major honours
    "Argentina":  2.0,   # Lionel Scaloni — WC 2022 winner, Copa America x2
    "France":     2.0,   # Didier Deschamps — WC 2018, Euro 2000 (as player, coach pedigree)
    "Spain":      1.8,   # Luis de la Fuente — Euro 2024 winner
    "Germany":    1.7,   # Julian Nagelsmann — Nations League 2025, rebuilding well
    "Portugal":   1.6,   # Roberto Martinez — solid record, Euro/WC experience
    "England":    1.5,   # Lee Carsley (interim) / Thomas Tuchel — UCL pedigree
    "Brazil":     1.5,   # Dorival Junior — improved Brazil post-Tite era
    "Croatia":    1.4,   # Zlatko Dalic — WC 2018 final, WC 2022 3rd place
    "Uruguay":    1.3,   # Marcelo Bielsa — high-intensity, proven tactician
    "Morocco":    1.3,   # Walid Regragui — WC 2022 semi-finalist
    "Netherlands":1.3,   # Ronald Koeman — experienced, steady
    "Belgium":    1.2,   # Domenico Tedesco — competent but unproven at WC level
    "Switzerland":1.2,   # Murat Yakin — consistent qualifier, disciplined
    "Japan":      1.2,   # Hajime Moriyasu — back-to-back WC R16, Asian Cup winner
    "Senegal":    1.2,   # Aliou Cisse — AFCON winner, WC QF 2002
    "Colombia":   1.2,   # Nestor Lorenzo — Copa America 2024 winner
    "Mexico":     1.1,   # Javier Aguirre — experienced, knows CONCACAF
    "South Korea":1.1,   # Hong Myung-bo — experienced Korean football figure
    "Austria":    1.1,   # Ralf Rangnick — high-press pioneer, strong UEFA record
    "Turkey":     1.1,   # Vincenzo Montella — Euro 2024 QF, steady tactician
    "Norway":     1.1,   # Stale Solbakken — consistent, but limited WC experience
    "Sweden":     1.0,   # Jon Dahl Tomasson — decent, mid-tier European coach
    "Algeria":    1.0,   # Vladimir Petkovic — experienced European coach
    "Ecuador":    1.0,   # Sebastian Beccacece — young, promising South American coach
    "Iran":       1.0,   # Amir Ghalenoei — solid AFC record
    "Australia":  1.0,   # Tony Popovic — new appointment, WC experience needed
    "Ivory Coast":1.0,   # Emerse Fae — young coach, promising AFCON run
    "Scotland":   0.9,   # Steve Clarke — consistent qualifier, limited WC pedigree
    "Canada":     0.9,   # Jesse Marsch — MLS/Bundesliga experience, improving
    "Czech Republic":0.9,# Ivan Hasek — solid UEFA coach
    "Egypt":      0.9,   # Hossam Hassan — AFCON experience, limited WC
    "Paraguay":   0.9,   # Daniel Garnero — competent South American coach
    "United States":0.9, # Mauricio Pochettino — UCL pedigree, adapting to USMNT
    "Ghana":      0.8,   # Otto Addo — local knowledge, limited top-level experience
    "Bosnia and Herzegovina": 0.8,
    "Tunisia":    0.8,
    "Saudi Arabia":0.8,
    "Qatar":      0.8,   # Marquez Lopez — limited WC experience
    "Cape Verde": 0.7,
    "Panama":     0.7,
    "South Africa":0.7,
    "Uzbekistan": 0.7,
    "New Zealand":0.7,
    "Democratic Republic of the Congo": 0.7,
    "Jordan":     0.6,
    "Iraq":       0.6,
    "Haiti":      0.6,
    "Curaçao":    0.5,
}

# Knockout pedigree — how often has this team reached WC knockouts historically
# Scale: 0.0 (never qualified / first timers) → 1.0 (multiple WC finals)
KNOCKOUT_PEDIGREE = {
    "Brazil":     1.0,   # 5x champion, always contend
    "Germany":    1.0,   # 4x champion, model of consistency
    "Argentina":  0.95,  # 3x champion, always deep runs
    "France":     0.90,  # 2x champion, regular finalists
    "Spain":      0.85,  # 1x champion, regular QF+
    "Italy":      0.85,  # (not in tournament but benchmark)
    "Uruguay":    0.75,  # 2x champion historically, regular knockouts
    "England":    0.70,  # 1x champion, regular R16+
    "Netherlands":0.70,  # 2x finalist, consistent
    "Portugal":   0.65,  # SF 2006, QF regular
    "Croatia":    0.65,  # Final 2018, 3rd 2022
    "Mexico":     0.60,  # Consistent R16, rarely beyond
    "Belgium":    0.55,  # QF 2018, improving record
    "Switzerland":0.50,  # R16 regular
    "Colombia":   0.50,  # QF 2014
    "Senegal":    0.45,  # QF 2002, R16 2022
    "Japan":      0.45,  # R16 x3
    "Morocco":    0.45,  # SF 2022
    "South Korea":0.45,  # SF 2002, R16 recent
    "United States":0.40,# QF 2002, regular R16
    "Australia":  0.35,  # QF 2006, R16 2022
    "Ecuador":    0.30,  # R16 2006
    "Turkey":     0.30,  # 3rd place 2002
    "Iran":       0.25,
    "Norway":     0.25,  # Last WC 1998, decent run
    "Sweden":     0.30,  # QF 2018
    "Austria":    0.25,
    "Algeria":    0.25,  # R16 2014
    "Ivory Coast":0.25,
    "Egypt":      0.20,
    "Ghana":      0.25,  # QF 2010
    "Canada":     0.15,  # WC 2022 first time back since 1986
    "Scotland":   0.15,
    "Czech Republic":0.20,
    "Paraguay":   0.25,  # QF 2010
    "Tunisia":    0.15,
    "Saudi Arabia":0.20, # R16 1994, beat Argentina 2022
    "Qatar":      0.10,  # Host only, Group exit
    "Bosnia and Herzegovina": 0.10,
    "Cape Verde": 0.05,
    "Panama":     0.10,
    "South Africa":0.15,
    "Uzbekistan": 0.05,
    "New Zealand":0.10,
    "Democratic Republic of the Congo": 0.10,
    "Jordan":     0.05,
    "Iraq":       0.10,
    "Haiti":      0.05,
    "Curaçao":    0.02,
}

# ── 4. MATCH-HISTORY STATS ────────────────────────────────────────────────────
def get_team_match_stats(team):
    home = matches_df[matches_df["_home_team"] == team]
    away = matches_df[matches_df["_away_team"] == team]

    elo_vals    = list(home["home_elo"])           + list(away["away_elo"])
    form_scored = list(home["home_form_scored"])   + list(away["away_form_scored"])
    form_conc   = list(home["home_form_conceded"]) + list(away["away_form_conceded"])
    form_wr     = list(home["home_form_win_rate"])  + list(away["away_form_win_rate"])
    trophy      = list(home["home_trophy_bonus"])   + list(away["away_trophy_bonus"])

    if not elo_vals:
        return None

    return {
        "elo":           np.mean(elo_vals[-10:]),
        "form_scored":   np.mean(form_scored[-5:]),
        "form_conceded": np.mean(form_conc[-5:]),
        "form_win_rate": np.mean(form_wr[-5:]),
        "trophy_bonus":  np.mean(trophy[-5:]) if trophy else 0.0,
    }

match_stats = {n: get_team_match_stats(n) for n in teams_df["Nation"]}
team_lookup  = teams_df.set_index("Nation").to_dict("index")

# Normalisation anchors
all_elo  = [s["elo"] for s in match_stats.values() if s]
ELO_MED  = np.median(all_elo)
ELO_STD  = np.std(all_elo)

# ── 5. COMPOSITE SCORE ────────────────────────────────────────────────────────
def compute_composite_score(team):
    ts = team_lookup.get(team)
    ms = match_stats.get(team)
    if ts is None:
        raise ValueError(f"Team not found: {team}")

    # ── TEAM STRENGTH (50%) ──────────────────────────────────────────────────
    # All z-scored or ratio-normalised inputs — clip to prevent outlier dominance
    overall_norm  = np.clip(ts["Overall_Team_Strength"]  * 0.25, -1, 1)
    top11_norm    = np.clip((ts["Top11_Avg"] - 80) / 10,  -1, 1)   # centre at 80, ±10
    squad_norm    = np.clip((ts["Squad_Strength"] - 78) / 8, -1, 1)
    attack_norm   = np.clip(ts["Attack_Rating_Norm"] * 0.35, -1, 1)
    defense_norm  = np.clip(ts["Defense_Rating_Norm"] * 0.35, -1, 1)
    mid_norm      = np.clip(ts["Midfield_Rating_Norm"] * 0.35, -1, 1)
    elite_norm    = np.clip(ts["Elite_Count"] / 15.0, 0, 1)

    strength_score = (
        0.25 * overall_norm  +
        0.15 * top11_norm    +
        0.15 * squad_norm    +
        0.15 * attack_norm   +
        0.15 * defense_norm  +
        0.10 * mid_norm      +
        0.05 * elite_norm
    )

    # ── MATCH HISTORY (50%) ──────────────────────────────────────────────────
    if ms:
        # tanh normalisation for Elo — soft cap prevents outlier inflation
        # tanh((x - median) / (1.5 * std)) maps most teams to [-0.7, 0.7]
        elo_norm  = np.tanh((ms["elo"] - ELO_MED) / (1.5 * ELO_STD))

        form_gd   = np.clip((ms["form_scored"] - ms["form_conceded"]) / 2.5, -1, 1)
        win_rate  = ms["form_win_rate"]              # already 0-1
        trophy    = np.clip(ms["trophy_bonus"], 0, 1)
        manager   = np.clip(MANAGER_RATINGS.get(team, 0.8) / 2.0, 0, 1)
        pedigree  = np.clip(KNOCKOUT_PEDIGREE.get(team, 0.2), 0, 1)

        match_score = (
            0.38 * elo_norm   +
            0.24 * form_gd    +
            0.20 * win_rate   +
            0.08 * trophy     +
            0.05 * manager    +
            0.05 * pedigree
        )
    else:
        match_score = strength_score

    return MATCH_WEIGHT * match_score + TEAM_WEIGHT * strength_score

composite_scores = {n: compute_composite_score(n) for n in teams_df["Nation"]}

# ── 6. MATCH PREDICTOR ────────────────────────────────────────────────────────
HOSTS_PRIMARY   = {"United States", "Mexico"}
HOSTS_SECONDARY = {"Canada"}
HOST_BOOST_PRIMARY   = 0.035
HOST_BOOST_SECONDARY = 0.015

def predict_match_probs(team1, team2):
    s1, s2 = composite_scores[team1], composite_scores[team2]
    diff = s1 - s2

    # k=5 → strong team wins ~70% vs weakest; much less steep than k=7-8
    # This is the key fix for preventing over-concentration of wins
    k = 5.0
    raw_win1 = 1 / (1 + np.exp(-k * diff))
    raw_win2 = 1 - raw_win1

    # Draw probability peaks at 27% for equal teams
    draw_base = 0.27 * np.exp(-5.0 * diff**2)

    p1   = raw_win1 * (1 - draw_base)
    draw = draw_base
    p2   = raw_win2 * (1 - draw_base)

    # Host boost
    if team1 in HOSTS_PRIMARY:
        p1 += HOST_BOOST_PRIMARY;   p2 -= HOST_BOOST_PRIMARY
    elif team1 in HOSTS_SECONDARY:
        p1 += HOST_BOOST_SECONDARY; p2 -= HOST_BOOST_SECONDARY
    elif team2 in HOSTS_PRIMARY:
        p2 += HOST_BOOST_PRIMARY;   p1 -= HOST_BOOST_PRIMARY
    elif team2 in HOSTS_SECONDARY:
        p2 += HOST_BOOST_SECONDARY; p1 -= HOST_BOOST_SECONDARY

    total = p1 + draw + p2
    return p1/total, draw/total, p2/total


def simulate_match(team1, team2, knockout=False):
    p1, draw, p2 = predict_match_probs(team1, team2)
    r = np.random.random()
    if r < p1:
        return team1
    elif r < p1 + draw:
        if knockout:
            edge = (p1 - p2) * 0.20   # small edge in pens
            return team1 if np.random.random() < 0.5 + edge else team2
        return "draw"
    else:
        return team2

# ── 7. GROUPS ─────────────────────────────────────────────────────────────────
GROUPS = {
    "A": ["Mexico",        "South Korea",   "Czech Republic",              "South Africa"],
    "B": ["Qatar",         "Canada",        "Bosnia and Herzegovina",      "Switzerland"],
    "C": ["Scotland",      "Brazil",        "Haiti",                       "Morocco"],
    "D": ["United States", "Turkey",        "Paraguay",                    "Australia"],
    "E": ["Ivory Coast",   "Germany",       "Curaçao",                     "Ecuador"],
    "F": ["Sweden",        "Netherlands",   "Japan",                       "Tunisia"],
    "G": ["Belgium",       "Iran",          "Egypt",                       "New Zealand"],
    "H": ["Uruguay",       "Spain",         "Saudi Arabia",                "Cape Verde"],
    "I": ["Senegal",       "France",        "Iraq",                        "Norway"],
    "J": ["Argentina",     "Jordan",        "Algeria",                     "Austria"],
    "K": ["Colombia",      "Uzbekistan",    "Democratic Republic of the Congo", "Portugal"],
    "L": ["England",       "Croatia",       "Panama",                      "Ghana"],
}

def simulate_group_stage():
    standings  = {}
    all_thirds = []

    for grp, teams in GROUPS.items():
        pts = defaultdict(int)
        gd  = defaultdict(int)
        gf  = defaultdict(int)

        for i in range(len(teams)):
            for j in range(i+1, len(teams)):
                t1, t2 = teams[i], teams[j]
                result = simulate_match(t1, t2, knockout=False)
                if result == t1:
                    pts[t1] += 3; gd[t1] += 1; gd[t2] -= 1; gf[t1] += 1
                elif result == t2:
                    pts[t2] += 3; gd[t2] += 1; gd[t1] -= 1; gf[t2] += 1
                else:
                    pts[t1] += 1; pts[t2] += 1

        sorted_teams = sorted(
            teams,
            key=lambda t: (pts[t], gd[t], gf[t], composite_scores[t]),
            reverse=True
        )
        standings[grp] = {"teams": sorted_teams, "pts": dict(pts), "gd": dict(gd)}
        all_thirds.append({
            "team":      sorted_teams[2],
            "pts":       pts[sorted_teams[2]],
            "gd":        gd[sorted_teams[2]],
            "composite": composite_scores[sorted_teams[2]],
        })

    all_thirds.sort(key=lambda x: (x["pts"], x["gd"], x["composite"]), reverse=True)
    best_thirds = [t["team"] for t in all_thirds[:8]]
    return standings, best_thirds


def get_qualifiers(standings, best_thirds):
    q = {}
    for grp, data in standings.items():
        q[f"{grp}1"] = data["teams"][0]
        q[f"{grp}2"] = data["teams"][1]
    for i, team in enumerate(best_thirds, 1):
        q[f"T{i}"] = team
    return q

# ── 8. KNOCKOUT BRACKET ───────────────────────────────────────────────────────
def build_r32_bracket(q):
    return [
        (q.get("A1"), q.get("B2")), (q.get("C1"), q.get("D2")),
        (q.get("E1"), q.get("F2")), (q.get("G1"), q.get("H2")),
        (q.get("I1"), q.get("J2")), (q.get("K1"), q.get("L2")),
        (q.get("B1"), q.get("A2")), (q.get("D1"), q.get("C2")),
        (q.get("F1"), q.get("E2")), (q.get("H1"), q.get("G2")),
        (q.get("J1"), q.get("I2")), (q.get("L1"), q.get("K2")),
        (q.get("T1"), q.get("T2")), (q.get("T3"), q.get("T4")),
        (q.get("T5"), q.get("T6")), (q.get("T7"), q.get("T8")),
    ]

def simulate_knockout_round(matchups):
    winners = []
    for t1, t2 in matchups:
        if t1 is None and t2 is None: continue
        if t1 is None: winners.append(t2); continue
        if t2 is None: winners.append(t1); continue
        winners.append(simulate_match(t1, t2, knockout=True))
    return winners

def pair_winners(winners):
    return [(winners[i], winners[i+1]) for i in range(0, len(winners)-1, 2)]

# ── 9. FULL TOURNAMENT ────────────────────────────────────────────────────────
STAGE_ORDER = {
    "Group Stage": 0, "Round of 32": 1, "Round of 16": 2,
    "Quarter-Final": 3, "Semi-Final": 4, "Runner-Up": 5, "Champion": 6,
}

def simulate_tournament():
    progress = {}
    standings, best_thirds = simulate_group_stage()
    qualifiers = get_qualifiers(standings, best_thirds)

    for grp, data in standings.items():
        for team in data["teams"][2:]:
            if team not in best_thirds:
                progress[team] = "Group Stage"
        progress[data["teams"][0]] = "Round of 32"
        progress[data["teams"][1]] = "Round of 32"
    for team in best_thirds:
        progress[team] = "Round of 32"

    r32  = build_r32_bracket(qualifiers)
    r32w = simulate_knockout_round(r32)
    for pair in r32:
        for t in pair:
            if t and t not in r32w: progress[t] = "Round of 32"
    for t in r32w: progress[t] = "Round of 16"

    r16w = simulate_knockout_round(pair_winners(r32w))
    for t in r32w:
        if t not in r16w: progress[t] = "Round of 16"
    for t in r16w: progress[t] = "Quarter-Final"

    qfw = simulate_knockout_round(pair_winners(r16w))
    for t in r16w:
        if t not in qfw: progress[t] = "Quarter-Final"
    for t in qfw: progress[t] = "Semi-Final"

    sfw = simulate_knockout_round(pair_winners(qfw))
    for t in qfw:
        if t not in sfw: progress[t] = "Semi-Final"
    for t in sfw: progress[t] = "Final"

    champion  = simulate_match(sfw[0], sfw[1], knockout=True)
    runner_up = sfw[1] if champion == sfw[0] else sfw[0]
    progress[runner_up] = "Runner-Up"
    progress[champion]  = "Champion"
    return champion, progress

# ── 10. MONTE CARLO ───────────────────────────────────────────────────────────
def run_simulations(n_sims=10000, seed=42):
    np.random.seed(seed)
    nations      = list(teams_df["Nation"])
    stage_counts = {s: defaultdict(int) for s in STAGE_ORDER}

    print(f"\n🌍 FIFA World Cup 2026 — Running {n_sims:,} simulations...")
    for sim in range(n_sims):
        if (sim+1) % 2000 == 0:
            print(f"   ✔  {sim+1:,} / {n_sims:,} completed")
        _, progress = simulate_tournament()
        for team, stage in progress.items():
            stage_counts[stage][team] += 1

    rows = []
    for nation in nations:
        champ    = stage_counts["Champion"].get(nation, 0)
        runnerup = stage_counts["Runner-Up"].get(nation, 0)
        sf       = stage_counts["Semi-Final"].get(nation, 0)
        qf       = stage_counts["Quarter-Final"].get(nation, 0)
        r16      = stage_counts["Round of 16"].get(nation, 0)
        r32      = stage_counts["Round of 32"].get(nation, 0)
        grp      = stage_counts["Group Stage"].get(nation, 0)

        rows.append({
            "Nation":          nation,
            "Composite_Score": round(composite_scores.get(nation, 0), 5),
            "Win_%":           round(champ / n_sims * 100, 2),
            "Final_%":         round((champ + runnerup) / n_sims * 100, 2),
            "Semi_Final_%":    round((champ + runnerup + sf) / n_sims * 100, 2),
            "Quarter_Final_%": round((champ + runnerup + sf + qf) / n_sims * 100, 2),
            "Round_of_16_%":   round((champ + runnerup + sf + qf + r16) / n_sims * 100, 2),
            "Round_of_32_%":   round((champ + runnerup + sf + qf + r16 + r32) / n_sims * 100, 2),
            "Group_Exit_%":    round(grp / n_sims * 100, 2),
        })

    df = (pd.DataFrame(rows)
            .sort_values("Win_%", ascending=False)
            .reset_index(drop=True))
    df.index += 1
    return df

# ── 11. RUN & SAVE ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    N_SIMS = 10000

    results = run_simulations(n_sims=N_SIMS, seed=42)

    print("\n" + "=" * 86)
    print(f"  FIFA WORLD CUP 2026 PREDICTIONS  ({N_SIMS:,} Monte Carlo simulations)  v2")
    print(f"  Match weight: {MATCH_WEIGHT*100:.0f}%  |  Team strength weight: {TEAM_WEIGHT*100:.0f}%")
    print("=" * 86)
    print(f"{'#':<4} {'Nation':<34} {'Win%':>6} {'Final%':>7} {'SF%':>6} {'QF%':>6} {'R16%':>6} {'R32%':>6}")
    print("-" * 86)
    for _, row in results.iterrows():
        print(
            f"{row.name:<4} {row['Nation']:<34} "
            f"{row['Win_%']:>6.2f} "
            f"{row['Final_%']:>7.2f} "
            f"{row['Semi_Final_%']:>6.2f} "
            f"{row['Quarter_Final_%']:>6.2f} "
            f"{row['Round_of_16_%']:>6.2f} "
            f"{row['Round_of_32_%']:>6.2f}"
        )

    print(f"\n📊 Sanity checks:")
    print(f"   Win% total   : {results['Win_%'].sum():.1f}%  (should be ~100%)")
    print(f"   Top favourite: {results.iloc[0]['Nation']}  ({results.iloc[0]['Win_%']:.2f}%)")
    print(f"   2nd favourite: {results.iloc[1]['Nation']}  ({results.iloc[1]['Win_%']:.2f}%)")
    print(f"   3rd favourite: {results.iloc[2]['Nation']}  ({results.iloc[2]['Win_%']:.2f}%)")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    results.to_csv(OUTPUT_PATH, index_label="Rank")
    print(f"\n✅  Results saved to: {OUTPUT_PATH}")

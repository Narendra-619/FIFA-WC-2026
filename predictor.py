import joblib
import pandas as pd
import numpy as np

# ── Load model artifacts ──────────────────────────────────────────
model= joblib.load("model/wc2026_final_model.pkl")

median_values= joblib.load("model/median_values.pkl")
final_team_features = pd.read_csv("data/final_team_features.csv")
feature_cols = model.feature_names_in_.tolist()
HOSTS = ["United States", "Mexico", "Canada"]
model = joblib.load("model/wc2026_final_model.pkl")


row = {
    
    "is_neutral": 1,
    "is_world_cup": 1,
    "is_continental": 0,

}

# ── Core fixture prediction ───────────────────────────────────────
def predict_fixture(team1, team2):

    h = final_team_features[final_team_features["Nation"] == team1].iloc[0]
    a = final_team_features[final_team_features["Nation"] == team2].iloc[0]

    row = {
        "home_elo":           h["Elo"],
        "away_elo":           a["Elo"],
        "elo_diff":           h["Elo"] - a["Elo"],
        "home_avg_overall":   h["avg_overall"],
        "away_avg_overall":   a["avg_overall"],
        "overall_diff":       h["avg_overall"] - a["avg_overall"],
        "home_max_overall":   h["max_overall"],
        "away_max_overall":   a["max_overall"],
        "home_avg_attack":    h["avg_attack"],
        "away_avg_attack":    a["avg_attack"],
        "attack_diff":        h["avg_attack"] - a["avg_attack"],
        "home_avg_defense":   h["avg_defense"],
        "away_avg_defense":   a["avg_defense"],
        "defense_diff":       h["avg_defense"] - a["avg_defense"],
        "home_avg_pace":      h["avg_pace"],
        "away_avg_pace":      a["avg_pace"],
        "home_avg_shooting":  h["avg_shooting"],
        "away_avg_shooting":  a["avg_shooting"],
        "home_avg_passing":   h["avg_passing"],
        "away_avg_passing":   a["avg_passing"],
        "home_form_scored":   h["Form_Scored"],
        "away_form_scored":   a["Form_Scored"],
        "home_form_conceded": h["Form_Conceded"],
        "away_form_conceded": a["Form_Conceded"],
        "home_form_win_rate": h["Form_Win_Rate"],
        "away_form_win_rate": a["Form_Win_Rate"],
        "home_trophy_bonus":  h["Trophy_Bonus"],
        "away_trophy_bonus":  a["Trophy_Bonus"],
        "is_world_cup":       1,        # ✅ in feature_cols
        "is_continental":     0,        # ✅ in feature_cols
        # "is_neutral" :1
    }

    X = pd.DataFrame([row])
    X = X.reindex(columns=feature_cols)
    X = X.fillna(median_values)

    return model.predict_proba(X)[0]


# ── Elo calibration ───────────────────────────────────────────────
def elo_calibrate(probs, elo1, elo2):

    p1, draw, p2 = probs
    diff = abs(elo1 - elo2)

    if diff < 200:
        return probs

    if elo1 > elo2:
        fav, dog  = p1, p2
        team1_fav = True
    else:
        fav, dog  = p2, p1
        team1_fav = False

    if diff >= 500:
        boost       = 0.15
        draw_weight = 0.80
    elif diff >= 450:
        boost       = 0.12
        draw_weight = 0.78
    elif diff >= 350:
        boost       = 0.08
        draw_weight = 0.75
    elif diff >= 250:
        boost       = 0.04
        draw_weight = 0.72
    else:
        boost       = 0
        draw_weight = 0

    fav  += boost
    draw -= boost * draw_weight
    dog  -= boost * (1 - draw_weight)

    total = fav + draw + dog
    fav  /= total
    draw /= total
    dog  /= total

    if team1_fav:
        return [fav, draw, dog]
    else:
        return [dog, draw, fav]


# ── Elite draw adjustment ─────────────────────────────────────────
def elite_draw_adjust(p1, draw, p2, elo1, elo2):

    avg_elo = (elo1 + elo2) / 2
    diff    = abs(elo1 - elo2)

    if avg_elo > 1900 and diff < 200:
        old_draw = draw
        draw    *= 0.90
        extra    = old_draw - draw
        p1 += extra / 2
        p2 += extra / 2

    return [p1, draw, p2]


# ── Neutral venue prediction ──────────────────────────────────────
def predict_neutral(team1, team2):

    p1 = predict_fixture(team1, team2)   # team1 as home
    p2 = predict_fixture(team2, team1)   # team2 as home

    # class 0 = away win, 1 = draw, 2 = home win
    team1_win = (p1[2] + p2[0]) / 2
    draw      = (p1[1] + p2[1]) / 2
    team2_win = (p1[0] + p2[2]) / 2

    probs = [team1_win, draw, team2_win]

    h = final_team_features[final_team_features["Nation"] == team1].iloc[0]
    a = final_team_features[final_team_features["Nation"] == team2].iloc[0]

    probs = elo_calibrate(probs, h["Elo"], a["Elo"])

    return probs


# ── World Cup prediction (with host boost) ────────────────────────
def predict_world_cup(team1, team2):

    p = predict_neutral(team1, team2)
    team1_win, draw, team2_win = p

    HOST_BOOST = 0.03

    if team1 in HOSTS:
        team1_win += HOST_BOOST
        team2_win -= HOST_BOOST
    elif team2 in HOSTS:
        team2_win += HOST_BOOST
        team1_win -= HOST_BOOST

    total = team1_win + draw + team2_win

    return [
        team1_win / total,
        draw      / total,
        team2_win / total,
    ]


# ── Public API ────────────────────────────────────────────────────
def predict_match(team1, team2):

    probs = predict_world_cup(team1, team2)

    return {
        team1:  float(round(probs[0] * 100, 2)),
        "Draw": float(round(probs[1] * 100, 2)),
        team2:  float(round(probs[2] * 100, 2)),
    }


# ── Entry point ───────────────────────────────────────────────────
if __name__ == "__main__":
    print(predict_neutral("Argentina", "New Zealand"))

    
    


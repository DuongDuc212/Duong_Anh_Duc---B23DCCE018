import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.ioff()

df = pd.read_csv('Bài 1/result.csv')

numeric_columns = [
    'age', 'matches_played', 'starts', 'minutes', 'goals', 'assists',
    'yellow_cards', 'red_cards', 'xG', 'xAG', 'PrgC', 'PrgP', 'PrgR',
    'per90_Gls', 'per90_Ast', 'per90_xG', 'per90_xAG', 'SoT%', 'SoT/90',
    'G/Sh', 'Dist', 'Pass_Cmp', 'Pass_Cmp%', 'TotDist', 'Short_Cmp%',
    'Medium_Cmp%', 'Long_Cmp%', 'KP', '1/3', 'PPA', 'CrsPA', 'SCA', 'SCA90',
    'GCA', 'GCA90', 'Tkl', 'TklW', 'Challenges_Att', 'Challenges_Lost',
    'Blocks', 'Blocks_SH', 'Blocks_Pass', 'Blocks_Int', 'Touches', 'Def_Pen',
    'Def_3rd', 'Mid_3rd', 'Att_3rd', 'Att_Pen', 'Take_Att', 'Take_Succ%',
    'Take_Tkld%', 'Carries', 'Carries_ProDist', 'Carries_ProgC', 'Carries_1/3',
    'Carries_CPA', 'Carries_Mis', 'Carries_Dis', 'REC', 'REC_PrgR', 'Fls',
    'Fld', 'Off', 'Crs', 'OG', 'Recov', 'Aerial_Won', 'Aerial_Lost', 'Aerial_Won%'
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

def find_extremes(df, columns, output_file='Bài 2/top_3.txt'):
    os.makedirs('Bài 2', exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for col in columns:
            if col not in df.columns or df[col].dropna().empty:
                f.write(f"\nStatistic: {col}\nNo valid data available\n")
                f.write("-" * 50 + "\n")
                continue
            top_players = df[['name', 'team', col]].dropna().sort_values(by=col, ascending=False).head(3)
            bottom_players = df[['name', 'team', col]].dropna().sort_values(by=col, ascending=True).head(3)
            f.write(f"\nStatistic: {col}\n")
            f.write("Top 3 Players:\n")
            for _, row in top_players.iterrows():
                f.write(f"{row['name']} ({row['team']}): {row[col]:.2f}\n")
            f.write("Bottom 3 Players:\n")
            for _, row in bottom_players.iterrows():
                f.write(f"{row['name']} ({row['team']}): {row[col]:.2f}\n")
            f.write("-" * 50 + "\n")

find_extremes(df, numeric_columns)

def calculate_stats(df, columns, output_file='Bài 2/results2.csv'):
    os.makedirs('Bài 2', exist_ok=True)
    teams = ['all (toàn bộ)'] + list(df['team'].unique())
    stats_data = {'Team': teams}
    for col in columns:
        if col not in df.columns or df[col].dropna().empty:
            continue
        stats_data[f'Trung vị của {col}'] = []
        stats_data[f'Trung bình của {col}'] = []
        stats_data[f'Độ lệch chuẩn của {col}'] = []
        median = df[col].median()
        mean = df[col].mean()
        std = df[col].std()
        stats_data[f'Trung vị của {col}'].append(median)
        stats_data[f'Trung bình của {col}'].append(mean)
        stats_data[f'Độ lệch chuẩn của {col}'].append(std)
        for team in teams[1:]:
            team_df = df[df['team'] == team]
            median = team_df[col].median()
            mean = team_df[col].mean()
            std = team_df[col].std()
            stats_data[f'Trung vị của {col}'].append(median)
            stats_data[f'Trung bình của {col}'].append(mean)
            stats_data[f'Độ lệch chuẩn của {col}'].append(std)
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(output_file, index=False, encoding='utf-8')

calculate_stats(df, numeric_columns)

def create_histograms(df, columns, teams):
    os.makedirs('Bài 2/histograms', exist_ok=True)
    for col in columns:
        if col not in df.columns or df[col].dropna().size < 3 or df[col].dropna().max() == df[col].dropna().min():
            continue
        plt.figure(figsize=(10, 6))
        n_bins = min(30, max(5, int(df[col].dropna().size / 5)))
        plt.hist(df[col].dropna(), bins=n_bins, density=True, histtype='bar', align='mid', orientation='vertical', rwidth=0.8, color='blue', alpha=0.7)
        plt.title(f'Distribution of {col} - All Players')
        plt.xlabel(col)
        plt.ylabel('Density')
        plt.grid(True, alpha=0.3)
        safe_col = col.replace('/', '_').replace('%', 'pct').replace('\\', '_')
        plt.savefig(f'Bài 2/histograms/league_{safe_col}.png')
        plt.close()
    for team in teams:
        team_df = df[df['team'] == team]
        safe_team = ''.join(c if c.isalnum() else '_' for c in team)
        for col in columns:
            if col not in df.columns or team_df[col].dropna().size < 3 or team_df[col].dropna().max() == team_df[col].dropna().min():
                continue
            plt.figure(figsize=(10, 6))
            n_bins = min(20, max(3, int(team_df[col].dropna().size / 3)))
            plt.hist(team_df[col].dropna(), bins=n_bins, density=True, histtype='bar', align='mid', orientation='vertical', rwidth=0.8, color='green', alpha=0.7)
            plt.title(f'Distribution of {col} - {team}')
            plt.xlabel(col)
            plt.ylabel('Density')
            plt.grid(True, alpha=0.3)
            safe_col = col.replace('/', '_').replace('%', 'pct').replace('\\', '_')
            plt.savefig(f'Bài 2/histograms/{safe_team}_{safe_col}.png')
            plt.close()

teams = df['team'].unique()
create_histograms(df, numeric_columns, teams)

def find_top_teams(df, columns):
    team_stats = []
    for col in columns:
        if col not in df.columns or df[col].dropna().empty:
            continue
        team_means = df.groupby('team')[col].mean()
        if team_means.empty or team_means.isna().all():
            continue
        top_team = team_means.idxmax()
        top_value = team_means.max()
        if pd.isna(top_team) or pd.isna(top_value):
            continue
        team_stats.append({
            'Statistic': col,
            'Top Team': top_team,
            'Average Value': top_value
        })
    return pd.DataFrame(team_stats)

top_teams_df = find_top_teams(df, numeric_columns)

def analyze_team_performance(top_teams_df):
    os.makedirs('Bài 2', exist_ok=True)
    output_file = 'Bài 2/team_performance.txt'
    if top_teams_df.empty:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("No team performance data available.")
        return
    team_counts = top_teams_df['Top Team'].value_counts()
    best_team = team_counts.index[0]
    best_team_count = team_counts.iloc[0]
    analysis = (
        f"Dựa trên phân tích, {best_team} dường như đang thi đấu tốt nhất trong mùa giải Ngoại hạng Anh 2024-2025.\n"
        f"Họ dẫn đầu ở {best_team_count} trên tổng số {len(top_teams_df)} hạng mục thống kê.\n"
        "Điều này cho thấy một màn trình diễn mạnh mẽ trên nhiều phương diện của trận đấu, bao gồm hiệu suất tấn công, "
        "khả năng triển khai bóng lên phía trước, và sự tham gia tổng thể vào các trận đấu."
    )
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Top Teams for Each Statistic:\n")
        for _, row in top_teams_df.iterrows():
            f.write(f"{row['Statistic']}: {row['Top Team']} (Avg: {row['Average Value']:.2f})\n")
        f.write("\nPerformance Analysis:\n")
        f.write(analysis)

analyze_team_performance(top_teams_df)
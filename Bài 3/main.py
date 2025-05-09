import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import seaborn as sns

plt.ioff()

df = pd.read_csv('Bài 1/result.csv')

numeric_columns = [
    'age', 'matches_played', 'starts', 'minutes', 'goals', 'assists',
    'yellow_cards', 'red_cards', 'xG', 'xAG', 'PrgC', 'PrgP', 'PrgR',
    'per90_Gls', 'per90_Ast', 'per90_xG', 'per90_xAG',
    'SoT%', 'SoT/90', 'G/Sh', 'Dist',
    'Pass_Cmp', 'Pass_Cmp%', 'TotDist',
    'Short_Cmp%', 'Medium_Cmp%', 'Long_Cmp%', 
    'KP', '1/3', 'PPA', 'CrsPA', 'PrgP',
    'Tkl', 'TklW', 'Challenges_Att', 'Challenges_Lost',
    'Blocks', 'Blocks_SH', 'Blocks_Pass', 'Blocks_Int',
    'Touches', 'Def_Pen', 'Def_3rd', 'Mid_3rd', 'Att_3rd', 'Att_Pen',
    'Take_Att', 'Take_Succ%', 'Take_Tkld%',
    'Carries', 'Carries_ProDist', 'Carries_ProgC', 'Carries_1/3', 'Carries_CPA', 'Carries_Mis', 'Carries_Dis',
    'REC', 'REC_PrgR',
    'Fls', 'Fld', 'Off', 'Crs', 'OG', 'Recov', 'Aerial_Won', 'Aerial_Lost', 'Aerial_Won%'
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

data_for_clustering = df[numeric_columns].dropna()

scaler = StandardScaler()
scaled_data = scaler.fit_transform(data_for_clustering)

inertia = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 6))
plt.plot(k_range, inertia, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.grid(True)
plt.savefig('Bài 3/elbow_plot.png')
plt.close()

optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

df_clusters = df.loc[data_for_clustering.index].copy()
df_clusters['Cluster'] = clusters

cluster_summary = df_clusters.groupby('Cluster')[numeric_columns].mean()
cluster_summary.to_csv('Bài 3/cluster_summary.csv', encoding='utf-8-sig')

pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

explained_variance = pca.explained_variance_ratio_.sum() * 100

plt.figure(figsize=(10, 8))
sns.scatterplot(x=pca_data[:, 0], y=pca_data[:, 1], hue=clusters, palette='tab10', s=100)
plt.title(f'2D PCA of Player Clusters (Explained Variance: {explained_variance:.2f}%)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.grid(True)
plt.savefig('Bài 3/pca_clusters.png')
plt.close()



def find_top_teams(df, columns):
    team_stats = []
    for col in columns:
        team_means = df.groupby('team')[col].mean().sort_values(ascending=False)
        top_team = team_means.index[0]
        top_value = team_means.iloc[0]
        team_stats.append({
            'Statistic': col,
            'Top Team': top_team,
            'Average Value': top_value
        })
    
    team_stats_df = pd.DataFrame(team_stats)
    return team_stats_df

top_teams_df = find_top_teams(df, numeric_columns)

def analyze_team_performance(top_teams_df):
    team_counts = top_teams_df['Top Team'].value_counts()
    best_team = team_counts.index[0]
    best_team_count = team_counts.iloc[0]
    
    analysis = (
        f"Based on the analysis, {best_team} appears to be performing the best in the 2024-2025 Premier League season.\n"
        f"They lead in {best_team_count} out of {len(numeric_columns)} statistical categories.\n"
        "This suggests strong performance across multiple aspects of the game, including offensive output, "
        "progressive play, and overall involvement in matches."
    )
    
    with open('team_performance.txt', 'w', encoding='utf-8-sig') as f:
        f.write("Top Teams for Each Statistic:\n")
        for _, row in top_teams_df.iterrows():
            f.write(f"{row['Statistic']}: {row['Top Team']} (Avg: {row['Average Value']:.2f})\n")
        f.write("\nPerformance Analysis:\n")
        f.write(analysis)

analyze_team_performance(top_teams_df)
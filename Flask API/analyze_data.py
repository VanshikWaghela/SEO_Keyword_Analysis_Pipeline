import pandas as pd
import matplotlib.pyplot as plt

# Data: Copy the dataset here
data = [['26aa60ed-7cb7-454f-b71d-7403c39cf5c2', 'Keyword_29', 'Finance', 'South America', 'Spanish', 'Navigational', 5335, 2.32, 0.0214, 53350, 1141, 0.096, 0.299, 96, 'Medium', 15, 782, 840, 394, 132, 477, 892, 570, 856, 546, 854, 935, 398], ['1cfb5ea3-79ad-49e2-ae64-edbc80f88048', 'Keyword_47', 'Finance', 'Australia', 'English', 'Navigational', 4481, 8.17, 0.0145, 44810, 649, 0.0448, 0.639, 25, 'Medium', 16, 719, 803, 406, 86, 449, 882, 577, 876, 490, 893, 958, 388], ['b5c420eb-4da5-4da2-8533-433751b85f7d', 'Keyword_78', 'Finance', 'South America', 'French', 'Transactional', 2156, 5.39, 0.051, 21560, 1099, 0.112, 0.4653, 3, 'Low', 15, 802, 843, 390, 110, 430, 861, 536, 825, 522, 838, 922, 458], ['16e7140e-cc36-4aec-b7cc-c219ef387fda', 'Keyword_87', 'Finance', 'Europe', 'English', 'Informational', 3927, 2.02, 0.1557, 39270, 6114, 0.0736, 0.8214, 78, 'High', 2, 794, 814, 415, 109, 423, 837, 556, 813, 527, 893, 875, 426], ['8375840b-3e68-4c81-92ca-85d225352348', 'Keyword_55', 'Finance', 'Europe', 'Spanish', 'Informational', 1383, 4.65, 0.0334, 13830, 461, 0.2384, 0.7686, 96, 'Low', 13, 714, 859, 399, 97, 412, 865, 529, 844, 500, 924, 935, 429], ['8f21bcaf-b1f8-430b-8b79-52c8403be080', 'Keyword_9', 'Finance', 'Australia', 'Chinese', 'Transactional', 4449, 2.85, 0.0336, 44490, 1494, 0.297, 0.2985, 94, 'Medium', 13, 756, 799, 376, 124, 429, 901, 572, 868, 485, 887, 921, 389], ['1db8753e-08f6-40e5-9f7a-701884d1eee8', 'Keyword_93', 'Finance', 'Australia', 'French', 'Navigational', 4803, 5.66, 0.1878, 48030, 9020, 0.0396, 0.4951, 3, 'Medium', 5, 725, 825, 437, 107, 474, 876, 554, 798, 513, 878, 898, 414], ['e6fa2a9d-0e2b-4a33-bed2-e460583ef044', 'Keyword_62', 'Finance', 'Europe', 'Spanish', 'Transactional', 7714, 3.31, 0.0545, 77140, 4204, 0.2444, 0.3263, 38, 'Medium', 4, 799, 871, 436, 79, 427, 829, 569, 842, 518, 917, 871, 374], ['357ac4e2-348c-42ac-afd8-eadf13f7ba84', 'Keyword_96', 'Finance', 'Europe', 'English', 'Navigational', 5060, 9.15, 0.1209, 50600, 6117, 0.0957, 0.2971, 60, 'Low', 12, 756, 818, 429, 96, 454, 904, 566, 832, 488, 902, 878, 374], ['fe8aee21-2cfc-4143-bcd4-e9def523ef76', 'Keyword_18', 'Finance', 'Australia', 'German', 'Navigational', 3037, 4.96, 0.016, 30370, 485, 0.2733, 0.2211, 9, 'Low', 13, 746, 827, 393, 172, 485, 886, 543, 875, 521, 910, 941, 384]]


# Columns
columns = [
    "Keyword ID", "Keyword Name", "Category", "Region", "Language", "Search Intent",
    "Search Volume", "CPC (Cost Per Click)", "CTR (Click-Through Rate)", "Impressions",
    "Clicks", "Conversion Rate", "Bounce Rate", "Keyword Difficulty", "Competition Level",
    "Competitor Rank", "Jan 2023", "Feb 2023", "Mar 2023", "Apr 2023", "May 2023",
    "Jun 2023", "Jul 2023", "Aug 2023", "Sep 2023", "Oct 2023", "Nov 2023", "Dec 2023"
]

# Create a DataFrame
df = pd.DataFrame(data, columns=columns)

# 1. Keyword Difficulty Distribution
plt.figure(figsize=(8, 5))
df["Keyword Difficulty"].value_counts().sort_index().plot(kind="bar", color="skyblue")
plt.title("Keyword Difficulty Distribution")
plt.xlabel("Difficulty")
plt.ylabel("Count")
plt.savefig("keyword_difficulty_distribution.png")
plt.close()

# 2. CPC vs Search Volume Scatter Plot
plt.figure(figsize=(8, 5))
plt.scatter(df["Search Volume"], df["CPC (Cost Per Click)"], color="red")
plt.title("CPC vs Search Volume")
plt.xlabel("Search Volume")
plt.ylabel("CPC (Cost Per Click)")
plt.savefig("cpc_vs_search_volume.png")
plt.close()

# 3. Monthly Trends Analysis (Example for "Clicks")
monthly_columns = [
    "Jan 2023", "Feb 2023", "Mar 2023", "Apr 2023", "May 2023", "Jun 2023",
    "Jul 2023", "Aug 2023", "Sep 2023", "Oct 2023", "Nov 2023", "Dec 2023"
]
df_monthly = df[monthly_columns].sum()

plt.figure(figsize=(10, 6))
df_monthly.plot(kind="line", marker="o", color="green")
plt.title("Monthly Click Trends (2023)")
plt.xlabel("Months")
plt.ylabel("Total Clicks")
plt.savefig("monthly_click_trends.png")
plt.close()

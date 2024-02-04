import pandas as pd
import glob

data_path = r"C:\Users\dongh\OneDrive\Desktop\workspace\SMTM\ShowMeTheMoney\toto\data"

# Get a list of CSV files in the specified data path
csv_files = glob.glob(f'{data_path}\*.csv')

# Column names
columns = ['round_number', 'sport_tag', 'league', 'home_team', 'home_score', 'odds[0]', 'away_team', 'away_score', 'odds[1]', 'month', 'day']

# Initialize an empty list to store DataFrames
dfs = [pd.read_csv(file, header=None, names=columns) for file in csv_files]

# Check if there are any DataFrames in the list
if dfs:
    # Concatenate the list of DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)

    # Filter DataFrame based on odds range [1.0, 1.3) for both odds[0] and odds[1]
    filtered_df = combined_df[
        ((combined_df['odds[0]'] >= 1.0) & (combined_df['odds[0]'] < 1.3)) |
        ((combined_df['odds[1]'] >= 1.0) & (combined_df['odds[1]'] < 1.3))
    ]

    # Function to determine win/loss based on odds[0] and odds[1]
    def determine_outcome(row):
        if row['home_score'] > row['away_score']:
            return 'home_win'
        elif row['home_score'] < row['away_score']:
            return 'away_win'
        else:
            return 'draw'

    # Apply the function to create a new 'outcome' column
    filtered_df['outcome'] = filtered_df.apply(determine_outcome, axis=1)

    # Calculate the rate of 'home_win' and 'away_win'
    home_win_rate = filtered_df['outcome'].value_counts(normalize=True).get('home_win', 0) * 100
    away_win_rate = filtered_df['outcome'].value_counts(normalize=True).get('away_win', 0) * 100

    # Display the DataFrame with the new 'outcome' column
    print(filtered_df[['home_team', 'away_team', 'home_score', 'away_score', 'odds[0]', 'odds[1]', 'outcome']])

    # Display the calculated rates
    print(f"Rate of Home Win: {home_win_rate:.2f}%")
    print(f"Rate of Away Win: {away_win_rate:.2f}%")

    # Define the output Excel file path
    output_excel_path = f'{data_path}\\sorted_analysis.xlsx'

    # Save the displayed DataFrame to the specified Excel file
    filtered_df[['home_team', 'away_team', 'home_score', 'away_score', 'odds[0]', 'odds[1]', 'outcome']].to_excel(output_excel_path, index=False)
else:
    print("No CSV files found.")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from controllers.BaseController import BaseController;
import joblib
# Load the dataset
# file_path = 'D:\Ghazanfar\FlaskScraper\EliveScrapers\\assets\match_data.csv'
# data = pd.read_csv(file_path)

# # Convert date column to datetime format
# data['date'] = pd.to_datetime(data['date'])

# # Filter data to include matches from 2010 to 2022
# data = data[(data['date'].dt.year >= 2010) & (data['date'].dt.year <= 2022)]

# # Clean the data by removing rows with missing values in key columns
# data = data.dropna(subset=['home_team_name', 'away_team_name', 'venue_name', 'fulltime_home_goals', 'fulltime_away_goals'])

# # Create a new column for match result based on fulltime goals
# def get_match_result(row):
#     if row['fulltime_home_goals'] > row['fulltime_away_goals']:
#         return 'Home Win'
#     elif row['fulltime_home_goals'] < row['fulltime_away_goals']:
#         return 'Away Win'
#     else:
#         return 'Draw'

# data['match_result'] = data.apply(get_match_result, axis=1)

# # Define all potential teams and venues
# all_teams = pd.concat([data['home_team_name'], data['away_team_name']]).unique().tolist()
# all_teams.extend(['Manchester United', 'Chelsea'])  # Add any potential new teams

# all_venues = data['venue_name'].unique().tolist()
# all_venues.extend(['Old Trafford'])  # Add any potential new venues

# # Ensure the label encoder includes all potential labels
# label_encoder_teams = LabelEncoder()
# label_encoder_teams.fit(all_teams)

# label_encoder_venues = LabelEncoder()
# label_encoder_venues.fit(all_venues)

# data['home_team_encoded'] = label_encoder_teams.transform(data['home_team_name'])
# data['away_team_encoded'] = label_encoder_teams.transform(data['away_team_name'])
# data['venue_encoded'] = label_encoder_venues.transform(data['venue_name'])

# # Calculate team form and head-to-head statistics
# def calculate_team_form(data, team, n_matches=5):
#     form_stats = {'wins': 0, 'losses': 0, 'draws': 0, 'goals_scored': 0, 'goals_conceded': 0}
#     team_matches = data[(data['home_team_name'] == team) | (data['away_team_name'] == team)].tail(n_matches)
    
#     for _, row in team_matches.iterrows():
#         if row['home_team_name'] == team:
#             form_stats['goals_scored'] += row['fulltime_home_goals']
#             form_stats['goals_conceded'] += row['fulltime_away_goals']
#             if row['match_result'] == 'Home Win':
#                 form_stats['wins'] += 1
#             elif row['match_result'] == 'Away Win':
#                 form_stats['losses'] += 1
#             else:
#                 form_stats['draws'] += 1
#         elif row['away_team_name'] == team:
#             form_stats['goals_scored'] += row['fulltime_away_goals']
#             form_stats['goals_conceded'] += row['fulltime_home_goals']
#             if row['match_result'] == 'Away Win':
#                 form_stats['wins'] += 1
#             elif row['match_result'] == 'Home Win':
#                 form_stats['losses'] += 1
#             else:
#                 form_stats['draws'] += 1
#     return form_stats

# # Add form and head-to-head statistics to the dataset
# data['home_team_recent_wins'] = 0
# data['home_team_recent_losses'] = 0
# data['home_team_recent_draws'] = 0
# data['home_team_recent_goals_scored'] = 0
# data['home_team_recent_goals_conceded'] = 0
# data['away_team_recent_wins'] = 0
# data['away_team_recent_losses'] = 0
# data['away_team_recent_draws'] = 0
# data['away_team_recent_goals_scored'] = 0
# data['away_team_recent_goals_conceded'] = 0

# for index, row in data.iterrows():
#     if index > 0:
#         home_team_form = calculate_team_form(data[:index], row['home_team_name'])
#         away_team_form = calculate_team_form(data[:index], row['away_team_name'])
#         data.at[index, 'home_team_recent_wins'] = home_team_form['wins']
#         data.at[index, 'home_team_recent_losses'] = home_team_form['losses']
#         data.at[index, 'home_team_recent_draws'] = home_team_form['draws']
#         data.at[index, 'home_team_recent_goals_scored'] = home_team_form['goals_scored']
#         data.at[index, 'home_team_recent_goals_conceded'] = home_team_form['goals_conceded']
#         data.at[index, 'away_team_recent_wins'] = away_team_form['wins']
#         data.at[index, 'away_team_recent_losses'] = away_team_form['losses']
#         data.at[index, 'away_team_recent_draws'] = away_team_form['draws']
#         data.at[index, 'away_team_recent_goals_scored'] = away_team_form['goals_scored']
#         data.at[index, 'away_team_recent_goals_conceded'] = away_team_form['goals_conceded']

# # Select features for model training
# features = ['home_team_encoded', 'away_team_encoded', 'venue_encoded',
#             'home_team_recent_wins', 'home_team_recent_losses', 'home_team_recent_draws',
#             'home_team_recent_goals_scored', 'home_team_recent_goals_conceded',
#             'away_team_recent_wins', 'away_team_recent_losses', 'away_team_recent_draws',
#             'away_team_recent_goals_scored', 'away_team_recent_goals_conceded']
# X = data[features]
# y = data['match_result']

# # Manual oversampling of minority classes
# class_counts = y.value_counts()
# max_count = class_counts.max()

# data_oversampled = pd.DataFrame()
# for class_label, count in class_counts.items():
#     class_data = data[y == class_label]
#     if count < max_count:
#         class_data = class_data.sample(max_count, replace=True)
#     data_oversampled = pd.concat([data_oversampled, class_data])

# X = data_oversampled[features]
# y = data_oversampled['match_result']

# # Split the resampled data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Hyperparameter tuning using Grid Search for RandomForestClassifier
# param_grid = {
#     'n_estimators': [100, 200, 300],
#     'max_depth': [None, 10, 20, 30],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4]
# }

# rf_model = RandomForestClassifier(random_state=42)
# grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
# grid_search.fit(X_train, y_train)

# # Best model from Grid Search
# best_rf_model = grid_search.best_estimator_

# # Make predictions
# y_pred = best_rf_model.predict(X_test)

# # Evaluate the model
# classification_report_str = classification_report(y_test, y_pred)
# conf_matrix = confusion_matrix(y_test, y_pred, labels=best_rf_model.classes_)

# # Plot the confusion matrix
# disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=best_rf_model.classes_)
# disp.plot(cmap=plt.cm.Blues)
# plt.title('Confusion Matrix')
# plt.show()

# # Calculate and print the accuracy
# accuracy = accuracy_score(y_test, y_pred)
# print(f'Accuracy: {accuracy * 100:.2f}%')

# print("Best Parameters: ", grid_search.best_params_)
# print(classification_report_str)

# Sample prediction
def sample_prediction(home_team, away_team, venue, model, label_encoder_teams, label_encoder_venues):
        home_team_encoded = label_encoder_teams.transform([home_team])[0]
        away_team_encoded = label_encoder_teams.transform([away_team])[0]
        venue_encoded = label_encoder_venues.transform([venue])[0]

        # Create a DataFrame for the sample match
        sample_data = pd.DataFrame({
            'home_team_encoded': [home_team_encoded],
            'away_team_encoded': [away_team_encoded],
            'venue_encoded': [venue_encoded],
            'home_team_recent_wins': [0],  # These would be calculated based on recent matches
            'home_team_recent_losses': [0],
            'home_team_recent_draws': [0],
            'home_team_recent_goals_scored': [0],
            'home_team_recent_goals_conceded': [0],
            'away_team_recent_wins': [0],
            'away_team_recent_losses': [0],
            'away_team_recent_draws': [0],
            'away_team_recent_goals_scored': [0],
            'away_team_recent_goals_conceded': [0]
        })

        # Predict the result
        prediction = model.predict(sample_data)
        return prediction[0]
class Prediction(BaseController):
    def __init__(self):
        self.headers = {}
        self.best_rf_model = joblib.load('assets/best_rf_model.pkl')
        self.label_encoder_teams = joblib.load('assets/label_encoder_teams.pkl')
        self.label_encoder_venues = joblib.load('assets/label_encoder_venues.pkl')


    def prediction(self,homeTeam,awayTeam,venu):
        sample_result = sample_prediction(homeTeam, awayTeam, venu, self.best_rf_model, self.label_encoder_teams, self.label_encoder_venues)
   
        return self.sendResponse("Prediction Result",{
            'result':sample_result
        })

# Example: Predicting a match between Manchester United and Chelsea at Old Trafford
# sample_result = sample_prediction('Manchester United', 'Chelsea', 'Old Trafford', best_rf_model, label_encoder_teams, label_encoder_venues)
# print(f'Sample Prediction: Manchester United vs Chelsea at Old Trafford -> {sample_result}')

from flask import Flask, jsonify,render_template
import requests

app = Flask(__name__)

@app.route('/')

def index():
        return render_template('index.html')


@app.route('/live-matches', methods=['GET'])
def live_matches():
    url = "https://livescore-api.com/api-client/matches/live.json"
    api_key = 'qGp7ISNPnu1IscVQ'
    api_secret = 'IS3lCnNPulRZbxXCemKXexNC2Okv1fmK'
    
    params = {
        'key': api_key,
        'secret': api_secret,
        'lang': 'en',
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        organized_matches = []
        top_priority_matches = []

        for match in data['data']['match']:
            try:
                home_team = match['home']['name']
                away_team = match['away']['name']
                country = match['country']['name']
                league = match['competition']['name']
                score = match['scores']['score']
                score_parts = score.split(' - ')
                total_score = int(score_parts[0]) + int(score_parts[1])
                minutes_played = match['time']
                minutes_int = int(minutes_played if minutes_played != 'FT' else '100')
                half = '1st Half' if minutes_int < 45 else '2nd Half'

                match_info = {
                    'country': country,
                    'league': league,
                    'home_team': home_team,
                    'away_team': away_team,
                    'score': score,
                    'minutes_played': minutes_played,
                    'half': half
                }

                if total_score >= 2 and minutes_int <= 15:
                    top_priority_matches.append(match_info)
                else:
                    organized_matches.append(match_info)

            except Exception as e:
                print(f"Error processing match: {e}")

        # Combine top priority and regular matches
        organized_matches = top_priority_matches + organized_matches
        
        return jsonify(organized_matches), 200
        
    else:
        return jsonify({"error": f"Error: {response.status_code} - {response.text}"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

import random

class Player:
    def __init__(self, name, bowling, batting, fielding, running, experience):
        self.name = name
        self.bowling = bowling
        self.batting = batting
        self.fielding = fielding
        self.running = running
        self.experience = experience

    def bowl(self):
        # Implement the logic for bowling
        return random.uniform(0, 1) <= self.bowling

    def bat(self, bowled):
        # Implement the logic for batting
        if bowled:
            return random.uniform(0, 1) <= self.batting
        else:
            return random.uniform(0, 1) <= self.batting * self.experience

    def field(self):
        # Implement the logic for fielding
        return random.uniform(0, 1) <= self.fielding

    def run(self, decision):
        # Implement the logic for running between the wickets
        if decision == 'out':
            return
        if decision == 'no_run':
            return
        if decision == 'one_run':
            return random.uniform(0, 1) <= self.running
        if decision == 'two_runs':
            return random.uniform(0, 1) <= self.running * self.experience
        if decision == 'three_runs':
            return random.uniform(0, 1) <= self.running * self.experience
        if decision == 'four_runs':
            return random.uniform(0, 1) <= self.running * self.experience
        if decision == 'six_runs':
            return random.uniform(0, 1) <= self.running * self.experience


class Teams:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.captain = None
        self.batting_order = []

    def add_player(self, player):
        self.players.append(player)

    def select_captain(self):
        self.captain = random.choice(self.players)

    def choose_batsmen(self):
        # Implement the logic to choose batsmen based on their batting skills
        self.batting_order = sorted(self.players, key=lambda player: player.batting, reverse=True)

    def choose_bowler(self):
        # Implement the logic to choose a bowler based on their bowling skills
        return random.choice(self.players)


class Field:
    def __init__(self, size, fan_ratio, pitch_conditions, home_advantage):
        self.size = size
        self.fan_ratio = fan_ratio
        self.pitch_conditions = pitch_conditions
        self.home_advantage = home_advantage

    def calculate_boundary_probability(self):
        # Implement the logic to calculate the probability of hitting a boundary based on field size and pitch conditions
        boundary_prob = 0.5  # Example implementation
        return boundary_prob


class Umpire:
    def __init__(self):
        self.scores = 0
        self.wickets = 0
        self.overs = 0

    def predict_outcome(self, bowler, batsman):
        # Implement the logic to predict the outcome of a ball based on bowler and batsman stats
        boundary_prob = field.calculate_boundary_probability()
        if bowler.bowl():
            if batsman.bat(True):
                if random.uniform(0, 1) <= boundary_prob:
                    return 'six_runs'
                else:
                    return 'no_run'
            else:
                return 'out'
        else:
            if batsman.bat(False):
                return random.choice(['one_run', 'two_runs', 'three_runs', 'four_runs'])
            else:
                return 'no_run'

    def make_decision(self, outcome):
        # Implement the logic to make decisions on LBWs, catches, no-balls, wide-balls, etc. based on the outcome
        # Example implementation:
        if outcome == 'out':
            self.wickets += 1
        elif outcome == 'no_run':
            self.scores += 0
        else:
            runs = int(outcome.split('_')[0])
            self.scores += runs

    def is_wicket_lost(self):
        return self.wickets >= 10

    def is_match_ended(self):
        return self.overs == 50 or self.is_wicket_lost()


class Commentator:
    def __init__(self):
        pass

    def provide_commentary(self, ball, bowler, batsman, outcome):
        # Implement the logic to provide commentary for each ball and over
        print(f"{batsman.name} faces {bowler.name}.")
        if outcome == 'out':
            print(f"{batsman.name} is OUT!")
        elif outcome == 'no_run':
            print(f"No run scored.")
        else:
            runs = int(outcome.split('_')[0])
            print(f"{runs} run{'s' if runs > 1 else ''} scored.")


class Match:
    def __init__(self, team1, team2, field):
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.current_batting_team = None
        self.current_bowling_team = None
        self.current_batsman = None
        self.current_bowler = None
        self.umpire = None
        self.commentator = None

    def start_match(self):
        self.team1.select_captain()
        self.team2.select_captain()
        self.team1.choose_batsmen()
        self.team2.choose_batsmen()
        self.current_batting_team = self.team1
        self.current_bowling_team = self.team2
        self.current_batsman = self.current_batting_team.batting_order[0]
        self.current_bowler = self.current_bowling_team.choose_bowler()
        self.umpire = Umpire()
        self.commentator = Commentator()

    def change_innings(self):
        self.current_batting_team, self.current_bowling_team = self.current_bowling_team, self.current_batting_team
        self.current_batsman = self.current_batting_team.batting_order[0]
        self.current_bowler = self.current_bowling_team.choose_bowler()
        self.umpire = Umpire()
        self.commentator = Commentator()

    def simulate_ball(self):
        outcome = self.umpire.predict_outcome(self.current_bowler, self.current_batsman)
        self.umpire.make_decision(outcome)
        self.commentator.provide_commentary(self.umpire.overs, self.current_bowler, self.current_batsman, outcome)

        if self.umpire.is_wicket_lost() or self.umpire.is_match_ended():
            self.change_innings()
        elif outcome == 'out':
            self.current_batsman = self.current_batting_team.batting_order[self.umpire.wickets]
        elif outcome != 'no_run':
            self.current_batsman = self.current_batting_team.batting_order[(self.umpire.scores // 4) % len(self.current_batting_team.batting_order)]
        else:
            self.current_batsman = self.current_batting_team.batting_order[(self.umpire.scores // 6) % len(self.current_batting_team.batting_order)]
        self.current_bowler = self.current_bowling_team.choose_bowler()
        self.umpire.overs += 0.1

    def end_match(self):
        print(f"Match ended. Final score: {self.current_batting_team.name} - {self.umpire.scores}/{self.umpire.wickets} in {self.umpire.overs} overs.")

# Taking input for teams
team1_name = input("Enter name for team 1: ")
team1 = Teams(team1_name)

num_players = int(input("Enter the number of players for team 1: "))
for i in range(num_players):
    name = input(f"Enter name for player {i + 1}: ")
    bowling = float(input(f"Enter bowling rating for player {i + 1}: "))
    batting = float(input(f"Enter batting rating for player {i + 1}: "))
    fielding = float(input(f"Enter fielding rating for player {i + 1}: "))
    running = float(input(f"Enter running rating for player {i + 1}: "))
    experience = float(input(f"Enter experience rating for player {i + 1}: "))
    player = Player(name, bowling, batting, fielding, running, experience)
    team1.add_player(player)

team2_name = input("Enter name for team 2: ")
team2 = Teams(team2_name)

num_players = int(input("Enter the number of players for team 2: "))
for i in range(num_players):
    name = input(f"Enter name for player {i + 1}: ")
    bowling = float(input(f"Enter bowling rating for player {i + 1}: "))
    batting = float(input(f"Enter batting rating for player {i + 1}: "))
    fielding = float(input(f"Enter fielding rating for player {i + 1}: "))
    running = float(input(f"Enter running rating for player {i + 1}: "))
    experience = float(input(f"Enter experience rating for player {i + 1}: "))
    player = Player(name, bowling, batting, fielding, running, experience)
    team2.add_player(player)

# Taking input for field information
field_size = input("Enter field size: ")
fan_ratio = input("Enter fan ratio: ")
pitch_conditions = input("Enter pitch conditions: ")
home_advantage = input("Enter home advantage: ")

field = Field(field_size, fan_ratio, pitch_conditions, home_advantage)

# Create objects for Umpire and Commentator classes if required
umpire = Umpire()
commentator = Commentator()

# Create a match object and start the match
match = Match(team1, team2, field)
match.start_match()
while not match.end_match():
    match.simulate_ball()

match.end_match()
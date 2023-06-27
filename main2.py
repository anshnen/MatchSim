import random

class Player:
    def __init__(self, name, batting, bowling, fielding, running, experience):
        self.name = name
        self.batting = batting
        self.bowling = bowling
        self.fielding = fielding
        self.running = running
        self.experience = experience

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.captain = None
        self.batting_order = []
        self.bowlers = []

    def select_captain(self):
        self.captain = random.choice(self.players)

    def set_batting_order(self, batting_order):
        self.batting_order = batting_order

    def choose_bowlers(self, num_bowlers):
        self.bowlers = random.sample(self.players, num_bowlers)

    def substitute_player(self, current_player, substitute_player):
        index = self.batting_order.index(current_player)
        self.batting_order[index] = substitute_player

class Field:
    def __init__(self, size, fan_ratio, pitch_conditions, home_advantage):
        self.size = size
        self.fan_ratio = fan_ratio
        self.pitch_conditions = pitch_conditions
        self.home_advantage = home_advantage

class Umpire:
    def __init__(self, team1, team2, field):
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.score = {team1.name: 0, team2.name: 0}
        self.wickets = {team1.name: 0, team2.name: 0}
        self.overs = 0

    def simulate_ball(self):
        batting_team = self.team1 if self.overs % 2 == 0 else self.team2
        bowling_team = self.team2 if self.overs % 2 == 0 else self.team1
        batsman = batting_team.batting_order[0]
        bowler = random.choice(bowling_team.bowlers)

        if random.random() < batsman.batting * bowler.bowling:
            # The batsman scores runs based on their batting and bowler's bowling stats
            runs_scored = random.randint(0, 6)
            self.score[batting_team.name] += runs_scored

            if runs_scored == 0:
                self.wickets[batting_team.name] += 1
                batting_team.batting_order.pop(0)

        self.overs += 0.1

    def simulate_match(self, no_of_deliveries):
        while self.overs < no_of_deliveries / 6:
            self.simulate_ball()

    def calculate_run_rate(self, team_name):
        overs_completed = int(self.overs)
        runs_scored = self.score[team_name]
        run_rate = runs_scored / overs_completed if overs_completed != 0 else 0.0
        return run_rate

    def calculate_required_run_rate(self, target, team_name):
        overs_remaining = int((no_of_deliveries / 6) - self.overs)
        runs_remaining = target - self.score[team_name]
        required_run_rate = runs_remaining / overs_remaining if overs_remaining != 0 else 0.0
        return required_run_rate

class Commentator:
    def __init__(self, umpire):
        self.umpire = umpire

    def provide_commentary(self):
        team1 = self.umpire.team1
        team2 = self.umpire.team2
        batting_team = team1 if self.umpire.overs % 2 == 0 else team2
        bowling_team = team2 if self.umpire.overs % 2 == 0 else team1
        batsman = batting_team.batting_order[0]
        bowler = random.choice(bowling_team.bowlers)

        print(f"Current Score: {self.umpire.score[batting_team.name]}/{self.umpire.wickets[batting_team.name]}")
        print(f"Current Over: {self.umpire.overs:.1f}")
        print(f"Batsman: {batsman.name} | Bowler: {bowler.name}")

class Match:
    def __init__(self, team1, team2, field):
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.umpire = Umpire(team1, team2, field)
        self.commentator = Commentator(self.umpire)
        self.target = 0

    def start_match(self, no_of_deliveries):
        self.team1.select_captain()
        self.team2.select_captain()
        self.team1.set_batting_order(self.team1.players)
        self.team2.set_batting_order(self.team2.players)
        self.team1.choose_bowlers(2)
        self.team2.choose_bowlers(2)

        self.umpire.simulate_match(no_of_deliveries)
        self.target = self.umpire.score[self.team1.name] + 1

    def end_match(self):
        print("Match ended.")
        print(f"Final Score: {self.umpire.score}")
        print(f"Final Wickets: {self.umpire.wickets}")
        print(f"Final Overs: {self.umpire.overs:.1f}")
        print()

        run_rate_team1 = self.umpire.calculate_run_rate(self.team1.name)
        required_run_rate_team2 = self.umpire.calculate_required_run_rate(self.target, self.team2.name)

        print(f"{self.team1.name}: {self.umpire.score[self.team1.name]}/{self.umpire.wickets[self.team1.name]}")
        print(f"{self.team2.name}: {self.umpire.score[self.team2.name]}/{self.umpire.wickets[self.team2.name]}")
        print()

        print(f"Run Rate ({self.team1.name}): {run_rate_team1:.2f}")
        print(f"Required Run Rate ({self.team2.name}): {required_run_rate_team2:.2f}")
        print()

        if self.umpire.score[self.team1.name] > self.umpire.score[self.team2.name]:
            print(f"{self.team1.name} won the match!")
        elif self.umpire.score[self.team1.name] < self.umpire.score[self.team2.name]:
            print(f"{self.team2.name} won the match!")
        else:
            print("The match ended in a draw.")

# Take user inputs
no_of_players = int(input("Enter the number of players in a team: "))
no_of_deliveries = int(input("Enter the number of deliveries in the match: "))

# Create player objects
players = []
for _ in range(no_of_players):
    name = input("Enter player name: ")
    while True:
        try:
            batting = float(input("Enter batting stat (0.0-1.0): "))
            bowling = float(input("Enter bowling stat (0.0-1.0): "))
            fielding = float(input("Enter fielding stat (0.0-1.0): "))
            running = float(input("Enter running stat (0.0-1.0): "))
            experience = float(input("Enter experience (0.0-1.0): "))
            break
        except ValueError:
            print("Invalid input. Please enter numeric values.")

    player = Player(name, batting, bowling, fielding, running, experience)
    players.append(player)

# Create team objects
team1_name = input("Enter Team 1 name: ")
team2_name = input("Enter Team 2 name: ")
team1 = Team(team1_name, players[:no_of_players])
team2 = Team(team2_name, players[no_of_players:])

# Create field object
size = input("Enter field size: ")
fan_ratio = input("Enter fan ratio: ")
pitch_conditions = input("Enter pitch conditions: ")
home_advantage = input("Enter home advantage: ")
field = Field(size, fan_ratio, pitch_conditions, home_advantage)

# Create match object and start the match
match = Match(team1, team2, field)
match.start_match(no_of_deliveries)

# End the match and display result
match.end_match()

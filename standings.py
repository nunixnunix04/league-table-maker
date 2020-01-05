import csv

# SETTINGS
country = "spain"
season = "1819" # Use the following format (eg: 2018-19 --> "1819")


filename = country + "/" + "season-" + season + "_csv.csv"

# Creates team
def create_team_list(reader):
	team_list = []
	for row in reader:
		team_name = row[2]
		if team_name not in team_list:
			team_list.append(team_name)
	del team_list[0]
	return team_list

class Team():
	
	def __init__(self, team, reader):
		self.team = team
		self.reader = reader
		self.matches = self.get_list_of_matches()
		self.wins = self.get_wins()
		self.draws = self.get_draws()
		self.losses = self.get_losses()
		self.points = self.get_points()
		self.goals_for = self.get_goals_for()
		self.goals_against = self.get_goals_against()
		self.goal_difference = self.get_goal_difference()

	def get_list_of_matches(self):
		list_of_matches = []
		for row in self.reader:
			if (self.team == row[2]):
				row.append("H")
				list_of_matches.append(row)
			elif (self.team == row[3]):
				row.append("A")
				list_of_matches.append(row)
		return list_of_matches

	def get_wins(self):
		wins = 0
		for match in self.matches:
			if (match[6] == match[-1]):
				wins += 1
		return wins

	def get_draws(self):
		draws = 0
		for match in self.matches:
			if match[6] == "D":
				draws += 1
		return draws

	def get_losses(self):
		losses = 0
		for match in self.matches:
			if (match[6] != match[-1]) and (match[6] != "D"):
				losses += 1
		return losses

	def get_points(self):
		points = (3 * self.wins) + (self.draws)
		return points


	def get_goals_for(self):
		goals_for = 0
		for match in self.matches:
			if (match[-1] == "H"):
				goals_for += int(match[4])
			elif (match[-1] == "A"):
				goals_for += int(match[5])
		return goals_for

	def get_goals_against(self):
		goals_against = 0
		for match in self.matches:
			if (match[-1] == "H"):
				goals_against += int(match[5])
			elif (match[-1] == "A"):
				goals_against += int(match[4])
		return goals_against

	def get_goal_difference(self):
		goal_difference = self.goals_for - self.goals_against
		return goal_difference
	
	def print_list_of_matches(self):
		for match in self.matches:
			print(match[2] + " " + match[4] + " - " + match[5] + " " + match[3])

	def print_season_summary(self):
		print("Team: " + self.team)
		print("\tGames Played: " + str(len(self.matches)))
		print("\tWins: " + str(self.wins))
		print("\tDraws: " + str(self.draws))
		print("\tLosses: " + str(self.losses))
		print("\tGoals For: " + str(self.goals_for))
		print("\tGoals Against: " + str(self.goals_against))
		print("\tGoal Difference: " + str(self.goal_difference))

league = {}
team_objects = []
with open(filename) as f:
	reader = csv.reader(f)
	team_list = create_team_list(reader)

for team in team_list:
	with open(filename) as f:
		reader = csv.reader(f)
		league[team] = Team(team, reader)
		team_objects.append(league[team])

team_objects_sorted = sorted(team_objects, key=lambda x: (x.points, x.goal_difference, x.goals_for), reverse=True)

league_table = [["#","Team","GP","W","D","L","GF","GA","GD","Points"]]

for i in range(len(team_objects_sorted)):
	team_row = [
	i+1,
	team_objects_sorted[i].team,
	len(team_objects_sorted[i].matches),
	team_objects_sorted[i].wins,
	team_objects_sorted[i].draws,
	team_objects_sorted[i].losses,
	team_objects_sorted[i].goals_for,
	team_objects_sorted[i].goals_against,
	team_objects_sorted[i].goal_difference,
	team_objects_sorted[i].points
	]
	league_table.append(team_row)

outfile_name = country + "/" + "league_table_" + filename[-12:-8] + ".csv"
with open(outfile_name,"w",newline="") as f:
	writer = csv.writer(f)
	writer.writerows(league_table)
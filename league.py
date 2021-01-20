from copy import copy


class Match:
    max_len = 0

    def __init__(self, match_string):
        """
        Match constructor
        :param match_string: Result of the match in string format
        :return: None
        """
        # spliting input string based on spaces to extract information
        self.match_string = match_string.split()
        self.home = self.match_string[0]
        self.away = self.match_string[4]
        self.home_goals = self.match_string[1]
        self.away_goals = self.match_string[3]
        # Finding longest team name to show table in beautiful manner
        mx_len = len(self.home) if len(self.home) > len(self.away) else len(self.away)
        Match.max_len = mx_len if mx_len > Match.max_len else Match.max_len

    def data(self):
        """
        Data function : returns each team's data in a single match
        :return: each team's data in a single match
        """
        # Updating each team's tupple
        home_tuple = (
            1,
            int(int(self.home_goals) > int(self.away_goals)),
            int(int(self.home_goals) == int(self.away_goals)),
            int(int(self.home_goals) < int(self.away_goals)),
            int(self.home_goals),
            int(self.away_goals),
            int(self.home_goals) - int(self.away_goals),
            int(int(self.home_goals) > int(self.away_goals)) * 3
            + int(int(self.home_goals) == int(self.away_goals)) * 1,
        )
        away_tuple = (
            1,
            home_tuple[3],
            home_tuple[2],
            home_tuple[1],
            home_tuple[5],
            home_tuple[4],
            home_tuple[6] * -1,
            1 if home_tuple[7] == 1 else 3 - home_tuple[7],
        )
        return home_tuple, away_tuple

    # Returns match string if object is called
    def __repr__(self):
        return f"{self.home : >{Match.max_len}} {self.home_goals : >2}  -  {self.away_goals : <2} {self.away}"

    # Returns match string if object is called
    def __str__(self):
        return f"{self.home : >{Match.max_len}} {self.home_goals : >2}  -  {self.away_goals : <2} {self.away}"


class Weeks:
    def __init__(self, no_of_week, first_matches=[]):
        """
        Weeks constructor
        :param no_of_week: Week number
        :param first_matches: Initial matches of the wwek
        :return: None
        """
        # Updating Week info
        self.no_of_week = no_of_week
        self.matches = first_matches.copy()

    def add_match(self, match):
        """
        add_match Function
        :param match: Match object to add to the Week
        :return: None
        """
        # Check if match already exist -> in this case deosn't add
        # Otherwise add match
        for it in self.matches:
            if (
                match.home.upper() == it.home.upper()
                or match.home.upper() == it.away.upper()
                or match.away.upper() == it.home.upper()
                or match.away.upper() == it.away.upper()
            ):
                break
        else:
            self.matches.append(match)

    # Returns Week Matches string if object is called
    def __repr__(self):
        str_weeks = "\n"
        # Call each match object to use it's __repr__ or __str__ method
        for print_object in self.matches:
            str_weeks += f"{print_object}\n"
        return str_weeks[: len(str_weeks) - 1]

    # Returns Week Matches string if object is called
    def __str__(self):
        str_weeks = "\n"
        # Call each match object to use it's __repr__ or __str__ method
        for print_object in self.matches:
            str_weeks += f"{print_object}\n"
        return str_weeks[: len(str_weeks) - 1]


class Team:
    total_teams = 0  # Counting number of created teams for ranking for the first time

    def __init__(self, team_name):
        """
        Team Constructor
        :param  team_name: Team's name in string format
        :return: None
        """
        # Initialize Team info
        Team.total_teams += 1
        self.rank = Team.total_teams
        self.name = team_name
        self.mp = 0
        self.w = 0
        self.d = 0
        self.l = 0
        self.gf = 0
        self.ga = 0
        self.gd = 0
        self.pts = 0
        self.matches = []

    def add_match(self, input_match):
        """
        add_match Function
        :param input_match: Match object to add to team's match
        :return: None
        """
        # Check if input match is related to this team
        # (team name is in this match)
        if input_match.home.upper() == self.name.upper():
            this_team = 0  # First output tuple of Match.read_data()
        elif input_match.away.upper() == self.name.upper():
            this_team = 1  # Second output tuple of Match.read_data()
        else:
            return
        # Update team info based on input match
        self.matches.append(input_match)
        self.mp += 1
        self.w += input_match.data()[this_team][1]
        self.d += input_match.data()[this_team][2]
        self.l += input_match.data()[this_team][3]
        self.gf += input_match.data()[this_team][4]
        self.ga += input_match.data()[this_team][5]
        self.gd += input_match.data()[this_team][6]
        self.pts += input_match.data()[this_team][7]

    # Returns Team Info if object is called
    def __repr__(self):
        return_str = f"{self.rank : <3} {self.name : <{Match.max_len}} {self.mp : <3} "
        return_str += f"{self.w : <3} {self.d : <3} {self.l : <3} {self.gf: <3} {self.ga: <3} {self.gd : <3} {self.pts :<3}"
        return return_str

    # Returns Team Info if object is calleds
    def __str__(self):
        return_str = f"{self.rank : <3} {self.name : <{Match.max_len}} {self.mp : <3} "
        return_str += f"{self.w : <3} {self.d : <3} {self.l : <3} {self.gf: <3} {self.ga: <3} {self.gd : <3} {self.pts :<3}"
        return return_str

    def __del__(self):
        # Decrease number of tems if a team is deleted
        Team.total_teams -= 1


class League:
    max_len = 0

    def __init__(self, teams, year):
        """
        League Constructor
        :param  teams: A List of teams that are in the league
        :param  year: Year of the league
        :return: None
        """
        self.all_weeks = []
        self.year = year
        self.standing = teams.copy()
        # Sort teams based on their initial ranking
        self.standing.sort(key=lambda input: input.rank)
        # Append first standing to all_standing (All Zero)
        list_to_append = []
        for i in range(len(self.standing)):
            list_to_append.append(copy(self.standing[i]))  # Used copy
        self.all_standing = []
        self.all_standing.append(list_to_append.copy())

    def __add_match(self, input_match):
        """
        __add_match Private Function -> adds matches of week to teams
        :param input_match: Match object to add to team's match
        :return: None
        """
        for standing_list in self.standing:
            standing_list.add_match(input_match)

    def add_week(self, input_week):
        """
        add_week  -> adds a week to league and and matches to teams
        :param input_week: Week object to add
        :return: None
        """
        # Add input week to league's list of weeks
        self.all_weeks.append(input_week)
        # Add matches of week to teams
        for week_match_object in input_week.matches:
            self.__add_match(week_match_object)
        # Sort Teams based on their info
        self.standing.sort(
            reverse=True,
            key=lambda input: (
                input.pts,
                input.gd,
                input.gf,
                input.w,
                [-ord(l) for l in input.name],
            ),
        )
        # Update Rank of Teams in thier new standing
        for i in range(len(self.standing)):
            self.standing[i].rank = i + 1
        # Append standing of this week to all_standing (end of week)
        list_to_append = []
        for i in range(len(self.standing)):
            list_to_append.append(copy(self.standing[i]))  # Used copy
        self.all_standing.append(list_to_append.copy())

    # Returns League Standing table if object is called
    def __repr__(self):
        dummy_str = "team"
        str_league = (
            f"#   {dummy_str : <{Match.max_len}} mp  w   d   l   gf  ga  gd  pts\n"
        )
        # Retrive each team's Info
        for print_object in self.standing:
            str_league += f"{print_object}\n"
        return str_league[: len(str_league) - 1]

    # Returns League Standing table if object is called
    def __str__(self):
        dummy_str = "team"
        str_league = (
            f"#   {dummy_str : <{Match.max_len}} mp  w   d   l   gf  ga  gd  pts\n"
        )
        # Retrive each team's Info
        for print_object in self.standing:
            str_league += f"{print_object}\n"
        return str_league[: len(str_league) - 1]

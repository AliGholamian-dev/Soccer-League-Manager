from league import Team, Match, Weeks, League


def read_data(file_name, year):
    """
    read_data  -> reads league's informatin from file
    :param file_name: Name of file to read data from
    :param year: Year of the league
    :return: League Class Object
    """
    teams = []
    weeks_and_matches = []
    # Open File in read mode
    with open(file_name, "r") as file_stream:
        for each_line in file_stream.readlines():  # Capture each line of file
            # Look for a line containing table word with ( : ) character following it
            if each_line.find("table") > -1 and each_line.find(":") > -1:
                # Look for the begining of table
                get_list_str = each_line[each_line.find("[") + 1 : each_line.find("]")]
                # Retrieve Teams name
                for names in get_list_str.split():
                    names = names.strip(",")
                    if names.find("'") > -1:
                        # Append team object to teams list
                        teams.append(Team(names.strip("'")))
                    elif names.find('"') > -1:
                        # Append team object to teams list
                        teams.append(Team(names.strip('"')))

            # Look for lines containing week word with ( : ) character following it
            if each_line.find("week") > -1 and each_line.find(":") > -1:
                # Append Week matches and it's number to list
                weeks_and_matches.append(
                    [
                        # Number of week
                        each_line[: each_line.find(":")].strip("week").split()[0],
                        # Match of week
                        each_line[each_line.find(":") + 1 :].strip("\n"),
                    ]
                )

    # Create week objects
    list_of_weeks = []
    for i in range(int(len(teams) * (len(teams) - 1) / 2)):
        list_of_weeks.append(Weeks(i))

    # Add matches to weeks
    for object in weeks_and_matches:
        list_of_weeks[int(object[0]) - 1].add_match(Match(object[1]))

    # Create League object
    league_object = League(teams, year)

    # Add weeks to League object
    for object_of_week in list_of_weeks:
        league_object.add_week(object_of_week)

    return league_object

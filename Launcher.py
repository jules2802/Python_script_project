import pydriller
from radon.complexity import cc_rank

from Methods import only_devoted_committers, create_graph, create_bar_graph, create_complexity_mean_plots

# Variables to change
project_name = "Pandas"
directory = "pandas"
branch = "master"

modifications_complexity_by_committers = {}

list_devoted_committers = only_devoted_committers(directory, branch)
print(f'The list of devoted committers is:{list_devoted_committers}')

for commit in pydriller.RepositoryMining(path_to_repo=directory, only_in_branch=branch,
                                         only_authors=list_devoted_committers).traverse_commits():

    file_modified = 0
    commit_total_complexity = 0
    if commit.committer.name in list_devoted_committers and len(
            commit.modifications) != 0:  ##Some commit dont have any modifications

        if commit.committer.name not in modifications_complexity_by_committers:
            modifications_complexity_by_committers[commit.committer.name] = []

        for modifications in commit.modifications:
            file_modified += 1

            if modifications.complexity is not None:
                print(f'{commit.committer.name} commit something')
                commit_total_complexity += modifications.complexity

        mean_complexity_commit = commit_total_complexity / file_modified
        modifications_complexity_by_committers[commit.committer.name].append(mean_complexity_commit)

mean = {}
a_tot_rank = []
b_tot_rank = []
c_tot_rank = []
d_tot_rank = []
e_tot_rank = []
f_tot_rank = []
for committer in modifications_complexity_by_committers:
    total_complexity = 0
    total_commit = 0

    list_commit = [] # x axis for plot grah
    list_complexity = []  # y axis for plot graph
    list_mean_complexity = [] # y_mean

    a_rank = []
    b_rank = []
    c_rank = []
    d_rank = []
    e_rank = []
    f_rank = []

    for commit in modifications_complexity_by_committers[committer]:
        total_commit += 1
        list_commit.append(total_commit)
        list_complexity.append(commit)

        if cc_rank(commit) == "A":
            a_rank.append(cc_rank(commit))
            a_tot_rank.append(cc_rank(commit))

        elif cc_rank(commit) == "B":
            b_rank.append(cc_rank(commit))
            b_tot_rank.append(cc_rank(commit))

        elif cc_rank(commit) == "C":
            c_rank.append(cc_rank(commit))
            c_tot_rank.append(cc_rank(commit))

        elif cc_rank(commit) == "D":
            d_rank.append(cc_rank(commit))
            d_tot_rank.append(cc_rank(commit))

        elif cc_rank(commit) == "E":
            e_rank.append(cc_rank(commit))
            e_tot_rank.append(cc_rank(commit))

        elif cc_rank(commit) == "F":
            f_rank.append(cc_rank(commit))
            f_tot_rank.append(cc_rank(commit))

        total_complexity += commit
        list_mean_complexity.append(total_complexity / total_commit)

    x_bar = ["A", "B", "C", "D", "E", "F"]
    y_bar = [len(a_rank), len(b_rank), len(c_rank), len(d_rank), len(e_rank), len(f_rank)]

    create_graph(list_commit, list_complexity, list_mean_complexity, project_name, committer)
    create_bar_graph(x_bar, y_bar, project_name, committer)

    moyenne_commiter = total_complexity / total_commit
    mean[committer] = (moyenne_commiter, cc_rank(moyenne_commiter), total_commit)

y_tot_bar = [len(a_tot_rank), len(b_tot_rank), len(c_tot_rank), len(d_tot_rank), len(e_tot_rank), len(f_tot_rank)]
create_bar_graph(x_bar, y_tot_bar, project_name, f"{project_name}_totale")

create_complexity_mean_plots(mean, project_name)
print(f'Total complexity for each rank is: A:{y_tot_bar[0]}, B:{y_tot_bar[1]}, C:{y_tot_bar[2]}, D:{y_tot_bar[3]}, E:{y_tot_bar[4]}, F:{y_tot_bar[5]}')
print(f"{project_name} has been analyze, Script is done")

import pydriller
import matplotlib.pyplot as plt
from numpy import polyfit, poly1d


def only_devoted_committers(directory, branch):
    all_committers = {}
    devoted_committers = []
    total_commit = 0
    for commit in pydriller.RepositoryMining(path_to_repo=directory, only_in_branch=branch).traverse_commits():
            total_commit += 1

            if commit.committer.name not in all_committers:
                all_committers[commit.committer.name] = 1
            else:
                all_committers[commit.committer.name] += 1
    print(f'List of all committers: {all_committers}')
    print(f'Total commit: {total_commit}')
    for committer in all_committers:
        if all_committers[committer] > 0.01 * total_commit and committer != "GitHub":  ## Keep only known committer name
            devoted_committers.append(committer)

    return devoted_committers


def create_graph(x, y, y_mean, project_name, person):
    plt.plot(x, y)
    plt.plot(x, y_mean, label="mean")
    plt.legend()
    plt.title("Complexité moyenne des fichiers modifiés par commit: " + person)
    plt.xlabel('Nième commit')
    plt.ylabel('Complexite moyenne')
    plt.savefig(f"Resultats/{project_name}/{person}_plot_graph.png", bbox_inches="tight", dpi=800, quality=100)
    plt.close()
    print(f'Plot graph for {person} created')


def create_bar_graph(x, y, project, person):
    plt.bar(x, y, 0.5)
    plt.title("Occurence des rangs de complexité moyenne par commit: " + person)
    plt.xlabel("Rang de complexité moyenne")
    plt.ylabel("Occurence")
    plt.savefig(f"Resultats/{project}/{person}_bar_graph.png", bbox_inches="tight", dpi=800, quality=100)
    plt.close()
    print(f'Bar graph for {person} created')


def create_complexity_mean_plots(moyenne, project):
    for committer in moyenne:
        x = moyenne[committer][2]
        y = moyenne[committer][0]
        plt.scatter(x, y, label=committer)

    plt.title("Complexité moyenne en fonction du nombre de commit réalisé par un developpeur")
    plt.xlabel('Nombre de commits')
    plt.ylabel('Complexité moyenne')
    plt.legend(loc="best", bbox_to_anchor=(1, 1))
    plt.savefig(f"Resultats/{project}/complexite_moyenne_{project}.png", dpi=800, quality=100, bbox_inches="tight")
    plt.close()
    print(f'Mean plots complexity for {project} project created')

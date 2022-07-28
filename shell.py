from models.contact_spatial.main import contact_spatial
from models.scanlon_kalahari.main import scanlon_kalahari
from models.tricritical.main import tricritical

from plot_density import plot_density
from purge_data import purge_data
from render_simulation import render_simulation


def show_help():
    print("---> Models <---")
    print("contact_spatial(p, num_parallel, save)")
    print("scanlon_kalahari(rainfall, num_parallel, save)")
    print("tricritical(p, num_parallel, save)")
    print("!!! All the above functions return the final (averaged) density !!!")
    print("")

    print("---> Analysis <---")
    print("plot_density(model_name, range)")
    print("render_simulation(model_name, simulation_index)")
    print("purge_data(model_name)")
    print("!!! The above functions require some saved data to operate on !!!")


if __name__ == '__main__':
    print("---> Cluster dynamics in Semi-Arid Vegetation <---")
    print("Project by: Chandan Relekar | Fork me at GitHub (chanrt)")
    print("GitHub organization: TEE-Lab")
    print("GitHub repository name: vegetation-dynamics")
    print("\nType 'help' to see the list of available commands.\n")

    while True:
        input_string = input(">> ")

        if input_string in ["quit", "exit"]:
            break
        elif input_string == "help":
            show_help()

        try:
            exec(input_string)
        except:
            print("Some error encountered")
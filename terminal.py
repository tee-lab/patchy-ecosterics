from models.contact_spatial.main import contact_spatial
from models.scanlon_kalahari.main import scanlon_kalahari
from models.tricritical.main import tricritical

from plot_density import plot_density
from purge_data import purge_data
from render_simulation import render_simulation


if __name__ == '__main__':
    """ Write automated scripts here """
    tricritical(1, 0.92, 5, True)
    render_simulation("tricritical", 0)
    plot_density("tricritical", range(5), 1)
    purge_data("tricritical")

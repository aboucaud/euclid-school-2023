import os
import argparse

import h5py
import tqdm
import numpy as np


#################################### INPUT ###########################################
ROOT = os.path.expanduser("~/Data/FOF_Subfind")
SNAPNUM = 33  # 33(z=0) 25(z=0.5) 19(z=1) 14(z=1.5) 10(z=2) 4(z=3)
NSTARS_THRES = 20
PROPERTIES = 17  # 14 without U,K,g
######################################################################################

redshift = {33: 0.0, 25: 0.5, 14: 1.5, 19: 1.0, 10: 2.0, 4: 3.0}[SNAPNUM]
print(f"Redshift: {redshift:.2f}")


def construct_offset(simulation, redshift, n_realizations):
    """
    Construct the offset for the galaxies in the file.
    """
    n_gal_tot = 0
    offset = np.zeros((n_realizations, 2), dtype=np.int64)
    # get the name of the file
    for i in tqdm.trange(n_realizations, desc="Computing n_gal"):
        file_name = os.path.join(
            ROOT, simulation, "LH", f"LH_{i}", f"fof_subhalo_tab_{SNAPNUM:03d}.hdf5"
        )

        # open the file
        f = h5py.File(file_name, "r")
        Nstars = f["/Subhalo/SubhaloLenType"][:, 4]
        f.close()

        n_gal = len(np.where(Nstars > NSTARS_THRES)[0])
        offset[i, 0] = n_gal_tot
        offset[i, 1] = n_gal
        n_gal_tot += n_gal

    offset_file = f"offset_{simulation}_z={redshift:.2f}.txt"
    header = "| offset in file | length |"

    np.savetxt(offset_file, offset, fmt="%d", header=header)

    return n_gal_tot


def construct_catalog(simulation, redshift, n_gal_tot, n_realizations):
    """
    Construct the catalogue for the galaxies in the file.
    """
    gal_prop = np.zeros((n_gal_tot, PROPERTIES), dtype=np.float32)
    count = 0
    # get the name of the file
    for i in tqdm.trange(n_realizations, desc="Computing gal properties"):
        file_name = os.path.join(
            ROOT, simulation, "LH", f"LH_{i}", f"fof_subhalo_tab_{SNAPNUM:03d}.hdf5"
        )
        # find the number of galaxies in it
        f = h5py.File(file_name, "r")

        Mg = f["/Subhalo/SubhaloMassType"][:, 0] * 1e10  # Msun/h
        Mstar = f["/Subhalo/SubhaloMassType"][:, 4] * 1e10  # Msun/h
        Mbh = f["/Subhalo/SubhaloBHMass"][:] * 1e10  # Msun/h
        Mtot = f["/Subhalo/SubhaloMass"][:] * 1e10  # Msun/h

        Vmax = f["/Subhalo/SubhaloVmax"][:]
        Vdisp = f["/Subhalo/SubhaloVelDisp"][:]

        Zg = f["/Subhalo/SubhaloGasMetallicity"][:]
        Zs = f["/Subhalo/SubhaloStarMetallicity"][:]
        SFR = f["/Subhalo/SubhaloSFR"][:]
        J = f["/Subhalo/SubhaloSpin"][:]
        V = f["/Subhalo/SubhaloVel"][:]
        J = np.sqrt(J[:, 0] ** 2 + J[:, 1] ** 2 + J[:, 2] ** 2)
        V = np.sqrt(V[:, 0] ** 2 + V[:, 1] ** 2 + V[:, 2] ** 2)

        Rstar = f["/Subhalo/SubhaloHalfmassRadType"][:, 4] / 1e3  # Mpc/h
        Rtot = f["/Subhalo/SubhaloHalfmassRad"][:] / 1e3  # Mpc/h
        Rvmax = f["/Subhalo/SubhaloVmaxRad"][:] / 1e3  # Mpc/h

        U = f["/Subhalo/SubhaloStellarPhotometrics"][:, 0]
        K = f["/Subhalo/SubhaloStellarPhotometrics"][:, 3]
        g = f["/Subhalo/SubhaloStellarPhotometrics"][:, 4]

        Nstars = f["/Subhalo/SubhaloLenType"][:, 4]
        f.close()

        # only take galaxies with more than 20 stars
        indexes = np.where(Nstars > NSTARS_THRES)[0]
        Ngal = len(indexes)

        # fill the matrix
        gal_prop[count : count + Ngal, 0] = Mg[indexes]
        gal_prop[count : count + Ngal, 1] = Mstar[indexes]
        gal_prop[count : count + Ngal, 2] = Mbh[indexes]
        gal_prop[count : count + Ngal, 3] = Mtot[indexes]
        gal_prop[count : count + Ngal, 4] = Vmax[indexes]
        gal_prop[count : count + Ngal, 5] = Vdisp[indexes]
        gal_prop[count : count + Ngal, 6] = Zg[indexes]
        gal_prop[count : count + Ngal, 7] = Zs[indexes]
        gal_prop[count : count + Ngal, 8] = SFR[indexes]
        gal_prop[count : count + Ngal, 9] = J[indexes]
        gal_prop[count : count + Ngal, 10] = V[indexes]
        gal_prop[count : count + Ngal, 11] = Rstar[indexes]
        gal_prop[count : count + Ngal, 12] = Rtot[indexes]
        gal_prop[count : count + Ngal, 13] = Rvmax[indexes]
        gal_prop[count : count + Ngal, 14] = U[indexes]
        gal_prop[count : count + Ngal, 15] = K[indexes]
        gal_prop[count : count + Ngal, 16] = g[indexes]
        count += Ngal

    galaxy_file = f"galaxies_{simulation}_z={redshift:.2f}.txt"
    header = "| gas mass | stellar mass | black-hole mass | total mass | Vmax | velocity dispersion | gas metallicity | stars metallicity | star-formation rate | spin | peculiar velocity | stellar radius | total radius | Vmax radius | U | K | g"
    np.savetxt(galaxy_file, gal_prop, fmt="%.6e", header=header)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--n_realizations",
        type=int,
        default=1000,
        help="size of the probed catalogues. Can be reduced to create smaller datasets",
    )

    args = parser.parse_args()

    # do a loop over IllustrisTNG and SIMBA
    for simulation in ["SIMBA", "IllustrisTNG"]:
        print(f"\n{simulation}")

        # find how many galaxies are there in total
        n_gal_tot = construct_offset(simulation, redshift, args.n_realizations)

        # define the matrix containing all galaxies with their PROPERTIES
        print(f"Total number of galaxies found: {n_gal_tot}")

        construct_catalog(simulation, redshift, n_gal_tot, args.n_realizations)


if __name__ == "__main__":
    main()

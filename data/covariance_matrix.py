import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def forward_backward_average(R):
    """
    Apply forward-backward averaging:
        R_fb = 0.5 * (R + J R* J)
    """
    if R.ndim != 2 or R.shape[0] != R.shape[1]:
        raise ValueError("R must be a square matrix.")

    N = R.shape[0]
    J = np.fliplr(np.eye(N))

    R_fb = 0.5 * (R + J @ R.conj() @ J)

    return R_fb, J


def hermitian_error(R):
    """
    Relative Hermitian-symmetry error:
        ||R - R^H||_F / ||R||_F
    """
    denominator = np.linalg.norm(R, ord="fro")

    if denominator == 0:
        return 0.0

    return (
        np.linalg.norm(R - R.conj().T, ord="fro")
        / denominator
    )


def centro_symmetry_error(R, J):
    """
    Relative conjugate centro-symmetry error:
        ||R - J R* J||_F / ||R||_F
    """
    denominator = np.linalg.norm(R, ord="fro")

    if denominator == 0:
        return 0.0

    return (
        np.linalg.norm(R - J @ R.conj() @ J, ord="fro")
        / denominator
    )


# ------------------------------------------------------------
# Load covariance matrices
# ------------------------------------------------------------
R_broadside = np.load("web/covariance_matrix_broadside.npy")
R_off_boresight = np.load("web/covariance_matrix_off_boresight.npy")

covariance_cases = [
    ("Broadside", 0, R_broadside),
    ("Off-boresight", 45, R_off_boresight),
]


# ------------------------------------------------------------
# Process each covariance matrix
# ------------------------------------------------------------
for case_name, theta_deg, R in covariance_cases:

    # Apply forward-backward averaging
    R_fb, J = forward_backward_average(R)

    # --------------------------------------------------------
    # Print structural errors
    # --------------------------------------------------------
    print(f"\n{case_name} covariance, theta = {theta_deg} deg")
    print("-" * 55)

    print("Before FB averaging")
    print(
        f"  Hermitian error       : "
        f"{hermitian_error(R):.3e}"
    )
    print(
        f"  Centro-symmetry error : "
        f"{centro_symmetry_error(R, J):.3e}"
    )

    print("After FB averaging")
    print(
        f"  Hermitian error       : "
        f"{hermitian_error(R_fb):.3e}"
    )
    print(
        f"  Centro-symmetry error : "
        f"{centro_symmetry_error(R_fb, J):.3e}"
    )

    relative_change = (
        np.linalg.norm(R_fb - R, ord="fro")
        / np.linalg.norm(R, ord="fro")
    )

    print(
        f"  Relative matrix change: "
        f"{relative_change:.3e}"
    )

    # --------------------------------------------------------
    # Select which covariance to plot
    # --------------------------------------------------------
    # Replace R_plot with R to display the original covariance.
    R_plot = R_fb

    R_mag = np.abs(R_plot)
    R_phase = np.angle(R_plot)

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(14, 6),
        constrained_layout=True
    )

    # --------------------------------------------------------
    # Covariance magnitude
    # --------------------------------------------------------
    image_mag = axes[0].imshow(
        R_mag,
        origin="lower",
        aspect="equal"
    )

    axes[0].set_title(
        rf"$|\hat{{\mathbf{{R}}}}_{{\mathrm{{FB}}}}|$, "
        rf"$\theta={theta_deg}^\circ$"
    )
    axes[0].set_xlabel("Antenna index")
    axes[0].set_ylabel("Antenna index")

    fig.colorbar(
        image_mag,
        ax=axes[0],
        shrink=0.9,
        label="Magnitude"
    )

    # --------------------------------------------------------
    # Covariance phase
    # --------------------------------------------------------
    image_phase = axes[1].imshow(
        R_phase,
        origin="lower",
        aspect="equal",
        vmin=-np.pi,
        vmax=np.pi,
        cmap="twilight"
    )

    axes[1].set_title(
        rf"$\arg\left(\hat{{\mathbf{{R}}}}_{{\mathrm{{FB}}}}\right)$, "
        rf"$\theta={theta_deg}^\circ$"
    )
    axes[1].set_xlabel("Antenna index")
    axes[1].set_ylabel("Antenna index")

    phase_cbar = fig.colorbar(
        image_phase,
        ax=axes[1],
        shrink=0.9,
        label="Phase [rad]"
    )

    phase_cbar.set_ticks(
        [-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]
    )
    phase_cbar.set_ticklabels(
        [
            r"$-\pi$",
            r"$-\pi/2$",
            r"$0$",
            r"$\pi/2$",
            r"$\pi$"
        ]
    )

    fig.suptitle(
        f"{case_name} Covariance Matrix after FB Averaging\n"
        f"N = {R.shape[0]}"
    )

plt.show()
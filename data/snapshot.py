import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# ------------------------------------------------------------
# Load measured snapshots
# ------------------------------------------------------------
broadside = np.load("web/snapshot_data_broadside.npz")
off_boresight = np.load("web/snapshot_data_off_boresight.npz")

M = 8
virtual_channel = np.arange(M)
element_spacing_lambda = 0.5


def load_measurement(data):
    """Load complex snapshot and stored calibrated phase."""

    if "snapshot" in data:
        snapshot = np.asarray(data["snapshot"])
    else:
        snapshot = (
            np.asarray(data["real_part"])
            + 1j * np.asarray(data["imag_part"])
        )

    if "calibrated_phase_deg" not in data:
        raise KeyError(
            "'calibrated_phase_deg' is missing. "
            f"Available keys: {data.files}"
        )

    phase_deg = np.asarray(data["calibrated_phase_deg"])

    return snapshot[:M], phase_deg[:M]


x_broadside, phase_broadside_deg = load_measurement(broadside)
x_off_boresight, phase_off_deg = load_measurement(off_boresight)

# Remove complex DC component only from the I/Q data used for plotting
x_broadside_dc_free = x_broadside - np.mean(x_broadside)
x_off_boresight_dc_free = x_off_boresight - np.mean(x_off_boresight)


# ------------------------------------------------------------
# DoA estimation from stored calibrated phase
# ------------------------------------------------------------
def estimate_doa_from_phase(
    phase_deg,
    element_spacing_lambda=0.5,
):
    phase_rad = np.unwrap(np.deg2rad(phase_deg))

    slope, intercept = np.polyfit(
        virtual_channel,
        phase_rad,
        1,
    )

    phase_fit_rad = slope * virtual_channel + intercept

    # slope = -2*pi*(d/lambda)*sin(theta)
    sin_theta = -slope / (
        2 * np.pi * element_spacing_lambda
    )
    sin_theta = np.clip(sin_theta, -1.0, 1.0)

    theta_deg = np.rad2deg(np.arcsin(sin_theta))

    return (
        np.rad2deg(phase_rad),
        np.rad2deg(phase_fit_rad),
        slope,
        theta_deg,
    )


(
    phase_broadside_deg,
    fit_broadside_deg,
    slope_broadside,
    doa_broadside,
) = estimate_doa_from_phase(
    phase_broadside_deg,
    element_spacing_lambda,
)

(
    phase_off_deg,
    fit_off_deg,
    slope_off,
    doa_off,
) = estimate_doa_from_phase(
    phase_off_deg,
    element_spacing_lambda,
)

# Reference measured phases and fits to virtual channel 0
phase_broadside_deg -= phase_broadside_deg[0]
fit_broadside_deg -= fit_broadside_deg[0]

phase_off_deg -= phase_off_deg[0]
fit_off_deg -= fit_off_deg[0]


# ------------------------------------------------------------
# Smooth I/Q curves for visualization
# ------------------------------------------------------------
virtual_channel_smooth = np.linspace(
    virtual_channel.min(),
    virtual_channel.max(),
    200,
)


def smooth_curve(values):
    spline = make_interp_spline(
        virtual_channel,
        values,
        k=3,
    )
    return spline(virtual_channel_smooth)


# ------------------------------------------------------------
# Plot I/Q and stored calibrated phase
# ------------------------------------------------------------
fig, (ax_iq, ax_phase) = plt.subplots(
    1,
    2,
    figsize=(16, 6),
)

# Smoothed I/Q curves
ax_iq.plot(
    virtual_channel_smooth,
    smooth_curve(x_broadside_dc_free.real),
    label=r"$I$, broadside",
)
ax_iq.plot(
    virtual_channel_smooth,
    smooth_curve(x_broadside_dc_free.imag),
    linestyle="--",
    label=r"$Q$, broadside",
)
ax_iq.plot(
    virtual_channel_smooth,
    smooth_curve(x_off_boresight_dc_free.real),
    label=r"$I$, off-boresight",
)
ax_iq.plot(
    virtual_channel_smooth,
    smooth_curve(x_off_boresight_dc_free.imag),
    linestyle="--",
    label=r"$Q$, off-boresight",
)

# Original measured I/Q samples
ax_iq.plot(
    virtual_channel,
    x_broadside_dc_free.real,
    "o",
)
ax_iq.plot(
    virtual_channel,
    x_broadside_dc_free.imag,
    "s",
)
ax_iq.plot(
    virtual_channel,
    x_off_boresight_dc_free.real,
    "o",
)
ax_iq.plot(
    virtual_channel,
    x_off_boresight_dc_free.imag,
    "s",
)

ax_iq.set_title("Measured Snapshot Components")
ax_iq.set_xlabel("Virtual channel index")
ax_iq.set_ylabel("Amplitude")
ax_iq.set_xticks(virtual_channel)
ax_iq.grid(True, alpha=0.25)
ax_iq.legend()

# Stored calibrated phase
ax_phase.plot(
    virtual_channel,
    phase_broadside_deg,
    "o",
    label=r"Broadside phase",
)
ax_phase.plot(
    virtual_channel,
    phase_off_deg,
    "s",
    label=r"Off-boresight phase",
)

# Linear phase fits
ax_phase.plot(
    virtual_channel,
    fit_broadside_deg,
    "--",
    label=rf"Fit: $\hat{{\theta}}={doa_broadside:.1f}^\circ$",
)
ax_phase.plot(
    virtual_channel,
    fit_off_deg,
    "--",
    label=rf"Fit: $\hat{{\theta}}={doa_off:.1f}^\circ$",
)

ax_phase.set_title("Measured Calibrated Phase")
ax_phase.set_xlabel("Virtual channel index")
ax_phase.set_ylabel("Relative phase [deg]")
ax_phase.set_xticks(virtual_channel)
ax_phase.grid(True, alpha=0.25)
ax_phase.legend()

fig.suptitle("AWR2243 Single-Corner-Reflector Snapshots")
fig.tight_layout()

plt.show()

print(
    f"Broadside: slope = {slope_broadside:.4f} rad/channel, "
    f"estimated DoA = {doa_broadside:.2f} deg"
)
print(
    f"Off-boresight: slope = {slope_off:.4f} rad/channel, "
    f"estimated DoA = {doa_off:.2f} deg"
)
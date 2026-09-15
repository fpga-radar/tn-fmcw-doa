# FMCW Radar DoA Estimation

Direction-of-arrival estimation for automotive FMCW MIMO radar, covering the signal model, snapshot extraction, covariance-matrix processing, and the main DoA algorithms: Spatial FFT, Bartlett, Capon/MVDR, MUSIC, and ESPRIT.

The methods are organized into three groups: conventional beamforming with the Spatial FFT and Bartlett beamformer, adaptive beamforming with Capon/MVDR, and subspace-based estimation with MUSIC and ESPRIT.

![DoA estimation methods](docs/images/blockdiagram.png)

The Jupyter notebooks introduce the FMCW MIMO signal model, snapshot extraction strategies, covariance-matrix estimation and preprocessing, and the assumptions behind each DoA algorithm. Key formulas are complemented by compact Python implementations, numerical examples, and practical engineering observations.


The theoretical foundations and algorithm implementations are validated using real measurements acquired with a Texas Instruments **AWR2243** radar. The radar is configured as a two-transmitter, four-receiver TDM MIMO system, forming an eight-element virtual uniform linear array. 

The validation datasets are provided as part of the workshop:

### DoA estimation with two static corner reflectors

This workshop evaluates angular resolution in controlled broadside and off-boresight scenarios using static corner reflectors. The corresponding workshop and dataset are available [here](https://www.fpga-radar.com/doa-estimation-for-automotive-fmcw-radar).


## Contents

See the project homepage [here](https://www.fpga-radar.com/fmcw-radar-doa) for examples, too.

The below chapters are rendered via the nbviewer at nbviewer.jupyter.org/, and is read-only and rendered in real-time. Interactive notebooks + examples can be downloaded by cloning!

1. **Signal Model** ·
   [Read chapter](https://farbius.github.io/fmcw-radar-doa/01_signal_model.html) ·
   [View notebook](https://github.com/farbius/fmcw-radar-doa/blob/main/notebooks/01_signal_model.ipynb)

   The narrowband array signal model used for direction-of-arrival (DoA) estimation in FMCW radar

2. **Covariance Matrix** ·
   [Read chapter](https://farbius.github.io/fmcw-radar-doa/02_covariance_matrix.html) ·
   [View notebook](https://github.com/farbius/fmcw-radar-doa/blob/main/notebooks/02_covariance_matrix.ipynb)

   Spatial covariance estimation, matrix interpretation, forward-backward averaging, diagonal loading, eigendecomposition, and source-number estimation for covariance-based DoA processing

3. **FMCW MIMO** ·
   [Read chapter](https://farbius.github.io/fmcw-radar-doa/03_fmcw_mimo.html) ·
   [View notebook](https://github.com/farbius/fmcw-radar-doa/blob/main/notebooks/03_fmcw_mimo.ipynb)

   FMCW TDM-MIMO processing for DoA estimation, with emphasis on the processing chain, covariance snapshot extraction, and comparison of snapshot-formation strategies.

4. **Spatial FFT Beamformer** ·
   [Read chapter](https://farbius.github.io/fmcw-radar-doa/04_fft_beamformer.html) ·
   [View notebook](https://github.com/farbius/fmcw-radar-doa/blob/main/notebooks/04_fft_beamformer.ipynb)

   FFT beamformer fundamentals and performance analysis, including angular resolution and spectral leakage.

5. **Bartlett Beamformer** ·
   [Read chapter](https://farbius.github.io/fmcw-radar-doa/05_bartlett.html) ·
   [View notebook](https://github.com/farbius/fmcw-radar-doa/blob/main/notebooks/05_bartlett.ipynb)

   Bartlett beamformer fundamentals and performance analysis, including angular resolution and steering grid sampling.

6. **Capon MVDR Beamformer** ·
   [Read chapter](https://farbius.github.io/fmcw-radar-doa/06_capon_mvdr.html) ·
   [View notebook](https://github.com/farbius/fmcw-radar-doa/blob/main/notebooks/06_capon_mvdr.ipynb)

   Capon/MVDR beamformer fundamentals and performance analysis, including covariance preprocessing with validation on **AWR2243**, angular resolution, and sensitivity to array-model mismatch.

7. **MUSIC** ·
   [Read chapter](https://farbius.github.io/fmcw-radar-doa/07_music.html) ·
   [View notebook](https://github.com/farbius/fmcw-radar-doa/blob/main/notebooks/07_music.ipynb)

   MUSIC fundamentals and performance analysis, including subspace decomposition, probability of resolution, DoA estimation accuracy, and validation on **AWR2243**.

8. **ESPRIT** ·
   [Read chapter](https://farbius.github.io/fmcw-radar-doa/08_esprit.html) ·
   [View notebook](https://github.com/farbius/fmcw-radar-doa/blob/main/notebooks/08_esprit.ipynb)

   ESPRIT LS (Least-Squares) and TLS (Total Least-Squares) fundamentals and performance analysis, including probability of resolution, DoA estimation accuracy, and validation on **AWR2243**.

9. **Experimental Validation of DoA Algorithms**
   - [9.1 Corner Reflector Scenario](https://farbius.github.io/fmcw-radar-doa/09_corner_reflectors.html)
   - [9.2 Street Scene Scenario](https://farbius.github.io/fmcw-radar-doa/10_street_scene.html)


### References

1. Van Trees, H. L., *Optimum Array Processing: Part IV of Detection, Estimation, and Modulation Theory*. New York: John Wiley & Sons, 2002.
2. Wirth, W.-D., *Radar Techniques Using Array Antennas*, 2nd ed. London: Institution of Engineering and Technology, 2013.  
3. Bergin, J. S., and Guerci, J. R., *MIMO Radar: Theory and Application*. Boston, MA: Artech House, 2018.
4. Wen, D., Yi, H., Zhang, W., and Xu, H., “2D-Unitary ESPRIT Based Multi-Target Joint Range and Velocity Estimation Algorithm for FMCW Radar,” *Applied Sciences*, vol. 13, no. 18, art. 10448, 2023. doi: 10.3390/app131810448.
5. Kim, B.-S., Jin, Y., Lee, J., and Kim, S., “FMCW Radar Estimation Algorithm with High Resolution and Low Complexity Based on Reduced Search Area,” *Sensors*, vol. 22, no. 3, art. 1202, 2022. doi: 10.3390/s22031202.
6. Oh, D., and Lee, J.-H., “Low-Complexity Range-Azimuth FMCW Radar Sensor Using Joint Angle and Delay Estimation Without SVD and EVD,” *IEEE Sensors Journal*, vol. 15, no. 9, pp. 4799–4811, Sep. 2015. doi: 10.1109/JSEN.2015.2428814.


### helpers

```sh
jupyter nbconvert --to html --template classic .\notebooks\xx_sample_page.ipynb --output-dir .\docs
```
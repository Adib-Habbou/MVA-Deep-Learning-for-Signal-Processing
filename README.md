# MVA-Deep-Learning-for-Signal-Processing

Source Separation using classical filers and then Deep Learning models such as WaVE-U-Net, Conv-TasNet, HybridDemucs.

| Model              | MSE Loss  | SDR      | PESQ    | STOI     | Number of Parameters | Inference Time |
|--------------------|-----------|----------|---------|----------|----------------------|----------------|
| Wiener Filter      | 2.18e-04  | -10.6569 | 2.08805 | 0.80397  | 1                    | 4 ms           |
| Butterworth Filter | 2.23e-04  | -3.7573  | 1.57805 | 0.895725 | 4                    | 7 ms           |
| Dumb Model         | 7.76e-03  | -55.7942 | 1.20344 | 0.001805 | 400 K                | 3 ms           |
| WaveUNet Model     | 7.89e-06  | 6.72842  | 2.93885 | 0.6882   | 10.1 M               | 74 ms          |
| ConvTasnet Model   | 4.88e-06  | 5.8216   | 2.31814 | 0.701365 | 2.5 M                | 36 ms          |
| HybridDemucs Model | 2.67e-06  | 5.06163  | 1.97447 | 0.787565 | 2.5 M                | 21 ms          |

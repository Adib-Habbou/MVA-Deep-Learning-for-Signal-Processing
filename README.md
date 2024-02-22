# MVA-Deep-Learning-for-Signal-Processing

Source Separation using WaVE-U-Net, Conv-TasNet, HybridDemucs:

| Model              | MSE Loss  | SDR      | PESQ    | STOI     | Number of Parameters | Inference Time |
|--------------------|-----------|----------|---------|----------|----------------------|----------------|
| Wiener Filter      | 2.18e-04  | -10.6569 | 2.08805 | 0.80397  | 1                    | 4 ms           |
| Butterworth Filter | 2.23e-04  | -3.7573  | 1.57805 | 0.895725 | 4                    | 7 ms           |
| Dumb Model         | 7.76e-03  | -55.7942 | 1.20344 | 0.001805 | 400 K                | 3 ms           |
| WaveUNet Model     | 7.89e-06  | 6.72842  | 2.93885 | 0.6882   | 10.1 M               | 74 ms          |
| ConvTasnet Model   | 4.88e-06  | 5.8216   | 2.31814 | 0.701365 | 2.5 M                | 36 ms          |
| HybridDemucs Model | 2.67e-06  | 5.06163  | 1.97447 | 0.787565 | 2.5 M                | 21 ms          |

**Wiener** : Préserve le signal et l'intelligibilité, mais un SDR très bas suggère une séparation avec une distorsion significative, il utilise très peu de paramètres et a un temps d'inférence rapide.

**Butterworth** : Similaire à Wiener avec à nouveau un SDR négatif indiquant une séparation relativement pauvre, il utilise plus de paramètres et a un temps d'inférence légèrement plus long.

**WaveUNet** : Affiche un faible MSE Loss, avec le SDR et le PESQ les plus élevés, soulignant sa supériorité dans la préservation du signal et la perception de la qualité audio.

=> nécessite toutefois très un grand nombre de paramètres et a le temps d'inférence le plus long de tous les modèles.

**ConvTasnet** : Performe bien avec un faible MSE Loss, un SDR positif et un PESQ relativement élevé, montrant une séparation efficace des sources et une qualité audio décente.

=> utilise 4 fois moins de paramètres que le WaveUNet et en affichant un temps d'inférence 2 fois plus rapide.

**HybridDemucs** : Performe de manière similaire à ConvTasnet en termes de MSE Loss et SDR, avec un PESQ inférieur mais un STOI plus élevé, indiquant une bien meilleure intelligibilité.

=> utilise le même nombre de paramètres que le ConvTasnet mais avec un temps d'inférence plus court.

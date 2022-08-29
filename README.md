# Disruptive prediction model using KSTAR video and numerical data via Deep Learning
## Introduction
<img src="/image/연구_소개_01.PNG"  width="900" height="224">
<p>Research for predicting tokamak plasma disruption from video and numerical data via Deep Learning</p>

## How to Run
### setting
- Environment
```
conda create env -f environment.yaml
conda activate research-env
```

- Video Data Generation
```
# generate disruptive video data and normal video data from .avi
python3 ./src/generate_video_data.py --fps 210 --duration 21 --distance 5 --save_path './dataset/'
# train and test split with converting video as image sequences
python3 ./src/preprocessing.py --test_ratio 0.2 --valid_ratio 0.2 --video_data_path './dataset/dur21_dis0' --save_path './dataset/dur21_dis0'
```

- 0D Data(Numerical Data) Generation
```
# interpolate KSTAR data and convert as tabular dataframe
python3 ./src/generate_numerical_data.py 
```

### training
```
# ViViT model
python3 train_vivit.py --batch_size {batch size} --gpu_num {gpu num} --model_name {model name} --use_LDAM {bool : use LDAM loss}

# slowfast model
python3 train_slowfast.py --batch_size {batch size} --alpha {alpha} --gpu_num {gpu num} --model_name {model name} --use_LDAM {bool : use LDAM loss}

# R2Plus1D model
python3 train_R2Plus1D.py --batch_size {batch size} --gpu_num {gpu num} --model_name {model name} --use_LDAM {bool : use LDAM loss}
```

### Experiment
```
# experiment with different learning algorithm and models
python3 experiment.py --gpu_num {gpu_num} --loss_type {'CE', 'FOCAL', 'LDAM'}
```

## Detail
### model to use
- Video Encoder
1. SITS-BERT : not used
2. R2Plus1D
3. Slowfast
4. UTAE : not used
5. R3D
6. ViViT

- Tabular Encoder
1. Transformer
2. Self-Attention
3. Conv1D-LSTM
4. Tabnet

### technique or algorithm to use
1. Solving imbalanced classificatio issue
- Adversarial Training 
- Re-Sampling : ImbalancedWeightedSampler, Over-Sampling for minor classes
- Re-Weighting : Define inverse class frequencies as weights to apply with loss function (CE, Focal Loss, LDAM Loss)
- LDAM with DRW : Label-distribution-aware margin loss with deferred re-weighting scheduling

2. Analysis on physical characteristics of disruptive video data
- CAM
- Grad CAM

3. Data augmentation
- Video Mixup Algorithm for Data augmentation(done, not effective)
- Conventional Image Augmentation(Flip, Brightness, Contrast, Blur, shift)

4. Training Process enhancement
- Multigrid training algorithm : Fast training for SlowFast

### Additional Task
- Multi-GPU distributed Learning : done
- Database contruction : Tabular dataset(IKSTAR) + Video dataset, done
- ML Pipeline : Tensorboard

### Dataset
1. Disruption : disruptive state at t = tipminf (current-quench)
2. Borderline : inter-plane region(not used)
3. Normal : non-disruptive state

### Code Structure
```
```

## Reference
- R2Plus1D : A Spatial-temporal Attention Module for 3D Convolution Network in Action Recognition
- Slowfast : SlowFast Networks for Video Recognition
- Multigrid : A Multigrid Method for Efficiently Training Video Models, Chao-Yuan Wu et al, 2020
- Video Data Augmentation : VideoMix: Rethinking Data Augmentation for Video Classification
- SITS-BERT : Self-Supervised pretraining of Transformers for Satellite Image Time Series Classification
- UTAE : Panoptic Segmentation of Satellite Image Time Series with Convolutional Temporal Attention Networks
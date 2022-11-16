# Disruptive prediction model using KSTAR video and numerical data via Deep Learning
## Introduction
<div>
    <p>Research for predicting tokamak plasma disruption from video and numerical data via Deep Learning</p>
    <img src="/image/연구_소개_01.PNG"  width="900" height="224">
</div>
<div>
    <p>This research aims to predict disruptive phase using KSTAR IVIS(video) for real experiment shot</p>
    <p float = "left">
        <img src="/image/연구_소개_02.PNG"  width="320" height="196">
        <img src="/image/연구_소개_03.PNG"  width="320" height="196">
    </p>
</div>
<div>
    <p>We can proceed real-time disruption prediction using video data for shot 21310</p>
    <p float = 'left'>
        <img src="/image/연구_소개_04.PNG"  width="320" height="200">
        <img src="/results/real_time_disruption_prediction_21310.gif"  width="320" height="200">
    </p>
    <p>And this is the real-time disruption prediction using 0D data for shot 21310</p>
    <p>We can predict plasma disruption prior to 95.2ms(maximum prediction time) with 0D data</p>
    <p float = 'left'>
        <img src="/image/연구_소개_05.PNG"  width="320" height="196">
        <img src="/image/연구_소개_06.PNG"  width="320" height="196">
    </p>
</div>

- Video data would be helpful to detect VDE(Vertical Displacement Error) and time-varying shape characteristcs
- In future, we will try to predict disruption using multimodal data(video + 0D data)</p>

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

### Training

- Models for video data
```
# ViViT model
python3 train_vivit.py --batch_size {batch size} --gpu_num {gpu num} --use_LDAM {bool : use LDAM loss}

# slowfast model
python3 train_slowfast.py --batch_size {batch size} --alpha {alpha} --gpu_num {gpu num} --use_LDAM {bool : use LDAM loss}

# R2Plus1D model
python3 train_R2Plus1D.py --batch_size {batch size} --gpu_num {gpu num} --use_LDAM {bool : use LDAM loss}
```

- Models for 0D data
```
# Conv-LSTM
python3 train_conv_lstm.py --batch_size {batch size} --gpu_num {gpu num} --use_LDAM {bool : use LDAM loss}

# Transformer
python3 train_ts_transformer.py --batch_size {batch size} --alpha {alpha} --gpu_num {gpu num} --use_LDAM {bool : use LDAM loss}
```

- Models for MultiModal(video + 0D data)
```
python3 train_multi_modal.py --batch_size {batch size} --alpha {alpha} --gpu_num {gpu num --use_LDAM {bool : use LDAM loss}
```

### Experiment
```
# experiment with different learning algorithm and models
python3 experiment.py --gpu_num {gpu_num} --loss_type {'CE', 'FOCAL', 'LDAM'}
```

## Detail
### model to use
- Video encoder
1. R2Plus1D
2. Slowfast
3. ViViT (selected)

- 0D data encoder
1. Transformer
2. Conv1D-LSTM using self-attention (selected)

- Multimodal Model
1. Multimodal fusion model: video encoder + 0D data encoder
2. Tensor Fusion Network

### technique or algorithm to use
1. Solving imbalanced classificatio issue
- Adversarial Training 
- Re-Sampling : ImbalancedWeightedSampler, Over-Sampling for minor classes
- Re-Weighting : Define inverse class frequencies as weights to apply with loss function (CE, Focal Loss, LDAM Loss)
- LDAM with DRW : Label-distribution-aware margin loss with deferred re-weighting scheduling
- Multimodal Learning : Gradient Blending for avoiding sub-optimal due to large modalities
- Multimodal Learning : CCA Learning for enhancement

2. Analysis on physical characteristics of disruptive video data
- CAM
- Grad CAM
- attention rollout

3. Data augmentation
- Video Mixup Algorithm for Data augmentation(done, not effective)
- Conventional Image Augmentation(Flip, Brightness, Contrast, Blur, shift)

4. Training Process enhancement
- Multigrid training algorithm : Fast training for SlowFast

5. Generalization and Robustness
- Add noise with image sequence and 0D data for robustness
- Multimodality can also guarantee the robustness from noise of the data
- Gradient Blending for avoiding sub-optimal states from multi-modal learning

### Additional Task
- Multi-GPU distributed Learning : done
- Database contruction : Tabular dataset(IKSTAR) + Video dataset, done
- ML Pipeline : Tensorboard

### Dataset
1. Disruption : disruptive state at t = tipminf (current-quench)
2. Borderline : inter-plane region(not used)
3. Normal : non-disruptive state

## Reference
- R2Plus1D : A Spatial-temporal Attention Module for 3D Convolution Network in Action Recognition
- Slowfast : SlowFast Networks for Video Recognition
- Multigrid : A Multigrid Method for Efficiently Training Video Models, Chao-Yuan Wu et al, 2020
- Video Data Augmentation : VideoMix: Rethinking Data Augmentation for Video Classification
- UTAE : Panoptic Segmentation of Satellite Image Time Series with Convolutional Temporal Attention Networks
- LDAM : Label-distribution-aware Margin Loss
# python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 2 --dist 3 --batch_size 8 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'CE' --use_sampling '' --use_weighting '' --use_DRW ''
# python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 2 --dist 3 --batch_size 8 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'CE' --use_sampling 1 --use_weighting '' --use_DRW ''
# python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 2 --dist 3 --batch_size 8 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'CE' --use_sampling '' --use_weighting 1 --use_DRW ''
# python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 1 --dist 3 --batch_size 8 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'CE' --use_sampling 1 --use_weighting 1 --use_DRW ''
python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 3 --dist 3 --batch_size 32 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'CE' --use_sampling '' --use_weighting '' --use_DRW 1
python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 3 --dist 3 --batch_size 32 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'CE' --use_sampling 1 --use_weighting '' --use_DRW 1

# python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 2 --dist 3 --batch_size 8 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'Focal' --use_sampling '' --use_weighting '' --use_DRW ''
# python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 2 --dist 3 --batch_size 8 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'Focal' --use_sampling 1 --use_weighting '' --use_DRW ''
# python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 2 --dist 3 --batch_size 8 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'Focal' --use_sampling '' --use_weighting 1 --use_DRW ''
python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 3 --dist 3 --batch_size 32 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'Focal' --use_sampling 1 --use_weighting 1 --use_DRW ''
python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 3 --dist 3 --batch_size 32 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'Focal' --use_sampling '' --use_weighting '' --use_DRW 1
python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 3 --dist 3 --batch_size 32 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'Focal' --use_sampling 1 --use_weighting '' --use_DRW 1

# python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 2 --dist 3 --batch_size 8 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'LDAM' --use_sampling '' --use_weighting '' --use_DRW ''
# python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 2 --dist 3 --batch_size 8 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'LDAM' --use_sampling 1 --use_weighting '' --use_DRW ''
# python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 2 --dist 3 --batch_size 8 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'LDAM' --use_sampling '' --use_weighting 1 --use_DRW ''
python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 3 --dist 3 --batch_size 32 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'LDAM' --use_sampling 1 --use_weighting 1 --use_DRW ''
python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 3 --dist 3 --batch_size 32 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'LDAM' --use_sampling '' --use_weighting '' --use_DRW 1
python3 train_vision_network.py --lr 0.0002 --num_epoch 50 --gpu_num 3 --dist 3 --batch_size 32 --model 'SlowFast' --tag 'SlowFast-exp' --loss_type 'LDAM' --use_sampling 1 --use_weighting '' --use_DRW 1
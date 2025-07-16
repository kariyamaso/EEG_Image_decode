# EEG_Image_decode 実行手順

このドキュメントでは、MEGデータの前処理から学習、評価までの具体的な手順を説明します。

## 環境セットアップ

1. **仮想環境の作成とパッケージのインストール**
```bash
bash setup.sh
source .venv/bin/activate
```

## データの準備

### 1. MEGデータの前処理

MEG-preprocessing/pre_possess.ipynb をJupyterで開いて実行します：

```bash
jupyter lab MEG-preprocessing/pre_possess.ipynb
```

ノートブックで以下の処理が行われます：
- MEGエポックデータの読み込みとクロップ（0-1秒）
- トレーニングセットとゼロショットテストセットの分離
- データの形状変換と保存
- 画像ファイルの適切なディレクトリへの配置

### 2. 画像特徴量の抽出

CLIPモデルを使用して画像特徴量を抽出します：

```bash
cd Generation
python extract_clip_features.py
```

## モデルの学習

### 1. 画像再構成モデル（VAE）の学習

低レベル特徴量を使用したVAEモデルの学習：

```bash
cd Generation
python train_vae_latent_512_low_level_no_average.py \
    --num_epochs 200 \
    --batch_size 16 \
    --learning_rate 3e-4 \
    --gpu auto
```

### 2. 画像検索モデル（ATMS）の学習

MEGデータから画像を検索するモデルの学習：

```bash
cd Retrieval
python ATMS_retrieval_joint_train.py \
    --dnn "alexnet" \
    --batch_size 32 \
    --learning_rate 1e-3 \
    --num_epochs 50 \
    --gpu auto
```

## モデルの評価

### 1. 画像再構成の評価

学習済みモデルを使用してMEGデータから画像を再構成：

```bash
cd Generation
python ATMS_reconstruction.py \
    --checkpoint_path checkpoints/best_model.pth \
    --test_data_path ../ds004212/derivatives/preprocessed_npy/sub-01/preprocessed_meg_zs_test.pkl \
    --output_dir generated_imgs \
    --gpu auto
```

### 2. 画像検索の評価

MEGデータを使用した画像検索性能の評価：

```bash
cd Retrieval
python ATMS_retrieval.py \
    --test \
    --checkpoint_path checkpoints/best_retrieval_model.pth \
    --gpu auto
```

コントラスト学習ベースの検索：

```bash
cd Retrieval
python contrast_retrieval.py \
    --test \
    --checkpoint_path checkpoints/contrast_model.pth \
    --gpu auto
```

## ディレクトリ構造

学習・評価後のディレクトリ構造：

```
EEG_Image_decode/
├── ds004212/
│   └── derivatives/
│       ├── preprocessed/          # 元のMEGデータ
│       └── preprocessed_npy/      # 前処理済みデータ
│           └── sub-01/
│               ├── preprocessed_meg_training.pkl
│               └── preprocessed_meg_zs_test.pkl
├── data/
│   ├── training_images/           # トレーニング用画像
│   ├── test_images/              # テスト用画像
│   └── CLIP/                     # CLIP特徴量
├── Generation/
│   ├── checkpoints/              # 学習済みモデル
│   └── generated_imgs/           # 生成された画像
└── Retrieval/
    └── checkpoints/              # 検索モデル
```

## トラブルシューティング

### メモリ不足エラーの場合
- バッチサイズを小さくする（例：--batch_size 8）
- MPS使用時はCPUに切り替える（--gpu cpu）

### MPS関連のエラー
- PyTorchのバージョンを確認：`python -c "import torch; print(torch.__version__)"`
- MPSサポートの確認：`python -c "import torch; print(torch.backends.mps.is_available())"`

### データパスエラー
- data_config.jsonファイルのパスが正しいか確認
- 前処理が完了しているか確認

## 参考情報

- 元の論文: [Decoding brain representations by multimodal learning of neural activity and visual features](https://arxiv.org/abs/2012.11162)
- THINGS-MEGデータセット: [OpenNeuro ds004212](https://openneuro.org/datasets/ds004212)
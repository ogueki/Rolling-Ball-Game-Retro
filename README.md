# 大玉転がしゲーム（Pyxel版）

## ゲーム概要  
このゲームは、レトロ風2D横スクロールアクションです。プレイヤーはボールキャラクターを操作し、雲が流れる空と地面の上を転がりながら障害物を避け、ゴールを目指します。ゴールに到達するとステージが進行し、難易度が上がっていきます。

## 操作方法  
- ←→キー: ボールを左右に移動  
- SPACEキー: ジャンプ  

## ゲームの特徴  
- スクロール対応の広いステージ  
- ランダム生成される障害物  
- 効果音付き（ジャンプ・衝突）  
- 雲や太陽、地面などのレトロな背景演出  
- ステージ進行とともに難易度が上昇  

## 必要環境  
※exe版も用意しています。お好みの方法でお楽しみください。

- Python 3.x  
- Pyxel ライブラリ（v2.3.18以上推奨）  
- Pygame ライブラリ（効果音再生に使用）

## 動作環境  
- 推奨画面解像度：1200x600以上  
- Windows 10/11（他環境未検証）

## インストール方法  
1. Python 3.x をインストール  
   - https://www.python.org/downloads/

2. 必要なライブラリをインストール  
   ```bash
   pip install pyxel pygame

3. リポジトリをクローンまたはZIPでダウンロード
    ```
    git clone https://github.com/your-username/oodama-rolling-pyxel.git
cd oodama-rolling-pyxel

## 実行方法
以下のコマンドでゲームを起動できます：
```
python oodama2.py
```

## exe版について
- PyInstallerを使用してビルド済み（Windows向け）
- 実行時にセキュリティ警告が表示される場合は、「詳細情報」→「実行」を選択してください
- 効果音や画像リソース（.wav, .pyxres）と同じフォルダで実行してください

## 素材ファイルについて
以下のファイルが必要です：
- my_resources.pyxres … スプライト・マップ・BGM定義
- jump.wav … ジャンプ音
- collision.wav … 衝突音

## スクリーンショット
![スクリーンショット 2025-06-01 150025](https://github.com/user-attachments/assets/042bc5e2-9c89-4c88-b0b8-308f84b9b46b)

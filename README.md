# [自分用] ML系Webアプリケーション作りテンプレート

バックエンド側をpythonで作成し、APIで待ち受け。
フロントエンド側からAPIを叩いて利用する想定。

## 構成
- バックエンド
  - FastAPI
- フロントエンド
  - SvelteKit
  - Tailwind CSS


## 動作確認
### env設定
Bedrock, Geminiへのアクセスを行う場合は .env を作成し以下を記載。

```
aws_access_key_id=
aws_secret_access_key=
aws_region=

GOOGLE_API_KEY=
```

### 実行
```
# ビルドして
docker compose build
# 動かす。バックグラウンドで動かす場合は -d 付ける
docker compose up
```

- フロント側：
  - http://localhost:5173
- バック側：
  - サンプルデータ表示： http://localhost:8000
  - APIドキュメント１： http://localhost:8000/docs
  - APIドキュメント２： http://localhost:8000/redoc

## リファレンス

公式&開発時に参考になりそうなページ色々

- [FastAPI](https://fastapi.tiangolo.com/ja/)
  - [チュートリアルページ](https://fastapi.tiangolo.com/ja/tutorial/first-steps/)
- [SVELTEKIT](https://kit.svelte.jp/)
  - [イントロダクション](https://kit.svelte.dev/docs/introduction)
  - [チュートリアルページ](https://learn.svelte.dev/tutorial/welcome-to-svelte)
- [Tailwind CSS](https://tailwindcss.com/)
  - [Install Tailwind CSS with SvelteKit](https://tailwindcss.com/docs/guides/sveltekit)
  - [tailwindcomponents](https://tailwindcomponents.com/components)
  - [Flowrift](https://flowrift.com/c/gallery)
  - [tailwind UI](https://tailwindui.com/components)
  - [Flowbite](https://flowbite.com/)
  - 
- 参考リポジトリ
  - https://github.com/smartgoo/sveltekit-fastapi-mongodb
  - https://github.com/Synalytica/fastapi-template
  - https://github.com/urjeetpatel/svelte-fastapi-template


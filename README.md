# JobMentor Customer Success Dashboard

## 概要

本システムは、Data Pro SolutionsのCustomer Success担当者向けに開発した相談分析ダッシュボードです。

JobMentor（就活支援サービス）に寄せられる相談データをAIが分析し、カテゴリ分類・根本原因分析・データ集計を行うことで、サービス改善につなげることを目的としています。

---

## 背景

就活支援サービスではAI相談機能は充実していますが、利用者全体の相談内容を分析し、サービス改善へ活用する仕組みは十分ではありません。

そこでCustomer Success担当者が相談データを分析し、JobMentorの各機能改善へ活用できるダッシュボードを提案しました。

---

## 主な機能

- AIによる就活相談
- AI回答生成（OpenAI API）
- 相談内容のカテゴリ分類
- 根本原因分析
- SQLiteへのデータ保存
- カテゴリ別相談件数の可視化
- AI分析
- サービス改善提案

---

## システム構成

就活生
   │
   ▼
JobMentor AI相談
   │
   ▼
カテゴリ分類・根本原因分析
   │
   ▼
SQLiteへ保存
   │
   ▼
Customer Success Dashboard
   │
   ▼
相談分析
   │
   ▼
JobMentorのサービス改善

---

## 使用技術

- Python
- FastAPI
- SQLite
- OpenAI API
- HTML
- CSS
- Jinja2

---

## 工夫した点

- Customer Success担当者向けの管理画面として設計
- AI回答だけでなくカテゴリ・根本原因まで分析
- 相談件数を可視化し、サービス改善へつなげる仕組みを実装
- AIが答えを与えるだけでなく、利用者自身が課題に気付ける質問を行うよう設計

---

## 今後の展望

- 時系列分析
- AIによる改善提案の高度化
- 相談内容の詳細分析
- ダッシュボード機能の拡張

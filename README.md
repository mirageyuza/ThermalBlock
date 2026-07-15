# ThermalBlock

> Statistics-driven multi-channel thermal curve simulator with realistic block-structure generation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)]()

## Overview

**ThermalBlock** generates realistic multi-channel temperature curves (`.tpe` format) that faithfully reproduce the statistical characteristics of real thermal analysis instrument data. Unlike physics-based simulators, ThermalBlock uses a **data-driven statistical approach** — it extracts structural features from real instrument recordings and regenerates them with the same statistical distributions.

### Key features

- **Block-structured generation**: Rectangular step profiles matching real instrument quantization patterns, not smooth S-curves
- **Two-phase architecture**: S-shaped ramp-up (10-30 discrete large jumps, 70-140s) → platform oscillation with realistic overshoot
- **Multi-channel correlation**: Channel 1/2 share ramp structure but diverge independently in platform phase; Channel 3 fully independent; ambient channel with micro-drift
- **Data-driven fidelity**: Jump amplitude distribution (median ~1.0°C), block-length bimodal distribution (40% single-point, 50% standard 7-11s blocks), ch1↔ch2 correlation (~0.98)
- **Zero-dependency output**: Single-click EXE, no Python installation required on target machines

### Use cases

| Scenario | Description |
|----------|-------------|
| Instrument software QA | Generate mock .tpe files for testing data analysis pipelines |
| Algorithm development | Create controlled test datasets with known ground truth |
| Training / demonstration | Produce realistic curves for training or customer demos |
| Format migration testing | Validate .tpe parsers and converters with diverse data |

## Quick start

1. Download `TPE_Manager_v21.exe` from [Releases](https://github.com/yourname/ThermalBlock/releases)
2. Drag one or more real `.tpe` files onto the window
3. Click "Modify" — simulated `.tpe` files are generated alongside the originals

### Password

The software requires a one-time daily password: `crazy4vwo50`

## How it works

```
Real .tpe analysis → Statistical fingerprint extraction → Stochastic block generation → .tpe output
         ↓                                                    ↓
   [Block-length distribution]                    [Two-phase generator]
   [Jump amplitude distribution]                  [Correlated pair engine]
   [Channel correlation matrix]                   [Ambient drift model]
   [Ramp duration / step count]                   [Endothermic dip injector]
```

### Generation pipeline

1. **Analyze**: Read real `.tpe` SQLite data, extract targets, durations, and initial temperatures
2. **Ramp phase**: Generate S-shaped staircase ramp using sigmoid-weighted temperature increments over 5-15% of total duration
3. **Platform phase**: Stochastic block random walk with bimodal hold-length distribution and weak target bias
4. **Correlation**: Channel 1/2 share ramp timing; platform phase uses independent random walks → natural r ≈ 0.98
5. **Ambient**: Slow micro-drift (0.1°C steps, 1.2-1.8°C total range, 50-70 change points)
6. **Output**: Write to SQLite `.tpe` format, 100% compatible with original instrument software

### Why block-structured?

Real thermal analysis instruments do NOT produce smooth continuous curves. Due to ADC quantization and sensor polling intervals, the actual output is a series of **rectangular blocks** — discrete temperature levels held for varying durations. ThermalBlock replicates this behavior, which is critical for:

- Realistic instrument software testing (smooth-curve simulators cause false positives)
- Validating that data pipelines handle discrete jumps correctly
- Reproducing the visual "staircase" appearance of real instrument plots

## File format

`.tpe` files are SQLite3 databases with the schema:

```sql
CREATE TABLE sampleData (
    id INTEGER PRIMARY KEY,
    time INTEGER,        -- Unix timestamp (seconds)
    sampleIndex INTEGER, -- 0-based sample index
    data BLOB            -- Interleaved float values (÷100 = °C)
);
```

Channels: 0 = ambient, 1-3 = backface temperatures.

## Repository structure

```
ThermalBlock/
├── tpe_manager_v4.py       # Main application source (tkinter GUI)
├── i18n.py                 # Language pack generator plugin
├── lang/                   # Language JSON packs (10 languages)
├── output/dist/            # Pre-built EXE releases
├── LICENSE
└── README.md
```

## Building from source

```bash
pip install numpy
pyinstaller --onefile --windowed --name TPE_Manager tpe_manager_v4.py
```

## Localization

Use the included `i18n.py` plugin to generate language-specific builds:

```bash
# List available languages
python i18n.py --list

# Build German version
python i18n.py --lang de --build

# Build all 10 languages
python i18n.py --all
```

Output EXEs are placed in `output/dist/i18n/`.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourname/ThermalBlock&type=Date)](https://star-history.com/#yourname/ThermalBlock&Date)

---

## 🌍 中文 (Chinese)

### 概述

**ThermalBlock** 能够生成逼真的多通道温度曲线（`.tpe` 格式），忠实地再现真实热分析仪器数据的统计特征。与基于物理的模拟器不同，ThermalBlock 采用**数据驱动的统计方法**——从真实仪器记录中提取结构特征，并以相同的统计分布重新生成。

### 核心特性

- **分块结构生成**：矩形阶梯曲线匹配真实仪器的量化模式，而非平滑的 S 曲线
- **两阶段架构**：S 形升温阶段（10-30 个离散大跳跃，70-140 秒）→ 带有真实过冲的平台振荡阶段
- **多通道关联**：通道 1/2 共享升温结构但在平台阶段独立发散；通道 3 完全独立；环境通道带有微漂移
- **数据驱动保真**：跳跃幅度分布（中位数约 1.0°C）、块长度双峰分布（40% 单点、50% 标准 7-11 秒块）、ch1↔ch2 相关性（约 0.98）
- **零依赖输出**：单击即用的 EXE，目标机器无需安装 Python

### 快速开始

1. 从 [Releases](https://github.com/yourname/ThermalBlock/releases) 下载 `TPE_Manager_v21.exe`
2. 将一个或多个真实 `.tpe` 文件拖入窗口
3. 点击"修改"——模拟的 `.tpe` 文件将在原始文件旁生成

### 密码

软件需要一次性每日密码：`crazy4vwo50`

### 工作原理

```
真实 .tpe 分析 → 统计指纹提取 → 随机分块生成 → .tpe 输出
       ↓                          ↓
 [块长度分布]              [两阶段生成器]
 [跳跃幅度分布]            [关联通道对引擎]
 [通道相关性矩阵]          [环境漂移模型]
 [升温持续时间/步数]       [吸热谷注入器]
```

### 生成流程

1. **分析**：读取真实 `.tpe` SQLite 数据，提取目标温度、持续时间和初始温度
2. **升温阶段**：使用 S 形加权温度增量生成阶梯式升温曲线，占总时长的 5-15%
3. **平台阶段**：具有双峰保持时长分布和弱目标偏差的随机分块随机游走
4. **关联**：通道 1/2 共享升温时序；平台阶段使用独立随机游走 → 自然相关系数 r ≈ 0.98
5. **环境**：缓慢微漂移（0.1°C 步长，总范围 1.2-1.8°C，50-70 个变化点）
6. **输出**：写入 SQLite `.tpe` 格式，100% 兼容原始仪器软件

---

## 🌍 日本語 (Japanese)

### 概要

**ThermalBlock** は、実際の熱分析装置データの統計的特性を忠実に再現する、リアルなマルチチャンネル温度曲線（`.tpe` 形式）を生成します。物理ベースのシミュレータとは異なり、ThermalBlock は**データ駆動型の統計的アプローチ**を採用し、実際の装置記録から構造的特徴を抽出し、同じ統計分布で再生成します。

### 主な特徴

- **ブロック構造生成**：滑らかな S カーブではなく、実際の装置の量子化パターンに一致する矩形ステッププロファイル
- **2 段階アーキテクチャ**：S 字型の昇温段階（10〜30 の離散的大ジャンプ、70〜140 秒）→ リアルなオーバーシュートを持つプラトー振動
- **マルチチャンネル相関**：チャンネル 1/2 は昇温構造を共有するが、プラトー段階では独立して分岐；チャンネル 3 は完全に独立；環境チャンネルは微ドリフト付き
- **データ駆動の忠実度**：ジャンプ振幅分布（中央値約 1.0°C）、ブロック長の二峰性分布（40% 単一点、50% 標準 7〜11 秒ブロック）、ch1↔ch2 相関（約 0.98）
- **依存関係ゼロの出力**：ワンクリック EXE、対象マシンへの Python インストール不要

### クイックスタート

1. [Releases](https://github.com/yourname/ThermalBlock/releases) から `TPE_Manager_v21.exe` をダウンロード
2. 1 つ以上の実際の `.tpe` ファイルをウィンドウにドラッグ
3. 「Modify」をクリックすると、元ファイルの横にシミュレートされた `.tpe` ファイルが生成されます

### パスワード

ソフトウェアには 1 日 1 回のパスワードが必要です：`crazy4vwo50`

### 仕組み

```
実際の .tpe 分析 → 統計的指紋抽出 → 確率的ブロック生成 → .tpe 出力
        ↓                          ↓
  [ブロック長分布]            [2 段階生成器]
  [ジャンプ振幅分布]          [相関ペアエンジン]
  [チャンネル相関行列]        [環境ドリフトモデル]
  [昇温時間/ステップ数]       [吸熱ディップ注入器]
```

### 生成パイプライン

1. **分析**：実際の `.tpe` SQLite データを読み取り、目標温度、持続時間、初期温度を抽出
2. **昇温段階**：総持続時間の 5〜15% にわたって、シグモイド重み付き温度増分を使用した S 字型階段状昇温を生成
3. **プラトー段階**：二峰性保持時間分布と弱い目標バイアスを持つ確率的ブロックランダムウォーク
4. **相関**：チャンネル 1/2 は昇温タイミングを共有；プラトー段階では独立したランダムウォーク → 自然相関係数 r ≈ 0.98
5. **環境**：緩やかな微ドリフト（0.1°C ステップ、総範囲 1.2〜1.8°C、50〜70 の変化点）
6. **出力**：SQLite `.tpe` 形式で書き出し、元の装置ソフトウェアと 100% 互換

---

## 🌍 한국어 (Korean)

### 개요

**ThermalBlock**은 실제 열분석 기기 데이터의 통계적 특성을 충실히 재현하는 사실적인 다중 채널 온도 곡선(`.tpe` 형식)을 생성합니다. 물리 기반 시뮬레이터와 달리 ThermalBlock은 **데이터 기반 통계적 접근 방식**을 사용하여 실제 기기 기록에서 구조적 특징을 추출하고 동일한 통계 분포로 재생성합니다.

### 주요 기능

- **블록 구조 생성**: 부드러운 S-곡선이 아닌 실제 기기 양자화 패턴과 일치하는 직사각형 계단 프로필
- **2단계 아키텍처**: S자형 승온 단계(10~30개의 이산적 큰 점프, 70~140초) → 실제와 같은 오버슈트가 있는 플래토 진동
- **다중 채널 상관관계**: 채널 1/2는 승온 구조를 공유하지만 플래토 단계에서 독립적으로 분기; 채널 3은 완전히 독립적; 환경 채널은 미세 드리프트 포함
- **데이터 기반 충실도**: 점프 진폭 분포(중앙값 약 1.0°C), 블록 길이 이봉 분포(40% 단일 지점, 50% 표준 7~11초 블록), ch1↔ch2 상관관계(약 0.98)
- **의존성 없는 출력**: 원클릭 EXE, 대상 시스템에 Python 설치 불필요

### 빠른 시작

1. [Releases](https://github.com/yourname/ThermalBlock/releases)에서 `TPE_Manager_v21.exe` 다운로드
2. 하나 이상의 실제 `.tpe` 파일을 창으로 드래그
3. "Modify" 클릭 — 시뮬레이션된 `.tpe` 파일이 원본 옆에 생성됨

### 비밀번호

소프트웨어에는 일일 1회 비밀번호가 필요합니다: `crazy4vwo50`

### 작동 원리

```
실제 .tpe 분석 → 통계적 지문 추출 → 확률적 블록 생성 → .tpe 출력
       ↓                          ↓
 [블록 길이 분포]            [2단계 생성기]
 [점프 진폭 분포]            [상관 쌍 엔진]
 [채널 상관 행렬]            [환경 드리프트 모델]
 [승온 시간/단계 수]         [흡열 딥 주입기]
```

### 생성 파이프라인

1. **분석**: 실제 `.tpe` SQLite 데이터를 읽고 목표 온도, 지속 시간, 초기 온도 추출
2. **승온 단계**: 총 지속 시간의 5~15%에 걸쳐 시그모이드 가중 온도 증분을 사용한 S자형 계단식 승온 생성
3. **플래토 단계**: 이봉 유지 시간 분포와 약한 목표 편향을 가진 확률적 블록 랜덤 워크
4. **상관관계**: 채널 1/2는 승온 타이밍 공유; 플래토 단계에서는 독립적 랜덤 워크 사용 → 자연 상관계수 r ≈ 0.98
5. **환경**: 완만한 미세 드리프트(0.1°C 단계, 총 범위 1.2~1.8°C, 50~70개 변화 지점)
6. **출력**: SQLite `.tpe` 형식으로 저장, 원본 기기 소프트웨어와 100% 호환

---

## 🌍 Deutsch (German)

### Überblick

**ThermalBlock** erzeugt realistische mehrkanalige Temperaturkurven (`.tpe`-Format), die die statistischen Eigenschaften echter thermischer Analysedaten originalgetreu wiedergeben. Im Gegensatz zu physikbasierten Simulatoren verwendet ThermalBlock einen **datengesteuerten statistischen Ansatz** — es extrahiert Strukturmerkmale aus echten Instrumentenaufzeichnungen und generiert sie mit denselben statistischen Verteilungen neu.

### Hauptfunktionen

- **Blockstruktur-Generierung**: Rechteckige Stufenprofile, die den Quantisierungsmustern echter Instrumente entsprechen, keine glatten S-Kurven
- **Zweiphasen-Architektur**: S-förmige Aufheizphase (10–30 diskrete große Sprünge, 70–140 s) → Plateau-Oszillation mit realistischem Überschwingen
- **Mehrkanal-Korrelation**: Kanal 1/2 teilen die Rampenstruktur, divergieren aber in der Plateau-Phase unabhängig; Kanal 3 vollständig unabhängig; Umgebungskanal mit Mikrodrift
- **Datengesteuerte Genauigkeit**: Sprungamplitudenverteilung (Median ~1,0 °C), bimodale Blocklängenverteilung (40 % Einzelpunkt, 50 % Standard 7–11 s-Blöcke), ch1↔ch2-Korrelation (~0,98)
- **Abhängigkeitsfreie Ausgabe**: Ein-Klick-EXE, keine Python-Installation auf Zielrechnern erforderlich

### Schnellstart

1. Laden Sie `TPE_Manager_v21.exe` von [Releases](https://github.com/yourname/ThermalBlock/releases) herunter
2. Ziehen Sie eine oder mehrere echte `.tpe`-Dateien in das Fenster
3. Klicken Sie auf „Modify" — simulierte `.tpe`-Dateien werden neben den Originalen erzeugt

### Passwort

Die Software erfordert ein einmaliges tägliches Passwort: `crazy4vwo50`

### Funktionsweise

```
Echte .tpe-Analyse → Statistischer Fingerabdruck → Stochastische Blockgenerierung → .tpe-Ausgabe
         ↓                                                    ↓
   [Blocklängenverteilung]                         [Zweiphasen-Generator]
   [Sprungamplitudenverteilung]                    [Korrelationspaar-Engine]
   [Kanalkorrelationsmatrix]                       [Umgebungsdriftmodell]
   [Rampendauer / Schrittzahl]                     [Endothermer Dip-Injektor]
```

### Generierungs-Pipeline

1. **Analyse**: Echte `.tpe`-SQLite-Daten einlesen, Zielwerte, Dauern und Anfangstemperaturen extrahieren
2. **Aufheizphase**: S-förmige treppenartige Rampe mit sigmoid-gewichteten Temperaturinkrementen über 5–15 % der Gesamtdauer
3. **Plateauphase**: Stochastischer Block-Random-Walk mit bimodaler Haltedauerverteilung und schwacher Zielausrichtung
4. **Korrelation**: Kanal 1/2 teilen das Rampen-Timing; Plateauphase verwendet unabhängige Random Walks → natürliches r ≈ 0,98
5. **Umgebung**: Langsame Mikrodrift (0,1 °C-Schritte, 1,2–1,8 °C Gesamtbereich, 50–70 Änderungspunkte)
6. **Ausgabe**: Schreiben in das SQLite-Format `.tpe`, 100 % kompatibel mit der Original-Instrumentensoftware

---

## 🌍 Français (French)

### Aperçu

**ThermalBlock** génère des courbes de température multicanaux réalistes (format `.tpe`) qui reproduisent fidèlement les caractéristiques statistiques des données réelles d'instruments d'analyse thermique. Contrairement aux simulateurs basés sur la physique, ThermalBlock utilise une **approche statistique pilotée par les données** — il extrait les caractéristiques structurelles des enregistrements réels et les régénère avec les mêmes distributions statistiques.

### Fonctionnalités principales

- **Génération en blocs structurés** : Profils en marches rectangulaires correspondant aux motifs de quantification réels des instruments, et non des courbes S lisses
- **Architecture biphasée** : Phase de montée en forme de S (10–30 grands sauts discrets, 70–140 s) → oscillation de plateau avec dépassement réaliste
- **Corrélation multicanaux** : Les canaux 1/2 partagent la structure de montée mais divergent indépendamment en phase plateau ; canal 3 totalement indépendant ; canal ambiant avec micro-dérive
- **Fidélité pilotée par les données** : Distribution d'amplitude de saut (médiane ~1,0 °C), distribution bimodale de longueur de bloc (40 % point unique, 50 % blocs standard de 7–11 s), corrélation ch1↔ch2 (~0,98)
- **Sortie sans dépendance** : EXE en un clic, aucune installation Python requise sur les machines cibles

### Démarrage rapide

1. Téléchargez `TPE_Manager_v21.exe` depuis [Releases](https://github.com/yourname/ThermalBlock/releases)
2. Faites glisser un ou plusieurs fichiers `.tpe` réels dans la fenêtre
3. Cliquez sur « Modify » — les fichiers `.tpe` simulés sont générés à côté des originaux

### Mot de passe

Le logiciel nécessite un mot de passe quotidien unique : `crazy4vwo50`

### Fonctionnement

```
Analyse .tpe réelle → Extraction d'empreinte statistique → Génération stochastique de blocs → Sortie .tpe
         ↓                                                          ↓
   [Distribution de longueur de bloc]                    [Générateur biphasé]
   [Distribution d'amplitude de saut]                    [Moteur de paires corrélées]
   [Matrice de corrélation des canaux]                   [Modèle de dérive ambiante]
   [Durée de rampe / nombre de pas]                      [Injecteur de creux endothermique]
```

### Pipeline de génération

1. **Analyse** : Lire les données SQLite `.tpe` réelles, extraire les cibles, durées et températures initiales
2. **Phase de montée** : Générer une rampe en escalier en S utilisant des incréments de température pondérés sigmoïdes sur 5–15 % de la durée totale
3. **Phase plateau** : Marche aléatoire stochastique par blocs avec distribution bimodale de durée de maintien et faible biais de cible
4. **Corrélation** : Les canaux 1/2 partagent le timing de montée ; la phase plateau utilise des marches aléatoires indépendantes → r naturel ≈ 0,98
5. **Ambiant** : Micro-dérive lente (pas de 0,1 °C, plage totale 1,2–1,8 °C, 50–70 points de changement)
6. **Sortie** : Écriture au format SQLite `.tpe`, 100 % compatible avec le logiciel d'instrument d'origine

---

## 🌍 Español (Spanish)

### Descripción general

**ThermalBlock** genera curvas de temperatura multicanal realistas (formato `.tpe`) que reproducen fielmente las características estadísticas de los datos reales de instrumentos de análisis térmico. A diferencia de los simuladores basados en física, ThermalBlock utiliza un **enfoque estadístico basado en datos**: extrae características estructurales de grabaciones reales de instrumentos y las regenera con las mismas distribuciones estadísticas.

### Características principales

- **Generación en bloques estructurados**: Perfiles de escalón rectangulares que coinciden con los patrones de cuantificación reales, no curvas S suaves
- **Arquitectura bifásica**: Fase de rampa en forma de S (10–30 grandes saltos discretos, 70–140 s) → oscilación de meseta con sobreimpulso realista
- **Correlación multicanal**: Los canales 1/2 comparten la estructura de rampa pero divergen independientemente en la fase de meseta; canal 3 completamente independiente; canal ambiente con microderiva
- **Fidelidad basada en datos**: Distribución de amplitud de salto (mediana ~1,0 °C), distribución bimodal de longitud de bloque (40 % punto único, 50 % bloques estándar de 7–11 s), correlación ch1↔ch2 (~0,98)
- **Salida sin dependencias**: EXE de un solo clic, no requiere instalación de Python en las máquinas de destino

### Inicio rápido

1. Descargue `TPE_Manager_v21.exe` desde [Releases](https://github.com/yourname/ThermalBlock/releases)
2. Arrastre uno o más archivos `.tpe` reales a la ventana
3. Haga clic en "Modify" — los archivos `.tpe` simulados se generan junto a los originales

### Contraseña

El software requiere una contraseña diaria única: `crazy4vwo50`

### Cómo funciona

```
Análisis .tpe real → Extracción de huella estadística → Generación estocástica de bloques → Salida .tpe
         ↓                                                        ↓
   [Distribución de longitud de bloque]               [Generador bifásico]
   [Distribución de amplitud de salto]                [Motor de pares correlacionados]
   [Matriz de correlación de canales]                 [Modelo de deriva ambiente]
   [Duración de rampa / número de pasos]              [Inyector de valle endotérmico]
```

### Canalización de generación

1. **Análisis**: Leer datos SQLite `.tpe` reales, extraer objetivos, duraciones y temperaturas iniciales
2. **Fase de rampa**: Generar rampa escalonada en S usando incrementos de temperatura ponderados sigmoides sobre el 5–15 % de la duración total
3. **Fase de meseta**: Caminata aleatoria estocástica por bloques con distribución bimodal de duración de retención y sesgo débil hacia el objetivo
4. **Correlación**: Los canales 1/2 comparten el tiempo de rampa; la fase de meseta usa caminatas aleatorias independientes → r natural ≈ 0,98
5. **Ambiente**: Microderiva lenta (pasos de 0,1 °C, rango total 1,2–1,8 °C, 50–70 puntos de cambio)
6. **Salida**: Escritura en formato SQLite `.tpe`, 100 % compatible con el software original del instrumento

---

## 🌍 Português (Brazilian Portuguese)

### Visão geral

O **ThermalBlock** gera curvas de temperatura multicanal realistas (formato `.tpe`) que reproduzem fielmente as características estatísticas dos dados reais de instrumentos de análise térmica. Diferentemente dos simuladores baseados em física, o ThermalBlock utiliza uma **abordagem estatística orientada por dados** — extrai características estruturais de gravações reais de instrumentos e as regenera com as mesmas distribuições estatísticas.

### Principais recursos

- **Geração em blocos estruturados**: Perfis de degrau retangulares que correspondem aos padrões de quantização reais dos instrumentos, não curvas S suaves
- **Arquitetura bifásica**: Fase de rampa em forma de S (10–30 grandes saltos discretos, 70–140 s) → oscilação de platô com sobressinal realista
- **Correlação multicanal**: Os canais 1/2 compartilham a estrutura de rampa, mas divergem independentemente na fase de platô; canal 3 totalmente independente; canal ambiente com microderiva
- **Fidelidade orientada por dados**: Distribuição de amplitude de salto (mediana ~1,0 °C), distribuição bimodal de comprimento de bloco (40% ponto único, 50% blocos padrão de 7–11 s), correlação ch1↔ch2 (~0,98)
- **Saída sem dependências**: EXE de um clique, sem necessidade de instalação do Python nas máquinas de destino

### Início rápido

1. Baixe o `TPE_Manager_v21.exe` em [Releases](https://github.com/yourname/ThermalBlock/releases)
2. Arraste um ou mais arquivos `.tpe` reais para a janela
3. Clique em "Modify" — os arquivos `.tpe` simulados são gerados ao lado dos originais

### Senha

O software requer uma senha diária única: `crazy4vwo50`

### Como funciona

```
Análise .tpe real → Extração de impressão digital estatística → Geração estocástica de blocos → Saída .tpe
         ↓                                                              ↓
   [Distribuição de comprimento de bloco]                   [Gerador bifásico]
   [Distribuição de amplitude de salto]                     [Motor de pares correlacionados]
   [Matriz de correlação de canais]                         [Modelo de deriva ambiente]
   [Duração da rampa / número de passos]                    [Injetor de vale endotérmico]
```

### Pipeline de geração

1. **Análise**: Ler dados SQLite `.tpe` reais, extrair alvos, durações e temperaturas iniciais
2. **Fase de rampa**: Gerar rampa em escada em S usando incrementos de temperatura ponderados sigmoides ao longo de 5–15% da duração total
3. **Fase de platô**: Passeio aleatório estocástico por blocos com distribuição bimodal de duração de retenção e viés fraco em direção ao alvo
4. **Correlação**: Os canais 1/2 compartilham o tempo de rampa; a fase de platô usa passeios aleatórios independentes → r natural ≈ 0,98
5. **Ambiente**: Microderiva lenta (passos de 0,1 °C, faixa total de 1,2–1,8 °C, 50–70 pontos de mudança)
6. **Saída**: Gravação no formato SQLite `.tpe`, 100% compatível com o software original do instrumento

---

## 🌍 Русский (Russian)

### Обзор

**ThermalBlock** генерирует реалистичные многоканальные температурные кривые (формат `.tpe`), которые точно воспроизводят статистические характеристики реальных данных приборов термического анализа. В отличие от физических симуляторов, ThermalBlock использует **статистический подход на основе данных** — извлекает структурные особенности из реальных записей приборов и восстанавливает их с теми же статистическими распределениями.

### Ключевые возможности

- **Генерация блочной структуры**: Прямоугольные ступенчатые профили, соответствующие реальным паттернам квантования приборов, а не гладкие S-образные кривые
- **Двухфазная архитектура**: S-образная фаза нарастания (10–30 дискретных больших скачков, 70–140 с) → колебания плато с реалистичным перерегулированием
- **Многоканальная корреляция**: Каналы 1/2 имеют общую структуру нарастания, но независимо расходятся на фазе плато; канал 3 полностью независим; канал окружающей среды с микродрейфом
- **Точность на основе данных**: Распределение амплитуды скачков (медиана ~1,0 °C), бимодальное распределение длины блока (40% одиночные точки, 50% стандартные блоки 7–11 с), корреляция ch1↔ch2 (~0,98)
- **Вывод без зависимостей**: EXE-файл в один клик, установка Python на целевых компьютерах не требуется

### Быстрый старт

1. Скачайте `TPE_Manager_v21.exe` со страницы [Releases](https://github.com/yourname/ThermalBlock/releases)
2. Перетащите один или несколько реальных файлов `.tpe` в окно
3. Нажмите «Modify» — смоделированные файлы `.tpe` будут созданы рядом с оригиналами

### Пароль

Программное обеспечение требует одноразовый ежедневный пароль: `crazy4vwo50`

### Принцип работы

```
Анализ реального .tpe → Извлечение статистического отпечатка → Стохастическая генерация блоков → Вывод .tpe
         ↓                                                                   ↓
   [Распределение длины блока]                                    [Двухфазный генератор]
   [Распределение амплитуды скачков]                              [Движок коррелированных пар]
   [Матрица корреляции каналов]                                   [Модель дрейфа среды]
   [Длительность нарастания / число шагов]                        [Инжектор эндотермического провала]
```

### Конвейер генерации

1. **Анализ**: Чтение реальных данных SQLite `.tpe`, извлечение целей, длительностей и начальных температур
2. **Фаза нарастания**: Генерация S-образной ступенчатой рампы с использованием сигмоидально-взвешенных приращений температуры на протяжении 5–15% общей длительности
3. **Фаза плато**: Стохастическое блочное случайное блуждание с бимодальным распределением времени удержания и слабым смещением к цели
4. **Корреляция**: Каналы 1/2 имеют общее время нарастания; на фазе плато используются независимые случайные блуждания → естественный r ≈ 0,98
5. **Окружающая среда**: Медленный микродрейф (шаги 0,1 °C, общий диапазон 1,2–1,8 °C, 50–70 точек изменения)
6. **Вывод**: Запись в формат SQLite `.tpe`, 100% совместимость с оригинальным программным обеспечением прибора

---

## 🌍 العربية (Arabic)

### نظرة عامة

يقوم **ThermalBlock** بتوليد منحنيات درجة حرارة متعددة القنوات واقعية (بتنسيق `.tpe`) تعيد إنتاج الخصائص الإحصائية لبيانات أجهزة التحليل الحراري الحقيقية بأمانة. على عكس المحاكيات القائمة على الفيزياء، يستخدم ThermalBlock **نهجًا إحصائيًا قائمًا على البيانات** — حيث يستخرج السمات الهيكلية من تسجيلات الأجهزة الحقيقية ويعيد توليدها بنفس التوزيعات الإحصائية.

### الميزات الرئيسية

- **توليد هيكل الكتل**: مقاطع مستطيلة متدرجة تطابق أنماط التكميم الحقيقية للأجهزة، وليس منحنيات S ناعمة
- **معمارية ثنائية الطور**: مرحلة صعود على شكل S (10–30 قفزة كبيرة منفصلة، 70–140 ثانية) → تذبذب المنصة مع تجاوز واقعي
- **ارتباط متعدد القنوات**: القناتان 1/2 تتشاركان هيكل الصعود لكنهما تتباعدان بشكل مستقل في مرحلة المنصة؛ القناة 3 مستقلة تمامًا؛ قناة البيئة مع انجراف دقيق
- **دقة قائمة على البيانات**: توزيع سعة القفزات (الوسيط ~1.0°م)، توزيع ثنائي النسق لطول الكتلة (40% نقطة مفردة، 50% كتل قياسية 7–11 ثانية)، ارتباط ch1↔ch2 (~0.98)
- **مخرجات بدون تبعيات**: EXE بنقرة واحدة، لا يتطلب تثبيت Python على الأجهزة المستهدفة

### البداية السريعة

1. قم بتنزيل `TPE_Manager_v21.exe` من [Releases](https://github.com/yourname/ThermalBlock/releases)
2. اسحب ملف `.tpe` حقيقي واحد أو أكثر إلى النافذة
3. انقر على "Modify" — يتم إنشاء ملفات `.tpe` المحاكاة بجانب الملفات الأصلية

### كلمة المرور

يتطلب البرنامج كلمة مرور يومية لمرة واحدة: `crazy4vwo50`

### كيفية العمل

```
تحليل .tpe حقيقي → استخراج البصمة الإحصائية → توليد الكتل العشوائي → مخرجات .tpe
         ↓                                                    ↓
   [توزيع طول الكتلة]                              [مولد ثنائي الطور]
   [توزيع سعة القفزات]                             [محرك الأزواج المترابطة]
   [مصفوفة ارتباط القنوات]                         [نموذج الانجراف البيئي]
   [مدة الصعود / عدد الخطوات]                      [حاقن الانخفاض الماص للحرارة]
```

### خط أنابيب التوليد

1. **التحليل**: قراءة بيانات SQLite `.tpe` الحقيقية، استخراج الأهداف والمدد ودرجات الحرارة الأولية
2. **مرحلة الصعود**: توليد صعود متدرج على شكل S باستخدام زيادات درجة الحرارة الموزونة سيجمويديًا على مدى 5–15% من المدة الإجمالية
3. **مرحلة المنصة**: مسيرة عشوائية للكتل بتوزيع ثنائي النسق لمدة الثبات وانحياز ضعيف نحو الهدف
4. **الارتباط**: القناتان 1/2 تتشاركان توقيت الصعود؛ مرحلة المنصة تستخدم مسيرات عشوائية مستقلة → r طبيعي ≈ 0.98
5. **البيئة**: انجراف دقيق بطيء (خطوات 0.1°م، نطاق إجمالي 1.2–1.8°م، 50–70 نقطة تغيير)
6. **المخرجات**: كتابة بتنسيق SQLite `.tpe`، متوافقة 100% مع برنامج الجهاز الأصلي

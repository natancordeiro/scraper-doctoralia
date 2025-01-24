<div align="left" style="position: relative;">
<img src="https://yt3.googleusercontent.com/ytc/AIdro_nfu68FSSCavTB3PbN8bC2WNH4GQc3u5WiLnHcO5mExVQ=s900-c-k-c0x00ffffff-no-rj" align="right" width="15%" style="margin: -20px 0 0 20px;">
<h1>Scraper Doctoralia</h1>

<p align="left">
	<img src="https://img.shields.io/github/license/natancordeiro/scraper-doctoralia?style=default&logo=opensourceinitiative&logoColor=white&color=00c3a5" alt="license">
	<img src="https://img.shields.io/github/last-commit/natancordeiro/scraper-doctoralia?style=default&logo=git&logoColor=white&color=00c3a5" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/natancordeiro/scraper-doctoralia?style=default&color=00c3a5" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/natancordeiro/scraper-doctoralia?style=default&color=00c3a5" alt="repo-language-count">
</p>
<p align="left"><!-- default option, no dependency badges. -->
</p>
<p align="left">
	<!-- default option, no dependency badges. -->
</p>
</div>
<br clear="right">

## 🔗 Sumário

- [📍 Visão Geral](#-visão-geral)
- [👾 Funcionalidades](#-funcionalidades)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
  - [📂 Índice do Projeto](#-índice-do-projeto)
- [🚀 Começando](#-começando)
  - [☑️ Pré-requisitos](#-pré-requisitos)
  - [⚙️ Instalação](#-instalação)
  - [🤖 Uso](#🤖-uso)
- [🔰 Contribuindo](#-contribuindo)
- [🎗 Licença](#-licença)

---

## 📍 Visão Geral

O **Scraper Doctoralia** é uma aplicação desenvolvida em Python que realiza extração automatizada de informações sobre profissionais de saúde listados na plataforma Doctoralia. Ele obtém dados como nome, especialidade e avaliações, salvando-os em um arquivo `.json` para análise posterior.

---

## 👾 Funcionalidades

- Raspagem de dados de profissionais de saúde por cidade e especialidade.
- Salvamento de informações em formatos JSON.
- Logs detalhados para monitoramento do processo.

---

## 📁 Estrutura do Projeto

```sh
└── scraper-doctoralia/
    ├── LICENSE
    ├── data
    │   └── cities.json
    ├── main.py
    ├── requirements.txt
    ├── src
    │   └── scraper.py
    └── utils
        ├── parsing.py
        └── setup_logger.py
```

### 📂 Project Index
<details open>
	<summary><b><code>SCRAPER-DOCTORALIA/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/natancordeiro/scraper-doctoralia/blob/master/main.py'>main.py</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/natancordeiro/scraper-doctoralia/blob/master/requirements.txt'>requirements.txt</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- src Submodule -->
		<summary><b>src</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/natancordeiro/scraper-doctoralia/blob/master/src/scraper.py'>scraper.py</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- utils Submodule -->
		<summary><b>utils</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='https://github.com/natancordeiro/scraper-doctoralia/blob/master/utils/parsing.py'>parsing.py</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			<tr>
				<td><b><a href='https://github.com/natancordeiro/scraper-doctoralia/blob/master/utils/setup_logger.py'>setup_logger.py</a></b></td>
				<td><code>❯ REPLACE-ME</code></td>
			</tr>
			</table>
		</blockquote>
	</details>
</details>

---
## 🚀 Começando

### ☑️ Pré-requisitos

- Python 3.9 ou superior;
- Pip para gerenciamento de pacotes.


### ⚙️ Instalação

1. Clone o repositório:
```sh
❯ git clone https://github.com/natancordeiro/scraper-doctoralia
```

2. Navegue até o diretório:
```sh
❯ cd scraper-doctoralia
```

3. Instale as dependências:


**Using pip** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt
```




### 🤖 Uso
Execute o scraper com o comando:
**Using pip** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python main.py
```


## 🔰 Contribuindo


<details closed>
<summary>Contributing Guidelines</summary>

1. Faça um fork do repositório.
2. Crie uma branch para sua funcionalidade:
   
```sh
   git clone https://github.com/natancordeiro/scraper-doctoralia
```

3. Realize suas alterações e faça um commit.
   
```sh
   git checkout -b new-feature
```

4. Submeta um pull request.

</details>

---

## 🎗 Licença

Este projeto está licenciado sob os termos da [MIT]([https://mit.com/licenses/](https://opensource.org/license/mit)).

---


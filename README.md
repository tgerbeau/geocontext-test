# geocontext-test

This repository contains an integration test suite designed to validate the correct behavior of the MCP server `ignfab/geocontext` across different language models.

## Purpose

The main goal is to ensure that end-to-end interactions with `ignfab/geocontext` remain stable and consistent when switching model providers or model versions.

## What is tested

- Agent creation using a configured model name
- Real model invocation through integration scenarios
- Functional response checks for expected outputs

## Usage

### Testing with anthropic models

```bash
export MODEL_NAME="anthropic:claude-sonnet-4-6"
export ANTHROPIC_API_KEY=YourKey

uv run pytest
```

### Testing with google models

```bash
export MODEL_NAME="google_genai:gemini-2.5-flash"
export GOOGLE_API_KEY=YourKey

uv run pytest
```

```bash
export MODEL_NAME="google_genai:gemini-3.1-flash-lite-preview"
export GOOGLE_API_KEY=YourKey

uv run pytest
```

## Tests

| Test | Fichier | Outil(s) attendu(s) | Description |
|------|---------|---------------------|-------------|
| `test_france_capital` | [test_france_capital.py](test_france_capital.py) | aucun (LLM seul) | Test basique sans MCP — vérifie que le LLM répond "Paris" |
| `test_adminexpress` | [test_adminexpress.py](test_adminexpress.py) | `adminexpress` | Commune/département à partir de coordonnées (2.35, 48.85) |
| `test_cadastre` | [test_cadastre.py](test_cadastre.py) | `cadastre` | Parcelle cadastrale au 73 av. de Paris, Saint-Mandé |
| `test_describe_type` | [test_describe_type.py](test_describe_type.py) | `gpf_wfs_describe_type` | Attributs de la table BDTOPO_V3:batiment |
| `test_get_features` | [test_get_features.py](test_get_features.py) | `gpf_wfs_get_features` | Bâtiments BDTOPO proches de Chamonix |
| `test_search_batiment` | [test_search_batiment.py](test_search_batiment.py) | `gpf_wfs_search_types` | Recherche de tables contenant des bâtiments |
| `test_search_ecoles` | [test_search_ecoles.py](test_search_ecoles.py) | `gpf_wfs_search_types` | Recherche de tables contenant des écoles |
| `test_chaining_geocode` | [test_chaining_geocode.py](test_chaining_geocode.py) | `geocode` → `altitude` | Chaînage géocodage + altitude (mairie de Chamonix ≈ 1036m) |
| `test_chaining_cadastre_urbanisme` | [test_chaining_cadastre_urbanisme.py](test_chaining_cadastre_urbanisme.py) | `geocode` → `cadastre` → `urbanisme` | Chaînage géocodage, cadastre et urbanisme |
| `test_urbanisme` | [test_urbanisme.py](test_urbanisme.py) | `urbanisme` | Règles d'urbanisme pour la parcelle 94067000AI0042 |

## Derniers résultats de tests

**Date** : 11 mai 2026
**Modèle** : `anthropic:claude-haiku-4-5`
**Serveur MCP** : `geocontext@0.9.7`

### Run 1 — 10/10 passed (2 min 07 s)

| Test | Résultat |
|------|----------|
| test_adminexpress | ✅ PASSED |
| test_cadastre | ✅ PASSED |
| test_chaining_cadastre_urbanisme | ✅ PASSED |
| test_chaining_geocode_altitude | ✅ PASSED |
| test_describe_type | ✅ PASSED |
| test_france_capital | ✅ PASSED |
| test_get_features | ✅ PASSED |
| test_search_batiment | ✅ PASSED |
| test_search_ecoles | ✅ PASSED |
| test_urbanisme | ✅ PASSED |

### Run 2 — 9/10 passed (2 min 01 s)

| Test | Résultat | Détail |
|------|----------|--------|
| test_adminexpress | ✅ PASSED | |
| test_cadastre | ✅ PASSED | |
| test_chaining_cadastre_urbanisme | ✅ PASSED | |
| test_chaining_geocode_altitude | ✅ PASSED | |
| test_describe_type | ✅ PASSED | |
| test_france_capital | ✅ PASSED | |
| test_get_features | ✅ PASSED | |
| test_search_batiment | ✅ PASSED | |
| test_search_ecoles | ✅ PASSED | |
| test_urbanisme | ❌ FAILED | Flaky LLM — propriété inexistante demandée par le modèle |

### Run 3 — 9/10 passed (1 min 51 s)

| Test | Résultat | Détail |
|------|----------|--------|
| test_adminexpress | ✅ PASSED | |
| test_cadastre | ✅ PASSED | |
| test_chaining_cadastre_urbanisme | ✅ PASSED | |
| test_chaining_geocode_altitude | ✅ PASSED | |
| test_describe_type | ✅ PASSED | |
| test_france_capital | ✅ PASSED | |
| test_get_features | ✅ PASSED | |
| test_search_batiment | ✅ PASSED | |
| test_search_ecoles | ✅ PASSED | |
| test_urbanisme | ❌ FAILED | Flaky LLM — feature introuvable |

### Observations

- **9 tests sur 10 sont stables** à 100% sur les 3 runs.
- **`test_urbanisme`** est sujet à de la flakiness LLM : le modèle `claude-haiku-4-5` ne chaîne pas toujours correctement les appels d'outils (propriétés inventées, mauvais identifiants). Il passe ~50% du temps.

## License

[MIT](LICENSE)


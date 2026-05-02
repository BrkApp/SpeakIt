# SpeakIt — Dictée vocale pour Windows

Application système légère qui écoute le raccourci **Ctrl+Espace**, enregistre votre voix, transcrit via Whisper en local, et injecte le texte dans le champ actif (navigateur, Word, Slack, etc.).

## Fonctionnement

1. L'app démarre minimisée dans le **system tray**
2. Cliquez dans n'importe quel champ texte
3. **Ctrl+Espace** → enregistrement (icône rouge)
4. Parlez
5. **Ctrl+Espace** → fin d'enregistrement, transcription, injection du texte
6. Notification Windows de confirmation

## Installation

### Prérequis

- Windows 10/11
- Python 3.10+

### Dépendances

```bash
pip install -r requirements.txt
```

### Premier lancement

Au premier lancement, `faster-whisper` télécharge automatiquement le modèle Whisper choisi (~150 Mo pour "base"). Assurez-vous d'avoir une connexion Internet pour ce premier démarrage.

```bash
python main.py
```

> **Note :** Le module `keyboard` nécessite des droits administrateur sur certaines configurations Windows pour capturer les raccourcis globaux.

## Configuration

Modifiez `config.py` pour ajuster :

| Paramètre | Défaut | Description |
|---|---|---|
| `WHISPER_MODEL` | `"base"` | Modèle Whisper : `"tiny"`, `"base"`, `"small"` |
| `WHISPER_LANGUAGE` | `"fr"` | Code langue (ex: `"en"`, `"fr"`, `"de"`) |
| `COMPUTE_TYPE` | `"int8"` | `"int8"` (CPU), `"float16"` (GPU CUDA) |
| `HOTKEY` | `"ctrl+space"` | Raccourci global |
| `AUDIO_DEVICE` | `None` | Micro (None = défaut système) |
| `ENABLE_LOG` | `True` | Historique dans `transcription_log.txt` |

## Packager en .exe

```bash
pip install pyinstaller
python setup.py
```

L'exécutable est généré dans `dist/SpeakIt.exe`.

## Stack technique

- **faster-whisper** (CTranslate2) — transcription locale rapide
- **keyboard** — hotkey global sans focus
- **sounddevice** + **numpy** — capture micro
- **pyperclip** + **pyautogui** — injection texte via clipboard + Ctrl+V
- **pystray** + **Pillow** — icône system tray
- **winotify** — notifications toast Windows

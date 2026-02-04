# import logging

# def get_logger(name=__name__, level=logging.INFO):
#     logger = logging.getLogger(name)
#     if not logger.handlers:
#         handler = logging.StreamHandler()
#         formatter = logging.Formatter(
#             '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
#         )
#         handler.setFormatter(formatter)
#         logger.addHandler(handler)
#         logger.setLevel(level)
#     return logger


from __future__ import annotations

import logging
from pathlib import Path


def get_logger(name: str, log_file: Path, level: int = logging.INFO) -> logging.Logger:
    """
    Logger réutilisable: écrit dans un fichier + affiche en console.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Évite les doublons si on appelle get_logger plusieurs fois
    if logger.handlers:
        return logger

    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(fmt)

    sh = logging.StreamHandler()
    sh.setLevel(level)
    sh.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(sh)

    # Empêche de dupliquer vers le root logger
    logger.propagate = False

    return logger
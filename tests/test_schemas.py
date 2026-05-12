from serving.schemas import PredictionInput


SAMPLE = {
    "Identifiant arc": 12345,
    "heure": 8,
    "jour_semaine": 1,
    "is_weekend": 0,
    "Taux d'occupation": 0.42,
    "lat": 48.85,
    "lon": 2.35,
    "Etat arc": "ouvert",
}


def test_aliases_fr_parse_correctly():
    p = PredictionInput(**SAMPLE)
    assert p.identifiant_arc == 12345
    assert p.taux_occupation == 0.42
    assert p.etat_arc == "ouvert"


def test_etat_arc_default_is_unknown():
    payload = {k: v for k, v in SAMPLE.items() if k != "Etat arc"}
    p = PredictionInput(**payload)
    assert p.etat_arc == "unknown"


def test_to_model_dict_includes_etat_arc_for_v2():
    p = PredictionInput(**SAMPLE)
    row = p.to_model_dict(include_etat_arc=True)
    assert "Etat arc" in row
    assert row["Etat arc"] == "ouvert"
    assert row["Identifiant arc"] == 12345
    assert row["Taux d'occupation"] == 0.42


def test_to_model_dict_excludes_etat_arc_for_v1():
    p = PredictionInput(**SAMPLE)
    row = p.to_model_dict(include_etat_arc=False)
    assert "Etat arc" not in row
    assert row["Identifiant arc"] == 12345

import json
import os

SAVE_DIR = "saves"
SAVE_FILE = os.path.join(SAVE_DIR, "save_data.json")


def load_save_data() -> dict:
    """세이브 파일 로드 (없거나 손상된 경우 빈 딕셔너리 반환)"""
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_stage_clear(mode: str, stage_id: int, attempts: int) -> dict:
    """스테이지 클리어 기록 저장 및 갱신"""
    os.makedirs(SAVE_DIR, exist_ok=True)
    data = load_save_data()

    mode_data = data.setdefault(mode, {})
    stage_key = str(stage_id)
    record = mode_data.get(stage_key, {
        "cleared": False,
        "clear_count": 0,
        "best_attempts": None
    })

    record["cleared"] = True
    record["clear_count"] += 1
    if record["best_attempts"] is None or attempts < record["best_attempts"]:
        record["best_attempts"] = attempts

    mode_data[stage_key] = record

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


def get_stage_record(data: dict, mode: str, stage_id: int) -> dict:
    """특정 모드와 스테이지의 기록 조회"""
    return data.get(mode, {}).get(str(stage_id), {
        "cleared": False,
        "clear_count": 0,
        "best_attempts": None
    })
import database

def sample_result(text="Test prompt"):
    return {
        "original_text": text,
        "optimized_text": text,
        "original_token_count": 10,
        "optimized_token_count": 8,
        "tokens_saved": 2,
        "savings_Percentage": 20.0,
        "model_name": "SampleLLM",
        "selected_strategy": "whitespace_normalization",
        "optimization_status": "improved"
    }


def setup_test_database(tmp_path, monkeypatch):
    test_db_path = tmp_path / "test_token_optimizer.db"

    monkeypatch.setattr(
        database,
        "DATABASE_NAME",
        str(test_db_path)
    )

    database.initialize_database()


def test_save_and_retrieve_optimization(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)

    result = sample_result()

    record_id = database.save_optimization(result)

    history = database.get_optimization_history()

    assert record_id == 1
    assert len(history) == 1
    assert history[0]["original_text"] == "Test prompt"
    assert history[0]["tokens_saved"] == 2
    assert history[0]["model_name"] == "SampleLLM"


def test_history_returns_newest_first(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)

    database.save_optimization(sample_result("First prompt"))
    database.save_optimization(sample_result("Second prompt"))
    database.save_optimization(sample_result("Third prompt"))

    history = database.get_optimization_history()

    assert history[0]["original_text"] == "Third prompt"
    assert history[1]["original_text"] == "Second prompt"
    assert history[2]["original_text"] == "First prompt"


def test_history_respects_limit(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)

    database.save_optimization(sample_result("First"))
    database.save_optimization(sample_result("Second"))
    database.save_optimization(sample_result("Third"))

    history = database.get_optimization_history(limit=2)

    assert len(history) == 2
    assert history[0]["original_text"] == "Third"
    assert history[1]["original_text"] == "Second"


def test_empty_history_returns_empty_list(tmp_path, monkeypatch):
    setup_test_database(tmp_path, monkeypatch)

    history = database.get_optimization_history()

    assert history == []

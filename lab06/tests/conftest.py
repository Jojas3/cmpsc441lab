import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "llm: tests that require Ollama running")


@pytest.fixture(autouse=True)
def check_ollama():
    """Skip all tests if Ollama is not available."""
    try:
        import ollama
        ollama.list()
    except Exception:
        pytest.skip("Ollama is not running")

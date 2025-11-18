from ai.providers.provider_template import ProviderTemplate


def test_provider_template_basic():
    p = ProviderTemplate()
    models = p.get_models()
    assert isinstance(models, dict)
    # check generate_response returns the mocked string and includes prompt
    resp = p.generate_response("hello world", "system")
    assert "hello world" in resp
    assert "mock response" in resp

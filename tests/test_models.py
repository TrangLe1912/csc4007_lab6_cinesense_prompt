import pytest
import torch

from src.models import ModelConfig, build_model


@pytest.mark.parametrize("name", ["rnn", "lstm", "gru", "transformer"])
def test_backbone_output_shape(name: str) -> None:
    config = ModelConfig(vocab_size=100, hidden_size=16, num_layers=1, transformer_heads=4)
    model = build_model(name, config).eval()
    token_ids = torch.randint(0, config.vocab_size, (2, 8))
    with torch.inference_mode():
        output = model(token_ids)
    assert output.shape == (2, config.hidden_size)
    assert torch.isfinite(output).all()


def test_hidden_size_must_match_transformer_heads() -> None:
    config = ModelConfig(vocab_size=100, hidden_size=15, num_layers=1, transformer_heads=4)
    with pytest.raises(ValueError):
        build_model("transformer", config)


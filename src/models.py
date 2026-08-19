"""Small, comparable sequence backbones used by the Lab 6 benchmark."""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


class OptionalDependencyError(RuntimeError):
    """Raised when an optional model dependency is unavailable."""


class RecurrentBackbone(nn.Module):
    def __init__(
        self,
        kind: str,
        vocab_size: int,
        hidden_size: int,
        num_layers: int,
    ) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        recurrent = {"rnn": nn.RNN, "lstm": nn.LSTM, "gru": nn.GRU}[kind]
        self.encoder = recurrent(
            hidden_size,
            hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )
        self.norm = nn.LayerNorm(hidden_size)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        encoded, _ = self.encoder(self.embedding(token_ids))
        return self.norm(encoded).mean(dim=1)


class TransformerBackbone(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        hidden_size: int,
        num_layers: int,
        transformer_heads: int,
    ) -> None:
        super().__init__()
        if hidden_size % transformer_heads != 0:
            raise ValueError("hidden_size must be divisible by transformer_heads")
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        layer = nn.TransformerEncoderLayer(
            d_model=hidden_size,
            nhead=transformer_heads,
            dim_feedforward=4 * hidden_size,
            dropout=0.0,
            activation="gelu",
            batch_first=True,
            norm_first=False,
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=num_layers)
        self.norm = nn.LayerNorm(hidden_size)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        encoded = self.encoder(self.embedding(token_ids))
        return self.norm(encoded).mean(dim=1)


class MambaBackbone(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        hidden_size: int,
        num_layers: int,
    ) -> None:
        super().__init__()
        try:
            from mamba_ssm import Mamba
        except (ImportError, OSError) as exc:
            raise OptionalDependencyError(
                "mamba-ssm is not installed or its compiled extension cannot be loaded"
            ) from exc

        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.layers = nn.ModuleList(
            [
                Mamba(d_model=hidden_size, d_state=16, d_conv=4, expand=2)
                for _ in range(num_layers)
            ]
        )
        self.norm = nn.LayerNorm(hidden_size)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        encoded = self.embedding(token_ids)
        for layer in self.layers:
            encoded = encoded + layer(encoded)
        return self.norm(encoded).mean(dim=1)


@dataclass(frozen=True)
class ModelConfig:
    vocab_size: int = 20_000
    hidden_size: int = 64
    num_layers: int = 1
    transformer_heads: int = 4


def build_model(name: str, config: ModelConfig) -> nn.Module:
    """Build a sequence backbone with a shared token-to-vector interface."""
    normalized = name.lower().strip()
    if normalized in {"rnn", "lstm", "gru"}:
        return RecurrentBackbone(
            normalized,
            config.vocab_size,
            config.hidden_size,
            config.num_layers,
        )
    if normalized == "transformer":
        return TransformerBackbone(
            config.vocab_size,
            config.hidden_size,
            config.num_layers,
            config.transformer_heads,
        )
    if normalized == "mamba":
        return MambaBackbone(
            config.vocab_size,
            config.hidden_size,
            config.num_layers,
        )
    raise ValueError(f"Unsupported model: {name}")


def count_parameters(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters())

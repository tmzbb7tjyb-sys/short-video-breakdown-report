#!/usr/bin/env python3
"""Detect lightweight audio energy accents for BGM beat/cut-point analysis.

Usage:
  analyze_audio_beats.py <pcm_wav> <out_json> [--window-ms 50]

The input should be a PCM WAV, typically produced with:
  afconvert -f WAVE -d LEI16 input.m4a audio.wav

This is not a full music beat tracker. It is a deterministic evidence helper
for finding likely BGM accents to compare against visual cuts/action changes.
"""

from __future__ import annotations

import argparse
import json
import math
import struct
from pathlib import Path


def read_wav_pcm16(path: Path) -> tuple[int, int, list[int]]:
    data = path.read_bytes()
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise ValueError(f"{path} is not a RIFF/WAVE file")

    offset = 12
    channels = None
    sample_rate = None
    pcm_offset = None
    pcm_size = None

    while offset + 8 <= len(data):
      chunk_id = data[offset:offset + 4]
      chunk_size = struct.unpack_from("<I", data, offset + 4)[0]
      chunk_start = offset + 8
      chunk_end = chunk_start + chunk_size

      if chunk_id == b"fmt ":
          if chunk_size < 16:
              raise ValueError("Invalid fmt chunk")
          channels = struct.unpack_from("<H", data, chunk_start + 2)[0]
          sample_rate = struct.unpack_from("<I", data, chunk_start + 4)[0]
          bits_per_sample = struct.unpack_from("<H", data, chunk_start + 14)[0]
          if bits_per_sample != 16:
              raise ValueError(f"Only 16-bit PCM WAV is supported, got {bits_per_sample}-bit")
      elif chunk_id == b"data":
          pcm_offset = chunk_start
          pcm_size = chunk_size
          break

      offset = chunk_end + (chunk_size % 2)

    if channels is None or sample_rate is None or pcm_offset is None or pcm_size is None:
        raise ValueError("Could not find fmt/data chunks")

    pcm = data[pcm_offset:pcm_offset + pcm_size]
    pcm = pcm[: len(pcm) // 2 * 2]
    values = list(struct.unpack("<" + "h" * (len(pcm) // 2), pcm))
    return sample_rate, channels, values


def detect_accents(sample_rate: int, channels: int, values: list[int], window_ms: int) -> list[dict[str, float]]:
    window = max(1, int(sample_rate * window_ms / 1000)) * channels
    energies: list[tuple[float, float]] = []
    for index in range(0, len(values) - window, window):
        chunk = values[index:index + window]
        rms = math.sqrt(sum(x * x for x in chunk) / len(chunk))
        second = index / channels / sample_rate
        energies.append((second, rms))

    raw: list[tuple[float, float]] = []
    for index in range(2, len(energies) - 2):
        second, rms = energies[index]
        prev = sum(item[1] for item in energies[index - 2:index]) / 2
        nxt = sum(item[1] for item in energies[index + 1:index + 3]) / 2
        if rms > prev * 1.15 and rms > nxt * 0.82 and rms > 300:
            raw.append((round(second, 2), round(rms, 1)))

    picked: list[tuple[float, float]] = []
    for second, rms in raw:
        if picked and second - picked[-1][0] < 0.16:
            if rms > picked[-1][1]:
                picked[-1] = (second, rms)
        else:
            picked.append((second, rms))

    return [{"second": second, "rms": rms} for second, rms in picked]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_wav")
    parser.add_argument("out_json")
    parser.add_argument("--window-ms", type=int, default=50)
    args = parser.parse_args()

    input_wav = Path(args.input_wav)
    sample_rate, channels, values = read_wav_pcm16(input_wav)
    duration = len(values) / channels / sample_rate
    candidates = detect_accents(sample_rate, channels, values, args.window_ms)
    result = {
        "input": str(input_wav),
        "rate": sample_rate,
        "channels": channels,
        "duration": duration,
        "method": f"{args.window_ms}ms_rms_energy_accents_pcm16",
        "candidates": candidates,
    }
    Path(args.out_json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{args.out_json} candidates={len(candidates)} duration={duration:.3f}s")


if __name__ == "__main__":
    main()

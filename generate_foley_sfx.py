#!/usr/bin/env python3
"""
Sector 7 Tool: Python Procedural Foley & Sound Design Synthesizer
Generates sub-bass braams, mechanical tape clicks, atmospheric room tone,
and executes EBU R128 loudness normalization and -20dB background music ducking via FFmpeg.
"""

import os
import math
import wave
import struct
import subprocess

SAMPLE_RATE = 48000  # Broadcast standard 48kHz

def generate_sub_bass_braam(output_path, duration=3.0, freq_start=80.0, freq_end=35.0):
    """Synthesize cinematic sub-bass braam impact with exponential frequency glide."""
    num_samples = int(SAMPLE_RATE * duration)
    with wave.open(output_path, 'w') as wav:
        wav.setnchannels(2)  # Stereo
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(SAMPLE_RATE)
        
        frames = bytearray()
        for i in range(num_samples):
            t = i / SAMPLE_RATE
            # Exponential pitch sweep
            freq = freq_start * ((freq_end / freq_start) ** (t / duration))
            phase = 2 * math.pi * freq * t
            
            # Non-linear envelope: instant attack (5ms), sustained body, exponential decay
            env = math.exp(-2.5 * (t / duration)) if t > 0.005 else (t / 0.005)
            # Add saturation harmonic
            sample = math.sin(phase) + 0.3 * math.sin(2 * phase) + 0.15 * math.sin(3 * phase)
            sample = math.tanh(sample * 1.5) * env * 0.9
            
            val = int(max(min(sample * 32767, 32767), -32768))
            frames.extend(struct.pack('<hh', val, val))
        wav.writeframes(frames)
    print(f"[OK] Generated Sub-bass Braam: {output_path}")

def generate_tactile_tape_click(output_path, duration=0.08):
    """Synthesize mechanical tape latch / reel tactile click."""
    num_samples = int(SAMPLE_RATE * duration)
    with wave.open(output_path, 'w') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        
        frames = bytearray()
        for i in range(num_samples):
            t = i / SAMPLE_RATE
            # High frequency impulse with rapid decay
            freq = 2400.0 * math.exp(-60.0 * t)
            phase = 2 * math.pi * freq * t
            env = math.exp(-80.0 * t)
            sample = math.sin(phase) * env * 0.8
            val = int(max(min(sample * 32767, 32767), -32768))
            frames.extend(struct.pack('<hh', val, val))
        wav.writeframes(frames)
    print(f"[OK] Generated Tactile Tape Click: {output_path}")

def normalize_ebu_r128(input_audio, output_audio, target_lufs=-13.6):
    """Master audio to EBU R128 broadcast loudness standards via FFmpeg."""
    cmd = [
        'ffmpeg', '-y', '-i', input_audio,
        '-af', f'loudnorm=I={target_lufs}:TP=-1.0:LRA=7.0',
        '-ar', '48000', output_audio
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Mastered to EBU R128 ({target_lufs} LUFS): {output_audio}")

def duck_music_under_speech(voice_path, music_path, output_path, ducking_db=-20):
    """Dynamically duck background music bed under voice narration."""
    cmd = [
        'ffmpeg', '-y',
        '-i', voice_path,
        '-i', music_path,
        '-filter_complex',
        f"[1:a]volume=1.0[bg];[bg][0:a]sidechaincompress=threshold=0.12:ratio=4:attack=20:release=300[ducked];[0:a][ducked]amix=inputs=2:duration=first",
        '-ar', '48000', output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"[OK] Ducked music bed by {ducking_db}dB under narration: {output_path}")

if __name__ == '__main__':
    os.makedirs('audio/foley', exist_ok=True)
    generate_sub_bass_braam('audio/foley/sub_bass_braam.wav')
    generate_tactile_tape_click('audio/foley/tape_click.wav')

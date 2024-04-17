import os
import argparse
from sdr2 import SDR_cal
from stft_dis import STFT_distance
from visqol import visqol_audio
from mel_loss import Mel_loss
from pesq_local import pesq_folder
from stoi import stoi_folder


def Codec_Eval(syn_path, ref_path, metric_name, target_sr=16000):
    if metric_name == 'SDR':
        SDR_scores, ans = SDR_cal(ref_path, syn_path, target_sr)
        for file, score in SDR_scores.items():
            print(f"SDR for {file}: {score:.2f} dB")
    elif metric_name == 'stft_dis':
        stft_scores, ans = STFT_distance(ref_path, syn_path, target_sr)
        for file, score in stft_scores.items():
            print(f"STFT for {file}: {score:.2f}")
    elif metric_name == 'visqol':
        visqol_scores, ans = visqol_audio(ref_path, syn_path, int(target_sr))
        for file, score in visqol_scores.items():
            print(f"visqol for {file}: {score:.2f}")
    elif metric_name == 'mel_loss':
        mel_losses, ans = Mel_loss(ref_path, syn_path, target_sr)
        for file, score in mel_losses.items():
            print(f"Mel Loss for {file}: {score:.2f}")
    elif metric_name == 'pesq':
        pesq_scores, ans = pesq_folder(ref_path, syn_path, int(target_sr))
        for file, score in pesq_scores.items():
            print(f"PESQ for {file}: {score:.2f}")
    elif metric_name == 'stoi':
        stoi_scores, ans = stoi_folder(ref_path, syn_path)
        for file, score in stoi_scores.items():
            print(f"STOI for {file}: {score:.2f}")
    else:
        print('error metric name, please check! metric_name should be [SDR, stft_dis, visqol, mel_loss, pesq, stoi]')
        assert 1==2
    print(f'{metric_name} mean score is: ', ans)
    return ans


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Codec performance evaluation.')
    parser.add_argument('--syn_path', type=str, help='Directory containing synetic audio files')
    parser.add_argument('--ref_path', type=str, help='Directory containing reference audio files')
    parser.add_argument('--metric_name', type=str, help='The metric name, [SDR, stft_dis, visqol, mel_loss, pesq, stoi]')
    parser.add_argument('--target_sr', type=str, help='The target sampling rate')
    args = parser.parse_args()
    Codec_Eval(args.syn_path, args.ref_path, args.metric_name, args.target_sr)



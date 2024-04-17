from pesq import pesq
import numpy as np
import soundfile as sf
import librosa
import glob
import os

def pesq_folder(ref_folder, est_folder, target_sr=16000):
    """
    Calculate PESQ (Perceptual evaluation of speech quality) metric between pairs of reference and estimated audio files
    located in the given directories, optionally resampling all files to a specified sample rate.
    
    Parameters:
        ref_folder (str): The folder path containing the reference audio files (.wav).
        est_folder (str): The folder path containing the estimated/generated audio files (.wav).
    
    Returns:
        dict: A dictionary containing the STOI for each pair of audio files, with file names as keys.
    """
    # 获取所有参考音频和生成音频的路径
    ref_files = sorted(glob.glob(os.path.join(ref_folder, '*.wav')))
    est_files = sorted(glob.glob(os.path.join(est_folder, '*.wav')))
    
    if len(ref_files) != len(est_files):
        raise ValueError("The number of reference and estimated files do not match.")
    
    pesq_score = {}
    mean_score = []
    for ref_path, est_path in zip(ref_files, est_files):
        # 读取音频文件
        ref_audio, ref_rate = sf.read(ref_path)
        est_audio, est_rate = sf.read(est_path)
        
        # 确保音频是单通道
        if ref_audio.ndim > 1:
            ref_audio = ref_audio[:, 0]
        if est_audio.ndim > 1:
            est_audio = est_audio[:, 0]

        # 如果指定了目标采样率，进行重采样
        if target_sr is not None:
            if ref_rate != target_sr:
                ref_audio = librosa.resample(ref_audio, orig_sr=ref_rate, target_sr=target_sr)
            if est_rate != target_sr:
                est_audio = librosa.resample(est_audio, orig_sr=est_rate, target_sr=target_sr)

        score = pesq(target_sr, ref_audio, est_audio, mode = 'wb')
        mean_score.append(score)
        pesq_score[os.path.basename(ref_path)] = score
    
    return pesq_score, np.mean(mean_score)
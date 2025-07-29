import os
import tempfile

import torch
import whisper
from fastapi import UploadFile, File, HTTPException, APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/whisper", tags=["whisper"])

# GPU가 사용 가능한 경우만 fp16 사용
fp16_enabled = torch.cuda.is_available()
print("GPU 사용 가능 여부:", fp16_enabled)

# Whisper 모델 로드 (서버 시작시 한 번만 로드)
model = whisper.load_model("base")


@router.post("/transcribe")
async def transcribe_audio(
        file: UploadFile = File(...),
        language: str | None = None,
        task: str = "transcribe"  # transcribe 또는 translate
):
    """
    오디오 파일을 업로드하여 텍스트로 변환합니다.

    - **file**: 오디오 파일 (mp3, wav, m4a, flac 등)
    - **language**: 언어 코드 (선택사항, 자동 감지됨)
    - **task**: 'transcribe' (원본 언어) 또는 'translate' (영어로 번역)
    """

    # 지원되는 오디오 파일 형식 확인
    allowed_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.mp4', '.avi', '.mov'}
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"지원되지 않는 파일 형식입니다. 지원 형식: {', '.join(allowed_extensions)}"
        )

    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            while chunk := await file.read(1024 * 1024):  # 1MB씩 읽기
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name

        # 오디오 로드 및 전처리
        audio = whisper.load_audio(tmp_file_path)
        audio = whisper.pad_or_trim(audio)

        # log-Mel spectrogram 생성
        mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

        # 언어 감지
        _, probs = model.detect_language(mel)
        detected_language = max(probs, key=probs.get)

        print("감지된 언어", detected_language)

        # 디코딩 옵션 설정
        options = whisper.DecodingOptions(
            language=language if language else detected_language,
            task=task
        )

        # 오디오 디코딩
        result = whisper.decode(model, mel, options)

        # 임시 파일 삭제
        os.unlink(tmp_file_path)

        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "detected_language": detected_language,
            "language_confidence": probs[detected_language],
            "task": task,
            "text": result.text,
            "language_probabilities": dict(sorted(probs.items(), key=lambda x: x[1], reverse=True)[:5])
        })

    except Exception as e:
        # 에러 발생시 임시 파일 정리
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

        raise HTTPException(status_code=500, detail=f"오디오 변환 중 오류가 발생했습니다: {str(e)}")


@router.post("/transcribe-full")
async def transcribe_audio_full(
        file: UploadFile = File(...),
        language: str | None = None,
        task: str = "transcribe"
):
    """
    전체 오디오 파일을 세그먼트별로 변환합니다 (더 정확한 결과).

    - **file**: 오디오 파일
    - **language**: 언어 코드 (선택사항)
    - **task**: 'transcribe' 또는 'translate'
    """

    # 지원되는 오디오 파일 형식 확인
    allowed_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.mp4', '.avi', '.mov'}
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"지원되지 않는 파일 형식입니다. 지원 형식: {', '.join(allowed_extensions)}"
        )

    try:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            # chunk 단위로 파일 저장
            while chunk := await file.read(1024 * 1024):  # 1MB씩 읽기
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name

        # Whisper의 transcribe 함수 사용 (전체 파일 처리)
        result = model.transcribe(
            audio=tmp_file_path,
            language=language,
            task=task,
            verbose=False,
            fp16=fp16_enabled  # GPU 사용 시 float 16 연산 활성화 ( 속도 향상)
        )

        # 임시 파일 삭제
        os.unlink(tmp_file_path)

        # 세그먼트 정보 포함
        segments = []
        for segment in result["segments"]:
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })

        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "detected_language": result["language"],
            "task": task,
            "text": result["text"],
            "segments": segments
        })

    except Exception as e:
        # 에러 발생시 임시 파일 정리
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

        raise HTTPException(status_code=500, detail=f"오디오 변환 중 오류가 발생했습니다: {str(e)}")

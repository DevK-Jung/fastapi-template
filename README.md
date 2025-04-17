# 🚀 FastAPI Template

FastAPI 프로젝트를 빠르게 시작할 수 있도록 구성된 템플릿입니다. 
Poetry, Pydantic v2, 타입 안전한 요청/응답 모델, 서비스 분리 구조 등을 포함하고 있어 **확장성과 유지보수성에 최적화**되어 있습니다.

---

## 📦 주요 기술 스택

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [Poetry](https://python-poetry.org/) – 의존성 및 빌드 관리
- Python 3.13

---

## 🚀 실행 방법

### 1. Poetry 설치

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. 의존성 설치

```bash
poetry install
```

### 3. 서버 실행

```bash
poetry run uvicorn fastapi_template.main:app --reload
```

### 4. Swagger 문서 확인

- http://localhost:8000/docs
- http://localhost:8000/redoc

---

## 👤 Author

- **JungHyeon Kim**
   📧 dev.kjung@gmail.com
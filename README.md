# Token Optimizer

A Python-based prompt optimization system that reduces unnecessary tokens in user-provided text while preserving important information through rule-based semantic safety checks.

The project uses **FastAPI**, **Python**, **tiktoken**, and **SQLite** to optimize text, estimate token usage and API input costs, track optimization history, and manage temporary conversation sessions.

---

## 1. Project Overview

Large Language Models (LLMs) process user prompts as tokens. Unnecessary words, repeated sentences, and redundant phrases can increase token usage and potentially increase API input costs.

Token Optimizer addresses this problem by generating multiple optimized versions of an input prompt, validating them against selected semantic safety rules, and selecting the candidate with the lowest token count.

### Main Objectives

- Reduce unnecessary token usage in prompts.
- Preserve important information such as negations, numbers, constraints, and technical identifiers.
- Compare multiple optimization techniques.
- Select the best safe optimization candidate.
- Calculate estimated LLM input costs and potential savings.
- Maintain optimization history and statistics.
- Implement temporary conversation sessions with a fixed five-minute expiry.
- Generate permanent optimization reports after session expiry.

---

## 2. Key Features

### A. Token Counting

- Uses the `tiktoken` library for token counting.
- Uses the `cl100k_base` encoding.
- Calculates original and optimized token counts.

**Note:** This tokenizer is used for token estimation. It is not necessarily the native tokenizer of every supported LLM.

### B. Seven Text Optimization Techniques

The candidate engine currently evaluates seven optimization techniques:

| No. | Technique | Description |
|---|---|---|
| 1 | Duplicate Line Removal | Removes repeated lines. |
| 2 | Whitespace Normalization | Removes unnecessary spaces and blank lines. |
| 3 | Duplicate Sentence Removal | Removes repeated sentences. |
| 4 | Repeated Phrase Removal | Removes repeated multi-word phrases. |
| 5 | Common Expression Shortening | Replaces unnecessarily long expressions with shorter alternatives. |
| 6 | Filler Word Removal | Removes selected filler words such as "actually", "basically", and "literally". |
| 7 | Conservative Stop Word Removal | Removes selected articles such as "the", "a", and "an". |

The original input is also included as a baseline candidate.

### C. Candidate Selection Engine

The candidate engine:

1. Receives the original text.
2. Generates multiple optimization candidates.
3. Counts tokens for each candidate.
4. Validates each candidate using the semantic safety validator.
5. Rejects candidates that fail safety checks.
6. Selects the candidate with the lowest token count among safe candidates.
7. Retains the original text if no safe candidate reduces token usage.

The system avoids applying an optimization when it increases token usage.

### D. Rule-Based Semantic Safety Validation

The current semantic validator checks five categories:

| No. | Safety Check | Purpose |
|---|---|---|
| 1 | Negation Preservation | Protects words such as `not`, `never`, and `cannot`. |
| 2 | Modal Verb Preservation | Protects words such as `must`, `should`, `may`, and `could`. |
| 3 | Numbers and Dates | Checks preservation of numeric values and selected date/amount patterns. |
| 4 | Technical Identifiers | Protects identifiers such as `userId`, `API_KEY`, and `user_id`. |
| 5 | Constraints and Conditions | Checks phrases such as `before`, `after`, `at least`, `only`, and `maximum`. |

**Important limitation:** These are rule-based lexical checks. They do not guarantee complete semantic equivalence or understand the full context of a sentence.

Contextual semantic similarity using sentence embeddings is planned for a future version.

### E. Cost Calculation

The system estimates potential LLM input costs using configurable model pricing.

Currently configured example models:

- `SampleLLM`
- `SampleLLM-Pro`

The system calculates:

- Original input cost.
- Optimized input cost.
- Estimated cost saved.

These values are estimates based on configured pricing, not actual charges from a live LLM provider.

### F. Optimization History

SQLite stores optimization records, including:

- Original text.
- Optimized text.
- Original token count.
- Optimized token count.
- Tokens saved.
- Savings percentage.
- Model name.
- Selected optimization strategy.
- Optimization status.
- Creation timestamp.

### G. Statistics Tracking

The application tracks:

- Total optimization requests.
- Improved requests.
- Unchanged requests.
- Total tokens saved.
- Total estimated cost saved.
- Improvement rate percentage.

A statistics reset endpoint is also available.

### H. Five-Minute Session Management

The application implements temporary conversation sessions with a fixed five-minute expiry.

Session functionality includes:

- Unique session ID generation.
- Session creation and status checking.
- Fixed expiry calculated from session creation time.
- Session-based prompt optimization.
- Conversation message storage.
- Automatic finalization when an expired session is accessed.
- Deletion of temporary conversation messages.
- Permanent storage of session reports.

Session reports contain:

- Total messages.
- Total original tokens.
- Total optimized tokens.
- Total tokens saved.
- Savings percentage.
- Total estimated cost saved.
- Session start and end timestamps.

**Important implementation detail:** Expiry finalization is triggered when an endpoint checks an expired session. The current implementation does not use a background scheduler to finalize sessions at the exact expiry time.

---

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend REST API framework |
| Uvicorn | ASGI server |
| tiktoken | Token counting |
| Pydantic | Request and response validation |
| SQLite | Persistent database storage |
| Pytest | Automated testing |
| Swagger UI | API documentation and testing |

---

## 4. Project Architecture

The application follows a modular backend architecture.

```text
                    USER
                      |
                      v
                SWAGGER UI
                      |
                      v
                 main.py
                      |
                      v
           optimization_service.py
                      |
                      v
              candidate_engine.py
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       optimizer.py  semantic_validator.py
          |           |
          +-----+-----+
                |
                v
           token_counter.py
                |
                v
        Best Candidate Selection
                |
          +-----+------+
          |            |
          v            v
    cost_calculator  statistics_tracker
          |            |
          +------+-----+
                 |
                 v
              database.py
                 |
                 v
              SQLite
                 |
                 v
             API Response
```

Session management is handled separately through:

- `session_database.py`
- `session_service.py`

These modules manage conversation sessions, temporary messages, expiry validation, and permanent session reports.

---

## 5. Project Structure

```text
token-optimizer/
│
├── main.py
├── schemas.py
│
├── optimizer.py
├── candidate_engine.py
├── optimization_service.py
├── semantic_validator.py
│
├── token_counter.py
├── cost_calculator.py
├── pricing.py
├── statistics_tracker.py
│
├── database.py
├── session_database.py
├── session_service.py
│
├── test_api.py
├── test_candidate_engine.py
├── test_cost_calculator.py
├── test_database.py
├── test_main.py
├── test_optimization_service.py
├── test_optimizer.py
├── test_semantic_validator.py
├── test_statistics_tracker.py
│
├── .gitignore
└── token_optimizer.db
```

The database file is created and initialized by the application. Its actual location depends on the database configuration.

---

## 6. Installation and Setup

### Prerequisites

- Python 3.9 or later
- pip
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/manas-verma11/Token-Optimizer
```

### Step 2: Navigate to the project directory

```bash
cd token-optimizer
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the virtual environment

For macOS/Linux:

```bash
source .venv/bin/activate
```

For Windows:

```powershell
.venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install fastapi uvicorn tiktoken pydantic pytest
```

If the repository contains a maintained `requirements.txt`, install dependencies using:

```bash
pip install -r requirements.txt
```

### Step 6: Start the application

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

### Step 7: Open Swagger documentation

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to execute and test the API endpoints interactively.

---

## 7. API Endpoints

The current implementation provides the following endpoints.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/count-tokens` | Counts tokens in input text. |
| POST | `/optimize` | Performs prompt optimization. |
| POST | `/optimize-text` | Optimizes text and returns detailed results. |
| GET | `/history` | Retrieves optimization history. |
| GET | `/statistics` | Retrieves optimization statistics. |
| POST | Statistics reset endpoint | Resets tracked statistics. |
| POST | `/sessions` | Creates a new session. |
| GET | `/sessions/{session_id}` | Retrieves session status. |
| GET | `/sessions/{session_id}/history` | Retrieves conversation history. |
| POST | `/sessions/{session_id}/optimize` | Optimizes text inside a session. |
| GET | `/session-reports` | Retrieves session reports. |
| GET | `/session-reports/{session_id}` | Retrieves a report for a specific session. |

For exact request and response schemas, refer to the Swagger documentation at `/docs`.

---

## 8. Example Optimization

### Original Input

```text
The developer built a new application.
The developer built a new application.
```

### Optimized Output

```text
The developer built a new application.
```

### Example Result

| Metric | Original | Optimized |
|---|---:|---:|
| Token count | 14 | 7 |

**Tokens saved:** 7

**Token reduction:** 50%

**Selected strategy:** `duplicate_sentence_removal`

The system also returns the results of all candidate strategies so their token counts and savings can be compared.

---

## 9. Session Lifecycle

The session management system follows this lifecycle:

```text
Create Session
      |
      v
Session Status: ACTIVE
      |
      v
Store Conversation Messages
      |
      v
Optimize Session Prompts
      |
      v
Five-Minute Expiry Reached
      |
      v
Expired Session Detected
      |
      v
Generate Permanent Report
      |
      v
Delete Temporary Messages
      |
      v
Session Status: COMPLETED
```

After expiry:

- Conversation history is no longer accessible.
- History requests return HTTP `410 Gone`.
- Permanent session reports remain retrievable.

This separates temporary conversation context from permanent optimization analytics.

---

## 10. Testing

The project uses `pytest` for automated testing.

Run the complete test suite:

```bash
python -m pytest -v
```

### Latest Verified Test Results

```text
collected 95 items

95 passed in 0.28s
```

The test suite covers:

- API functionality.
- Candidate generation and selection.
- Token counting and cost calculation.
- Database operations.
- Optimization strategies.
- Semantic safety validation.
- Statistics tracking.
- Session creation and expiry.
- Session report generation and message deletion.

**Latest verified status: 95 tests passed, 0 failures.**

---

## 11. Current Limitations

The current version is a deterministic, rule-based text optimization system.

The following features are not yet implemented:

1. **Contextual Semantic Similarity:** Sentence embedding-based semantic comparison is planned but not implemented.
2. **SmolLM2 Integration:** Local LLM integration using SmolLM2 is planned.
3. **LLM-Based Compression:** The current optimizer does not use an LLM to generate compressed prompts.
4. **Output Quality Evaluation:** Actual downstream LLM response quality has not yet been systematically evaluated.
5. **Background Session Expiry:** Session finalization currently occurs when an expired session is accessed, rather than through a background scheduler.

---

## 12. Future Enhancements

Planned improvements include:

- Integrating sentence embeddings for contextual semantic similarity.
- Exploring local model integration with SmolLM2.
- Adding LLM-assisted prompt compression.
- Evaluating semantic preservation through similarity scores and human evaluation.
- Supporting model-specific tokenizers.
- Improving optimization strategy selection.
- Adding more comprehensive API integration tests.
- Improving production readiness, monitoring, and error handling.

---

## 13. Project Status

| Component | Status |
|---|---|
| FastAPI backend | Implemented |
| Token counting | Implemented |
| Seven optimization techniques | Implemented |
| Candidate selection engine | Implemented |
| Rule-based semantic validation | Implemented |
| Cost calculation | Implemented |
| Optimization history | Implemented |
| Statistics tracking | Implemented |
| SQLite integration | Implemented |
| Five-minute session management | Implemented |
| Permanent session reports | Implemented |
| Automated tests | 95 passing |
| Contextual semantic similarity | Planned |
| SmolLM2 integration | Planned |
| LLM-based compression | Planned |

---


*Token Optimizer — Reducing unnecessary tokens while preserving important information.*
    

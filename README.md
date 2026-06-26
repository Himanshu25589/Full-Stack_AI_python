# Python to GenAI

A structured walk-through of my path from Python fundamentals to building with Generative AI — kept open for anyone learning the same path, and as an honest record of how I got here.

This isn't a course dump. Each folder reflects a stage I actually went through, in order, while building toward [Multi-Agent AI Research System](https://github.com/Himanshu25589/Multi-Agent-Research-System) and [AI Video & Meeting Assistant](https://github.com/Himanshu25589/AI-Video-Assistant).

**This repo is open-source — not because I think it's groundbreaking, but because every "Hello World" deserves company along the way. Fork it, learn from it, or just see how messy the beginning of a real journey actually looks.**

---

## Why This Exists

Most "AI learning" repos either show finished projects with no context, or raw course notes with no structure. This sits in between — the actual progression from "what is a Python list" to "how does a RAG pipeline retrieve context," documented as I went.

---

## What's Inside

### Python Fundamentals
| Folder | Topic |
|---|---|
| `00_python` | Setup and basics |
| `01_virtual` | Virtual environments |
| `02_datatypes` | Data types |
| `03_conditionals` | If/else, match statements |
| `04_loops` | For, while loops |
| `05_functions` | Functions and scope |
| `06_chai_business` | Applied practice problems |
| `07_comprehensions` | List, dict, set comprehensions |
| `08_generators` | Generator functions |
| `09_decorators` | Decorators |
| `10_oop` | Object-oriented programming |
| `11_exceptions` | Error handling |
| `12_threads_concurrency` | Threading and concurrency |
| `13_async_python` | Async/await |
| `14_pydantic` | Data validation with Pydantic |

### Generative AI — LLMs, RAG, Agents *(in progress)*
| Folder | Topic |
|---|---|
| `genai_basics` | LLM fundamentals, prompting |
| `langchain_intro` | LangChain core concepts, chains |
| `rag_pipeline` | Document loaders, embeddings, vector stores |
| `agents` | Tool calling, AI agents, LangGraph basics |
| `mcp_servers` | Model Context Protocol — connecting tools to LLMs |
| `guardrails` | Input/output validation for production AI |
| `practice` | Smaller experiments and one-off scripts (Runnables, chat models, embedding models) |

### Backend for AI Systems *(upcoming)*
| Folder | Topic |
|---|---|
| `fastapi_basics` | Routing, Pydantic models, dependency injection |
| `fastapi_auth` | JWT, OAuth2, API key authentication |
| `fastapi_db` | SQLAlchemy, PostgreSQL integration |
| `fastapi_deployment` | Async patterns, rate limiting, deployment |

Goal: wrap the existing AI projects in proper REST APIs and build a third project — an AI-powered job search system combining LangChain with a FastAPI + PostgreSQL backend.

### Challenges
| Folder | Topic |
|---|---|
| `challenges` | Self-set practice problems across topics above |

---

## How to Use This

Each folder is self-contained. If you already know Python, skip straight to `genai_basics` onward. If you're starting from zero, follow the numbered folders in order.

---

## Where This Led

This foundation directly fed into two production-style projects:
- **[Multi-Agent AI Research System](https://github.com/Himanshu25589/Multi-Agent-Research-System)** — 4-agent pipeline using LangChain LCEL
- **[AI Video & Meeting Assistant](https://github.com/Himanshu25589/AI-Video-Assistant)** — multilingual RAG system with Whisper and Sarvam AI

---

**Himanshu Saini** — B.Tech, Software Engineering, DTU '28
[LinkedIn](https://linkedin.com/in/himanshusaini131) · [GitHub](https://github.com/Himanshu25589) · [Medium](https://medium.com/@himanshsaini417)

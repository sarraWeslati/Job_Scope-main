import threading
import time
import uuid
from queue import Queue, Empty
from typing import Any, Dict, Optional
import os
import json

from .scraper.scraper import scrape_jobs

# Simple in-memory job store and queue. Suitable for demo/dev only.
_job_store: Dict[str, Dict[str, Any]] = {}
_job_store_lock = threading.Lock()
_queue: Queue = Queue()

# Persistence file for job store so statuses survive restarts
_PERSIST_PATH = "data/jobs_store.json"


def _load_store():
    try:
        if not os.path.exists(_PERSIST_PATH):
            return
        with open(_PERSIST_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            with _job_store_lock:
                _job_store.clear()
                _job_store.update(data)
    except Exception:
        # ignore load errors
        pass


def _persist_store():
    try:
        os.makedirs(os.path.dirname(_PERSIST_PATH), exist_ok=True)
        with _job_store_lock:
            with open(_PERSIST_PATH, "w", encoding="utf-8") as f:
                json.dump(_job_store, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def enqueue_job(params: Optional[Dict[str, Any]] = None) -> str:
    job_id = str(uuid.uuid4())
    now = time.time()
    job = {
        "id": job_id,
        "status": "pending",
        "created_at": now,
        "started_at": None,
        "finished_at": None,
        "result": None,
        "error": None,
        "params": params or {},
    }
    with _job_store_lock:
        _job_store[job_id] = job
    # persist immediately
    _persist_store()
    _queue.put(job_id)
    return job_id


def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    with _job_store_lock:
        return _job_store.get(job_id)


def _worker_loop():
    while True:
        try:
            job_id = _queue.get(timeout=0.5)
        except Empty:
            time.sleep(0.2)
            continue

        with _job_store_lock:
            job = _job_store.get(job_id)
            if job is None:
                continue
            job["status"] = "running"
            job["started_at"] = time.time()

        try:
            params = job.get("params", {}) or {}
            # Run the scrape; ensure results saved and minimal data returned
            res = scrape_jobs(
                query=params.get("query", "python"),
                location=params.get("location", ""),
                sources=tuple(params.get("sources", ("indeed", "linkedin"))),
                max_pages=int(params.get("max_pages", 1)),
                max_jobs=int(params.get("max_jobs", 100)),
                use_playwright=bool(params.get("use_playwright", False)),
                headless=bool(params.get("headless", True)),
                proxies=tuple(params.get("proxies", ())),
                user_agents=tuple(params.get("user_agents", ())),
                timeout=int(params.get("timeout", 30)),
                retries=int(params.get("retries", 1)),
                save=True,
                return_results=False,
            )

            with _job_store_lock:
                job["status"] = "done"
                job["finished_at"] = time.time()
                job["result"] = res
                job["error"] = None
                # persist after finishing
                _persist_store()
        except Exception as e:
            with _job_store_lock:
                job["status"] = "failed"
                job["finished_at"] = time.time()
                job["result"] = None
                job["error"] = str(e)
                _persist_store()
        finally:
            _queue.task_done()


def _start_worker():
    t = threading.Thread(target=_worker_loop, daemon=True, name="scrape-worker")
    t.start()


# Start the worker on import
_load_store()
_start_worker()

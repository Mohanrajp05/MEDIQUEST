import time

import streamlit as st

from MEDIQUEST_ASSISTANT.pipeline import build_MEDIQUEST_ASSISTANT

st.set_page_config(
    page_title="MEDIQUEST Assistant",
    page_icon="🤖"
)

MAX_REQUESTS_PER_SESSION = 10

if "messages" not in st.session_state:
    st.session_state.messages = []

if "requests_used" not in st.session_state:
    st.session_state.requests_used = 0

if "last_stats" not in st.session_state:
    st.session_state.last_stats = None

if "answer_cache" not in st.session_state:
    st.session_state.answer_cache = {}

if "totals" not in st.session_state:
    st.session_state.totals = {
        "queries": 0,
        "cache_hits": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "latency": 0.0,
    }

header_left, header_right = st.columns([5, 1.4], vertical_alignment="center")

with header_left:
    st.title("🤖 MEDIQUEST Assistant")

with header_right:
    if st.button("🗑️ Delete chat data", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_stats = None
        st.session_state.answer_cache = {}
        st.session_state.totals = {
            "queries": 0,
            "cache_hits": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "latency": 0.0,
        }
        st.rerun()

st.caption("Ask me anything about the medical documents.")

@st.cache_resource(show_spinner="Setting up the assistant (only happens once)...")
def get_agent():
    return build_MEDIQUEST_ASSISTANT()

agent = get_agent()


def ask_with_stats(agent, question):
    start = time.perf_counter()
    response = agent.invoke({"messages": [{"role": "user", "content": question}]})
    latency = time.perf_counter() - start

    answer = response["messages"][-1].content

    input_tokens = 0
    output_tokens = 0
    for message in response["messages"]:
        usage = getattr(message, "usage_metadata", None)
        if usage:
            input_tokens += usage.get("input_tokens") or 0
            output_tokens += usage.get("output_tokens") or 0

    return answer, input_tokens, output_tokens, latency

# Show the past conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get a new question from the user
limit_reached = st.session_state.requests_used >= MAX_REQUESTS_PER_SESSION

question = st.chat_input(
    "Ask a question about MEDIQUEST...",
    disabled=limit_reached,
)

if limit_reached:
    st.warning(
        f"Request limit reached ({MAX_REQUESTS_PER_SESSION} per session). "
        "Refresh the page to start a new session."
    )

if question:
    st.session_state.requests_used += 1
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    cache_key = " ".join(question.lower().split())
    cached = st.session_state.answer_cache.get(cache_key)

    with st.chat_message("assistant"):
        if cached is not None:
            answer, _cached_input_tokens, _cached_output_tokens = cached
            input_tokens = 0
            output_tokens = 0
            start = time.perf_counter()
            latency = time.perf_counter() - start
            st.caption("⚡ Cached answer (no API call)")
            st.session_state.totals["cache_hits"] += 1
        else:
            with st.spinner("Thinking..."):
                answer, input_tokens, output_tokens, latency = ask_with_stats(
                    agent, question
                )
            st.session_state.answer_cache[cache_key] = (
                answer,
                input_tokens,
                output_tokens,
            )

        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    st.session_state.last_stats = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "tokens": input_tokens + output_tokens,
        "latency": latency,
    }

    st.session_state.totals["queries"] += 1
    st.session_state.totals["input_tokens"] += input_tokens
    st.session_state.totals["output_tokens"] += output_tokens
    st.session_state.totals["latency"] += latency

with st.sidebar:
    st.header("📊 Usage")

    last = st.session_state.last_stats
    if last is None:
        st.caption("No questions asked yet.")
    else:
        st.metric("Tokens (last answer)", f"{last['tokens']:,}")
        st.caption(
            f"Input {last['input_tokens']:,} · Output {last['output_tokens']:,}"
        )
        st.metric("Latency (last answer)", f"{last['latency']:.2f} s")


# Manages the request limits fro a session it provide only 10 request
    st.divider()

    totals = st.session_state.totals
    st.metric("Questions", f"{totals['queries']:,}")
    st.metric(
        "Requests",
        f"{st.session_state.requests_used} / {MAX_REQUESTS_PER_SESSION}",
    )
    st.progress(
        st.session_state.requests_used / MAX_REQUESTS_PER_SESSION
    )
    st.metric("Cache hits", f"{totals['cache_hits']:,}")
    st.metric(
        "Session tokens",
        f"{totals['input_tokens'] + totals['output_tokens']:,}",
    )
    if totals["queries"]:
        avg_latency = totals["latency"] / totals["queries"]
        st.metric("Avg latency", f"{avg_latency:.2f} s")
    else:
        st.metric("Avg latency", "—")




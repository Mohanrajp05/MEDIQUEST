"STEP 5 :  wrap the retreiver as a tool the agent can call"


from langchain_core.tools import tool


def create_search_tool(retriever):
    @tool
    def search_MEDIQUEST_ASSISTANT(question: str) -> str:
        """Search the MEDIQUEST medical documents for chunks relevant to the question."""
        matching_chunks = retriever.invoke(question)
        return "\n\n".join(chunk.page_content for chunk in matching_chunks)

    return search_MEDIQUEST_ASSISTANT

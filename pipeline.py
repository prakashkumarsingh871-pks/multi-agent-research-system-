from typing import Callable, Optional
from agent import build_reader_agent, build_search_agent, writer_chain, critic_chain


def run_research_pipeline(
    topic: str,
    on_step: Optional[Callable[[int, str], None]] = None,
) -> dict:

    state = {}

    def notify(step: int, message: str) -> None:
        if on_step is not None:
            on_step(step, message)

    # search agent working
    notify(1, "Step 1/4: Search agent is gathering information...")
    print("\n" + "=" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result["messages"][-1].text

    print("\n search result ", state["search_results"])

    # step 2 - reader agent
    notify(2, "Step 2/4: Reader agent is scraping top resources...")
    print("\n" + "=" * 50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    state["scraped_content"] = reader_result["messages"][-1].text

    print("\nscraped content: \n", state["scraped_content"])

    # step 3 - writer chain
    notify(3, "Step 3/4: Writer is drafting the report...")
    print("\n" + "=" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Final Report\n", state["report"])

    # critic report
    notify(4, "Step 4/4: Critic is reviewing the report...")
    print("\n" + "=" * 50)
    print("step 4 - critic is reviewing the report ")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\n critic report \n", state["feedback"])
    notify(5, "Pipeline completed.")

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
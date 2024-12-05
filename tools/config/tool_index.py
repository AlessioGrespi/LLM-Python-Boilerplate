tool_config = {
    "tools": [
        # {
        #     "toolSpec": {
        #         "name": "save_memory",
        #         "description": "Place to save things you think are important context and memories in your role as a personal assistant.",
        #         "inputSchema": {
        #             "json": {
        #                 "type": "object",
        #                 "properties": {
        #                     "memory": {
        #                         "type": "string",
        #                         "description": "Description of memory",
        #                     },
        #                 },
        #                 "required": ["memory"],
        #             }
        #         },
        #     }
        # },
        {
            "toolSpec": {
                "name": "time_and_date",
                "description": "get the time, date, timezone, day of week",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
        },
        {
            "toolSpec": {
                "name": "internet_search_for_sites",
                "description": "Use Brave API to search the internet and return a list of results",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "search_query": {
                                "type": "string",
                                "description": "string to enter in the search engine",
                            },
                            "number_of_results": {
                                "type": "number",
                                "description": "number of results to return, defaults to 5",
                            },
                            "page_number": {
                                "type": "number",
                                "description": "go to page number x of results, defaults to 0",
                            },
                        },
                        "required": ["search_query"],
                    }
                },
            }
        },
    ]
}

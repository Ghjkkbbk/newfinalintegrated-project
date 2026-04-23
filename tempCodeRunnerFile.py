 elif mode == "research":
            return jsonify({"response": research_agent(query)})

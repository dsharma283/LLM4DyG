class StaticGraphPrompt:
    """
    Static-graph prompt builder.
    Uses EXACT instruction (as you requested):
      'Generate the Breath First Search traversal of this graph'
    """
    def __init__(self, obj_task, args=None):
        self.obj_task = obj_task
        self.args = args

    def _format_graph(self, problem):
        lines = []
        N = problem['N']
        adj = problem['adj']
        for u in range(N):
            nbrs = " ".join(map(str, adj[u]))
            lines.append(f"{u}: {nbrs}")
        return "\n".join(lines)

    def generate_prompt_qa(self, problem, answer):
        graph_txt = self._format_graph(problem)
        instruction = "Generate the Breath First Search traversal of this graph"
        preface = (
            "You are given an undirected graph in adjacency-list form (0-indexed).\n"
            f"Start node: {problem['start']}\n"
            "Neighbors must be explored in ascending numeric order for BFS.\n"
            "Return the traversal as space-separated node IDs only.\n"
        )
        prompt = f"{preface}\nGraph:\n{graph_txt}\n\nInstruction: {instruction}"
        return {'prompt': prompt, 'answer': answer}

